from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.onboarding import *
from projectx_app.models.request import *
from projectx_app.models.task import *
from projectx_app.models.user_detail import *
from projectx_app.models.user import *
from projectx_app.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from projectx_app.forms.request import *
from projectx_app.forms.applicant import *
from projectx_app.forms.user_detail import *
from django.db.models import Sum
from datetime import timedelta
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings

def create_request_listing(request):
    applicants = User.objects.filter(user_type = 1) #applicant user
    company, requested_users, company_logo, company_name = None, None, None, None

    if 'company_id' in request.session:
        try:
            company = SystemCompanySetup.objects.get(pk = request.session['company_id'])
        except:
            company = None

        if company:
            try:
                company_logo = company.logo_image.url
            except:
                company_logo = None

            try:
                company_name = company.company_name
            except:
                company_name = None
    else:
        try:
            companyuser = CompanyUser.objects.get(user = request.user)
        except:
            companyuser = None

        if companyuser:
            company = companyuser.company

            company_setup = SystemCompanySetup.objects.get(pk = companyuser.company.id)

            try:
                company_logo = company_setup.logo_image.url
            except:
                company_logo = None

            try:
                company_name = company_setup.company_name
            except:
                company_name = None


    coonboardingtypes = CoOnboardingType.objects.filter(is_deleted = False, company = company)

    if request.user.user_type == 2 or request.user.user_type == 5: # company admin or rpo admin
        requested_users = MyRequest.objects.filter(company = company)
    elif request.user.user_type == 6 or request.user.user_type == 9: # company user or rpo user
        requested_users = MyRequest.objects.filter(created_by = request.user)

    return render(request, 'projectx_app/create-request-listing.html', { "applicants": applicants, "coonboardingtypes": coonboardingtypes, "requested_users": requested_users, "company_logo": company_logo, "company_name": company_name})


def create_request_form(request, type_id=None, user_id=None):
    bgv_documents = []
    my_request, bgv_details, hr_details, ref_details, company = None, None, None, None, None    

    company = None

    try:
        companyuser = CompanyUser.objects.get(user = self.request.user)
    except:
        companyuser = None

    if companyuser:
        company = companyuser.company

    try:
        coonboarding = CoOnboardingType.objects.get(pk=type_id)
    except:
        coonboarding = None

    if coonboarding:
        coonboardingtasks = CoOnboardingTask.objects.filter(co_onboarding_type_id = type_id)

    if coonboardingtasks:
        for task in coonboardingtasks:
            if task.step_id == '1':
                bgv_details = CoOnboardingTaskBGV.objects.filter(co_onboarding_task_id = task.id)

                if bgv_details:
                    for bgv_detail in bgv_details:
                        bgv_documents.append(bgv_detail.document.document_name)

            elif task.step_id == '2':
                ref_details = CoOnboardingTaskRefCheck.objects.filter(onboarding_ref_task_id = task.id)

            elif task.step_id == '3':
                hr_details = CoOnboardingTaskHrForm.objects.filter(onboarding_hr_task_id = task.id)


    if request.method == 'POST' and request.POST.getlist('task_id'):
        # if user is company admin    
        my_request = MyRequest.objects.create(applicant_id = user_id, co_onboarding_type = coonboarding, company = company)

        if my_request:
            return redirect('request-listing')

    return render(request, 'projectx_app/create-request-form.html', {"coonboardingtasks": coonboardingtasks, "bgv_details": bgv_details, "ref_details": ref_details, "hr_details": hr_details, "bgv_documents": bgv_documents, "coonboarding": coonboarding, "user_id": user_id, "type_id": type_id })


class RequestApplicantCreateView(LoginRequiredMixin, CompanyGeneric, generic.CreateView):
    form_class = ApplicantForm
    template_name = 'projectx_app/request-create-applicant-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        applicant = form.save()
        return redirect('/create-request/'+str(applicant.id))


class MyRequestView(LoginRequiredMixin, generic.ListView):
    model = MyRequest
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        company = None
        try:
            companyuser = CompanyUser.objects.get(user = self.request.user)
        except:
            companyuser = None

        if companyuser:
            company = companyuser.company

        my_request = self.model.objects.filter(company = company)
        return my_request


def my_request_detail(request, type_id=None):
    bgv_documents = []
    my_request, bgv_details, hr_details, ref_details, admin_company, user_company = None, None, None, None, None, None     

    try:
        coonboarding = CoOnboardingType.objects.get(pk=type_id)
    except:
        coonboarding = None

    if coonboarding:
        coonboardingtasks = CoOnboardingTask.objects.filter(co_onboarding_type_id = type_id)

    if coonboardingtasks:
        for task in coonboardingtasks:
            if task.step_id == '1':
                bgv_details = CoOnboardingTaskBGV.objects.filter(co_onboarding_task_id = task.id)

                if bgv_details:
                    for bgv_detail in bgv_details:
                        bgv_documents.append(bgv_detail.document.document_name)

            elif task.step_id == '2':
                ref_details = CoOnboardingTaskRefCheck.objects.filter(onboarding_ref_task_id = task.id)

            elif task.step_id == '3':
                hr_details = CoOnboardingTaskHrForm.objects.filter(onboarding_hr_task_id = task.id)

    return render(request, 'projectx_app/my-request-form.html', {"coonboardingtasks": coonboardingtasks, "bgv_details": bgv_details, "ref_details": ref_details, "hr_details": hr_details, "bgv_documents": bgv_documents, "coonboarding": coonboarding, "type_id": type_id })


def search_applicant(request):
    data_array = []
    search_content = request.POST['search_content']
    applicants = Applicant.objects.filter(
        Q(user__first_name__icontains = search_content)|
        Q(user__last_name__icontains = search_content)|
        Q(user__email__icontains = search_content))

    if applicants:
        for applicant in applicants:
            data_array.append({
                'applicant_id': applicant.id,
                'name': applicant.user.first_name+' '+applicant.user.last_name,
                'email': applicant.user.email,
            })

    return JsonResponse(data_array, safe=False)


def search_onboarding_tasks(request, id=None, applicant_id=None):
    data_array = []

    is_requested = MyRequest.objects.filter(applicant_id = applicant_id, co_onboarding_type_id = id)

    if is_requested:
        data_array.append({'is_requested': 'true'})
    else:
        coonboardingtasks = CoOnboardingTask.objects.filter(co_onboarding_type_id = int(id)).order_by('step_id')
        if coonboardingtasks:
            for task in coonboardingtasks:
                due_date = task.created_at + timedelta(days=int(task.due_date))
                data_array.append({
                    'id':task.id,
                    'vendor_id':task.vendor.id,
                    'step_id':task.step_id,
                    'task_name':task.task_name,
                    'vendor': task.vendor.vendor.vendor_company_name,
                    'due_date':due_date.strftime("%d-%m-%Y"),
                })

    return JsonResponse(data_array, safe=False)



def create_request(request, id=None):
    company, company_logo, username = None, None, None

    try:
        applicant = Applicant.objects.get(id = id)
    except:
        applicant = None

    if applicant:
        username = applicant.user.first_name +' '+applicant.user.last_name

    if 'company_id' in request.session:
        try:
            company = SystemCompanySetup.objects.get(pk = request.session['company_id'])
        except:
            company = None

        if company:
            try:
                company_logo = company.logo_image.url
            except:
                company_logo = None
    else:
        try:
            companyuser = CompanyUser.objects.get(user = request.user)
        except:
            companyuser = None

        if companyuser:
            company = companyuser.company
            try:
                company_logo = companyuser.company.logo_image.url
            except:
                company_logo = None

    coonboardingtypes = CoOnboardingType.objects.filter(is_deleted = False, company = company)


    if request.method == 'POST':
        applicant_id = int(request.POST['applicant_id'])
        co_onboarding_type = int(request.POST['onboarding_type'])
        job_id = request.POST['job_id']
        position_id = request.POST['position']
        hiring_manager_user = int(request.POST['hiring_manager_user'])

        my_request = MyRequest.objects.create(applicant_id = applicant_id, company = company,  co_onboarding_type_id = co_onboarding_type, job_id = job_id, position_id = position_id, hiring_manager_user= hiring_manager_user, recruiter = request.user, request_status=True, created_by = request.user)

        if my_request:
            task_ids = request.POST.getlist('task_id')

            for task_id in task_ids:
                task_id = int(task_id)
                try:
                    onboarding_task = CoOnboardingTask.objects.get(id = task_id)
                except:
                    onboarding_task = None

                myrequest_tasks_info = MyRequestTasksInfo.objects.create(myrequest = my_request, task_id = task_id, co_onboarding_type_id = co_onboarding_type, task_name = onboarding_task.task_name, vendor = onboarding_task.vendor,request_due_date = onboarding_task.due_date, company = company, step_id = onboarding_task.step_id, comments = onboarding_task.comment)

                # copy all onboarding step details in request step details
                if myrequest_tasks_info:
                    if onboarding_task.step_id == '1':
                        coonboardingtaskbgv = CoOnboardingTaskBGV.objects.filter(co_onboarding_task_id = task_id)
                        for taskbgv in coonboardingtaskbgv:
                            MyRequestTaskBGV.objects.create(myrequest_tasks_info = myrequest_tasks_info, document = taskbgv.document)
                    elif onboarding_task.step_id == '2':
                        coonboardingtaskref = CoOnboardingTaskRefCheck.objects.filter(onboarding_ref_task_id = task_id)
                        for taskref in coonboardingtaskref:
                            MyRequestTaskRefCheck.objects.create(myrequest_tasks_info = myrequest_tasks_info, reference_check = taskref.reference_check, no_of_references = taskref.no_of_references)
                    elif onboarding_task.step_id == '3':
                        coonboardingtaskhrform = CoOnboardingTaskHrForm.objects.filter(onboarding_hr_task_id = task_id)
                        for hrform in coonboardingtaskhrform:
                            MyRequestTaskHrForm.objects.create(myrequest_tasks_info = myrequest_tasks_info, template = hrform.template)
                    else:
                        return redirect('request-listing')

            return redirect('request-listing')

    return render(request, 'projectx_app/create-request.html', {"coonboardingtypes": coonboardingtypes, "applicant_id": id, "username": username})


class MyRequestUpdateView(LoginRequiredMixin, CompanyGeneric, generic.UpdateView):
    model = MyRequest
    form_class = MyRequestForm
    template_name = 'projectx_app/request-form.html'
    success_url = reverse_lazy('request-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        my_request = get_object_or_404(MyRequest, pk=self.kwargs['id'])
        return my_request


def update_request(request, id=None):
    company, company_logo, company_name = None, None, None
    myrequest_hr_task_update, myrequest_ref_task_update, myrequest_bgv_task_update = None, None, None

    if 'company_id' in request.session:
        try:
            company = SystemCompanySetup.objects.get(pk = request.session['company_id'])
        except:
            company = None

        if company:
            try:
                company_logo = company.logo_image.url
            except:
                company_logo = None
            try:
                company_name = company.company_name
            except:
                company_name = None
    else:
        try:
            companyuser = CompanyUser.objects.get(user = request.user)
        except:
            companyuser = None

        if companyuser:
            company = companyuser.company
            try:
                company_logo = companyuser.company.logo_image.url
            except:
                company_logo = None

            try:
                company_name = companyuser.company.company_name
            except:
                company_name = None

    document_types = DocumentType.objects.all()
    document_type_names = DocumentTypeName.objects.all()

    vendors = CompanyVendor.objects.filter(
        company = company, 
        user__user_type = 3,
    ).filter(~Q(sys_vendor_type__type_description = 'Medical')) # vendor admin type

    templates = Template.objects.filter(company = company)
    sysrefchecks = SysRefCheck.objects.all()

    cmo_users = CompanyUser.objects.filter(user__user_type = 7, company = company)
    medical_vendors = CompanyVendor.objects.filter(company = company, sys_vendor_type__type_description = 'Medical')

    # step 1 data
    try:
        my_request = MyRequest.objects.get(pk = id)
    except:
        my_request = None

    try:
        request_bgv_task = MyRequestTasksInfo.objects.get(step_id = 1, myrequest_id = id)
    except:
        request_bgv_task = None

    try:
        requesttaskbgv = MyRequestTaskBGV.objects.filter(myrequest_tasks_info_id = request_bgv_task.id)
    except:
        requesttaskbgv = None

    # step 2 data
    try:
        request_ref_task = MyRequestTasksInfo.objects.get(step_id = 2, myrequest_id = id)
    except:
        request_ref_task = None

    try:
        requesttaskref = MyRequestTaskRefCheck.objects.filter(myrequest_tasks_info_id = request_ref_task.id)
    except:
        requesttaskref = None

    # step 3 data
    try:
        request_hr_task = MyRequestTasksInfo.objects.get(step_id = 3, myrequest_id = id)
    except:
        request_hr_task = None

    try:
        requesttaskhr = MyRequestTaskHrForm.objects.filter(myrequest_tasks_info_id = request_hr_task.id)
    except:
        requesttaskhr = None

    # step 4 data
    try:
        request_medical_task = MyRequestTasksInfo.objects.get(step_id = 4, myrequest_id = id)
    except:
        request_medical_task = None

    try:
        requesttaskmedical = MyRequestTaskHrForm.objects.filter(myrequest_tasks_info_id = request_medical_task.id)
    except:
        requesttaskmedical = None


    if request.method == "POST":
        if 'save_for_step_1' in request.POST:
            #step 1
            bgv_due_date = request.POST.get('bgv_due_date')
            bgv_documents = request.POST.getlist('bgv_document')
            bgv_comment = request.POST.get('bgv_comment')
            bgv_vendor = request.POST.get('bgv_vendor')
            task_name_step_one = request.POST.get('task_name_step_one')

            # update
            if my_request and len(bgv_documents) > 0:
                try:
                    myrequest_bgv_task_update = MyRequestTasksInfo.objects.filter(step_id = 1, myrequest_id = id).update(task_name = task_name_step_one, vendor_id = bgv_vendor, comments = bgv_comment, request_due_date = bgv_due_date)
                except:
                    myrequest_bgv_task_update = None

                if myrequest_bgv_task_update == 0:
                    myrequest_bgv_task_update = MyRequestTasksInfo.objects.create(step_id = 1, myrequest_id = id, task_name = task_name_step_one, vendor_id = bgv_vendor, comments = bgv_comment, request_due_date = bgv_due_date, co_onboarding_type_id = my_request.co_onboarding_type.id, company = company, owner = request.user)

                    try:
                        request_bgv_task = MyRequestTasksInfo.objects.get(step_id = 1, myrequest_id = id)
                    except:
                        request_bgv_task = None

                # Create background verification task
                if myrequest_bgv_task_update:
                    try:
                        requesttaskbgv_delete = MyRequestTaskBGV.objects.filter(myrequest_tasks_info = request_bgv_task).delete()
                    except:
                        requesttaskbgv_delete = None

                    for document in bgv_documents:
                        MyRequestTaskBGV.objects.create(myrequest_tasks_info = request_bgv_task, document_id = document)

                    # if the applicant has submitted the task for step 1, then open the task again for him
                    MyRequestTasks.objects.filter(step_id = 1, myrequest_id = id).update(mark_complete = False)
            elif len(bgv_documents) == 0:
                try:
                    delete_myrequestbgvtask = MyRequestTasksInfo.objects.filter(step_id = 1, myrequest_id = id).delete()
                except:
                    delete_myrequestbgvtask = None

                try:
                    requesttaskbgvdelete = MyRequestTaskBGV.objects.filter(myrequest_tasks_info = request_bgv_task).delete()
                except:
                    requesttaskbgvdelete = None

        if 'save_for_step_2' in request.POST:
            ref_checks = request.POST.getlist('ref_check')
            ref_no_of_reference = request.POST.getlist('ref_no_of_reference')
            ref_due_date = request.POST.get('ref_due_date')
            ref_comment = request.POST.get('ref_comment')
            ref_vendor = request.POST.get('ref_vendor')
            task_name_step_two = request.POST.get('task_name_step_two')

            # Update            
            if my_request and len(ref_checks) > 0:
                try:
                    myrequest_ref_task_update = MyRequestTasksInfo.objects.filter(step_id = 2, myrequest_id = id).update(task_name = task_name_step_two, vendor_id = ref_vendor, comments = ref_comment, request_due_date = ref_due_date)
                except:
                    myrequest_ref_task_update = None

                if myrequest_ref_task_update == 0:
                    myrequest_ref_task_update = MyRequestTasksInfo.objects.create(step_id = 2, myrequest_id = id, task_name = task_name_step_two, vendor_id = ref_vendor, comments = ref_comment, request_due_date = ref_due_date, co_onboarding_type_id = my_request.co_onboarding_type.id, company = company, owner = request.user)

                    try:
                        request_ref_task = MyRequestTasksInfo.objects.get(step_id = 2, myrequest_id = id)
                    except:
                        request_ref_task = None

                # Reference Check
                if myrequest_ref_task_update:
                    try:
                        requesttaskref_delete = MyRequestTaskRefCheck.objects.filter(myrequest_tasks_info = request_ref_task).delete()
                    except:
                        requesttaskref_delete = None

                    ref = []
                    [ref.append(reference) for reference in ref_no_of_reference if reference != '']                    
                    for idx, ref_check in enumerate(ref_checks):
                        MyRequestTaskRefCheck.objects.create(myrequest_tasks_info = request_ref_task, reference_check_id = ref_check, no_of_references = ref[idx])

                    # if the applicant has submitted the task for step 2, then open the task again for him
                    MyRequestTasks.objects.filter(step_id = 2, myrequest_id = id).update(mark_complete = False)
            elif len(ref_checks) == 0:
                try:
                    delete_requesttaskref = MyRequestTasksInfo.objects.filter(step_id = 2, myrequest_id = id).delete()
                except:
                    delete_requesttaskref = None

                try:
                    requesttaskrefdelete = MyRequestTaskRefCheck.objects.filter(myrequest_tasks_info = request_ref_task).delete()
                except:
                    requesttaskrefdelete = None


        if 'save_for_step_3' in request.POST:
            hr_templates = request.POST.getlist('hr_template')
            hr_due_date = request.POST.get('hr_due_date')
            hr_vendor = request.POST.get('hr_vendor')
            hr_comment = request.POST.get('hr_comment')
            task_name_step_three = request.POST.get('task_name_step_three')

            if my_request and len(hr_templates) > 0:
                try:
                    myrequest_hr_task_update = MyRequestTasksInfo.objects.filter(step_id = 3, myrequest_id = id).update(task_name = task_name_step_three, vendor_id = hr_vendor, comments = hr_comment, request_due_date = hr_due_date)
                except:
                    myrequest_hr_task_update = None

                if myrequest_hr_task_update == 0:
                    myrequest_hr_task_update = MyRequestTasksInfo.objects.create(step_id = 3, myrequest_id = id, task_name = task_name_step_three, vendor_id = hr_vendor, comments = hr_comment, request_due_date = hr_due_date, co_onboarding_type_id = my_request.co_onboarding_type.id, company = company, owner = request.user)

                    try:
                        request_hr_task = MyRequestTasksInfo.objects.get(step_id = 3, myrequest_id = id)
                    except:
                        request_hr_task = None

                if myrequest_hr_task_update:
                    try:
                        coonboardingtaskhr = MyRequestTaskHrForm.objects.filter(myrequest_tasks_info = request_hr_task).delete()
                    except:
                        coonboardingtaskhr = None

                    for hr_template in hr_templates:
                        MyRequestTaskHrForm.objects.create(myrequest_tasks_info = request_hr_task, template_id = hr_template)
            elif len(hr_templates) == 0:
                try:
                    delete_requesttaskhr = MyRequestTasksInfo.objects.filter(step_id = 3, myrequest_id = id).delete()
                except:
                    delete_requesttaskhr = None

                try:
                    requesttaskhrdelete = MyRequestTaskHrForm.objects.filter(myrequest_tasks_info = request_hr_task).delete()
                except:
                    requesttaskhrdelete = None

                # if the applicant has submitted the task for step 3, then open the task again for him
                MyRequestTasks.objects.filter(step_id = 3, myrequest_id = id).update(mark_complete = False)

        if 'save_for_step_4' in request.POST:
            medical_templates = request.POST.getlist('medical_template')
            medical_vendor = request.POST.get('medical_vendor')
            medical_comment = request.POST.get('medical_comment')
            medical_due_date = request.POST.get('medical_due_date')
            medical_task_name_step_four = request.POST.get('medical_task_name_step_four')
            send_to_candidate = request.POST.get('send_to_candidate')

            if send_to_candidate == "on":
                send_to_candidate = True
            else:
                send_to_candidate = False

            if my_request and len(medical_templates) > 0:
                try:
                    myrequest_medical_task_update = MyRequestTasksInfo.objects.filter(step_id = 4, myrequest_id = id).update(task_name = medical_task_name_step_four, vendor_id = medical_vendor, comments = medical_comment, request_due_date = medical_due_date, send_to_candidate = send_to_candidate)
                except:
                    myrequest_medical_task_update = None

                if myrequest_medical_task_update == 0:
                    myrequest_medical_task_update = MyRequestTasksInfo.objects.create(step_id = 4, myrequest_id = id, task_name = medical_task_name_step_four, vendor_id = medical_vendor, comments = medical_comment,  co_onboarding_type_id = my_request.co_onboarding_type.id, request_due_date = medical_due_date, company = company, owner = request.user, send_to_candidate = send_to_candidate)

                    try:
                        request_medical_task = MyRequestTasksInfo.objects.get(step_id = 4, myrequest_id = id)
                    except:
                        request_medical_task = None

                if myrequest_medical_task_update:
                    try:
                        coonboardingtaskmedical = MyRequestTaskMedicalForm.objects.filter(myrequest_tasks_info = request_medical_task).delete()
                    except:
                        coonboardingtaskmedical = None

                    for medical_template in medical_templates:
                        MyRequestTaskMedicalForm.objects.create(myrequest_tasks_info = request_medical_task, template_id = medical_template)
            elif len(medical_templates) == 0:
                try:
                    delete_requesttaskmedical = MyRequestTasksInfo.objects.filter(step_id = 4, myrequest_id = id).delete()
                except:
                    delete_requesttaskmedical = None

                try:
                    requesttaskmedicaldelete = MyRequestTaskMedicalForm.objects.filter(myrequest_tasks_info = request_medical_task).delete()
                except:
                    requesttaskmedicaldelete = None

                # if the applicant has submitted the task for step 4, then open the task again for him
                MyRequestTasks.objects.filter(step_id = 4, myrequest_id = id).update(mark_complete = False)

            if send_to_candidate == True:
                try:
                    myrequest_medical_task_update = MyRequestTasksInfo.objects.filter(step_id = 4, myrequest_id = id).update(task_name = medical_task_name_step_four, send_to_candidate = send_to_candidate, comments = medical_comment, request_due_date = medical_due_date)
                except:
                    myrequest_medical_task_update = None

                if myrequest_medical_task_update == 0:
                    myrequest_medical_task_update = MyRequestTasksInfo.objects.create(step_id = 4, myrequest_id = id, task_name = medical_task_name_step_four, send_to_candidate = send_to_candidate, comments = medical_comment,  co_onboarding_type_id = my_request.co_onboarding_type.id, request_due_date = medical_due_date, company = company, owner = request.user)

                    try:
                        request_medical_task = MyRequestTasksInfo.objects.get(step_id = 4, myrequest_id = id)
                    except:
                        request_medical_task = None

            if medical_vendor != "":
                try:
                    myrequest_medical_task_update = MyRequestTasksInfo.objects.filter(step_id = 4, myrequest_id = id).update(task_name = medical_task_name_step_four, vendor_id = medical_vendor, comments = medical_comment, request_due_date = medical_due_date)
                except:
                    myrequest_medical_task_update = None

                if myrequest_medical_task_update == 0:
                    myrequest_medical_task_update = MyRequestTasksInfo.objects.create(step_id = 4, myrequest_id = id, task_name = medical_task_name_step_four, vendor_id = medical_vendor, comments = medical_comment,  co_onboarding_type_id = my_request.co_onboarding_type.id, request_due_date = medical_due_date, company = company, owner = request.user)

                    try:
                        request_medical_task = MyRequestTasksInfo.objects.get(step_id = 4, myrequest_id = id)
                    except:
                        request_medical_task = None

    # todo for getting the data after update
    try:
        request_bgv_task = MyRequestTasksInfo.objects.get(step_id = 1, myrequest_id = id)
    except:
        request_bgv_task = None

    try:
        requesttaskbgv = MyRequestTaskBGV.objects.filter(myrequest_tasks_info_id = request_bgv_task.id)
    except:
        requesttaskbgv = None

    # step 2 data
    try:
        request_ref_task = MyRequestTasksInfo.objects.get(step_id = 2, myrequest_id = id)
    except:
        request_ref_task = None

    try:
        requesttaskref = MyRequestTaskRefCheck.objects.filter(myrequest_tasks_info_id = request_ref_task.id)
    except:
        requesttaskref = None

    # step 3 data
    try:
        request_hr_task = MyRequestTasksInfo.objects.get(step_id = 3, myrequest_id = id)
    except:
        request_hr_task = None

    try:
        requesttaskhr = MyRequestTaskHrForm.objects.filter(myrequest_tasks_info_id = request_hr_task.id)
    except:
        requesttaskhr = None

    # step 4 data
    try:
        request_medical_task = MyRequestTasksInfo.objects.get(step_id = 4, myrequest_id = id)
    except:
        request_medical_task = None

    try:
        requesttaskmedical = MyRequestTaskMedicalForm.objects.filter(myrequest_tasks_info_id = request_medical_task.id)
    except:
        requesttaskmedical = None

    return render(request, 'projectx_app/update-request.html', { "document_types":document_types, "document_type_names": document_type_names, "vendors":vendors, "templates": templates, "sysrefchecks": sysrefchecks, "my_request": my_request, "requesttaskbgv": requesttaskbgv, "request_bgv_task": request_bgv_task, "request_ref_task": request_ref_task, "requesttaskref": requesttaskref, "request_hr_task": request_hr_task, "requesttaskhr": requesttaskhr, "request_medical_task": request_medical_task, "requesttaskmedical": requesttaskmedical, "cmo_users": cmo_users, "medical_vendors": medical_vendors })


def create_onboarding_request(request, applicant_id=None, onboarding_id=None):
    co_onboarding_bgv_task, coonboardings, company, company_logo, company_name = None, None, None, None, None
    is_step_one_sent, is_step_two_sent,  is_step_three_sent, is_step_four_sent = False, False, False, False
    coonboardingtype, co_onboarding_bgv_task, coonboardingtaskbgv, co_onboarding_ref_task, coonboardingtaskref, co_onboarding_hr_task, coonboardingtaskhr, my_request, co_onboarding_medical_task, coonboardingtaskmedical = None, None, None, None, None, None, None, None, None, None

    try:
        applicant = Applicant.objects.get(id = applicant_id)
    except:
        applicant = None

    try:
        myrequest = MyRequest.objects.filter(applicant_id = applicant_id).values_list('co_onboarding_type', flat=True)
    except:
        myrequest = None

    myrequest = list(myrequest)

    if 'company_id' in request.session:
        try:
            company = SystemCompanySetup.objects.get(pk = request.session['company_id'])
        except:
            company = None

        if company:
            try:
                company_logo = company.logo_image.url
            except:
                company_logo = None
            try:
                company_name = company.company_name
            except:
                company_name = None
    else:
        try:
            companyuser = CompanyUser.objects.get(user = request.user)
        except:
            companyuser = None

        if companyuser:
            company = companyuser.company
            try:
                company_logo = companyuser.company.logo_image.url
            except:
                company_logo = None

            try:
                company_name = companyuser.company.company_name
            except:
                company_name = None

    if onboarding_id == None:
        coonboardings = CoOnboardingType.objects.filter(
            ~Q(id__in = myrequest),
            company = company
        )
    else:
        if onboarding_id in myrequest:
            myrequest.remove(onboarding_id)
        coonboardings = CoOnboardingType.objects.filter(
            ~Q(id__in = myrequest),
            company = company
        )

    document_types = DocumentType.objects.all()
    document_type_names = DocumentTypeName.objects.all()

    vendors = CompanyVendor.objects.filter(
        company = company, 
        user__user_type = 3,
    ).filter(~Q(sys_vendor_type__type_description = 'Medical')) # vendor admin type
    
    templates = Template.objects.filter(company = company)
    sysrefchecks = SysRefCheck.objects.all()

    cmo_users = CompanyUser.objects.filter(user__user_type = 7, company = company)
    hiring_manager_users = CompanyUser.objects.filter(user__user_type = 8, company = company)
    medical_vendors = CompanyVendor.objects.filter(company = company, sys_vendor_type__type_description = 'Medical')

    if onboarding_id:

        # step 1 data
        try:
            coonboardingtype = CoOnboardingType.objects.get(pk = onboarding_id)
        except:
            coonboardingtype = None

        try:
            my_request = MyRequest.objects.get(applicant_id = applicant_id, co_onboarding_type_id = coonboardingtype.id)
        except:
            my_request = None
            
        try:
            co_onboarding_bgv_task = CoOnboardingTask.objects.get(step_id = 1, co_onboarding_type_id = onboarding_id)
        except:
            co_onboarding_bgv_task = None

        try:
            coonboardingtaskbgv = CoOnboardingTaskBGV.objects.filter(co_onboarding_task_id = co_onboarding_bgv_task.id)
        except:
            coonboardingtaskbgv = None

        # step 2 data
        try:
            co_onboarding_ref_task = CoOnboardingTask.objects.get(step_id = 2, co_onboarding_type_id = onboarding_id)
        except:
            co_onboarding_ref_task = None
        
        try:
            coonboardingtaskref = CoOnboardingTaskRefCheck.objects.filter(onboarding_ref_task_id = co_onboarding_ref_task.id)
        except:
            coonboardingtaskref = None

        # step 3 data
        try:
            co_onboarding_hr_task = CoOnboardingTask.objects.get(step_id = 3, co_onboarding_type_id = onboarding_id)
        except:
            co_onboarding_hr_task = None
        
        try:
            coonboardingtaskhr = CoOnboardingTaskHrForm.objects.filter(onboarding_hr_task = co_onboarding_hr_task.id)
        except:
            coonboardingtaskhr = None

        # step 4 data
        try:
            co_onboarding_medical_task = CoOnboardingTask.objects.get(step_id = 4, co_onboarding_type_id = onboarding_id)
        except:
            co_onboarding_medical_task = None

        try:
            coonboardingtaskmedical = CoOnboardingTaskMedicalForm.objects.filter(onboarding_medical_task = co_onboarding_medical_task.id)
        except:
            coonboardingtaskmedical = None

        if request.method == "POST":

            job_id = request.POST['job_id']
            position_id = request.POST['position']
            hiring_manager_user = int(request.POST['hiring_manager_user'])

            if my_request == None:
                my_request = MyRequest.objects.create(applicant_id = applicant_id, company = company,  co_onboarding_type_id = coonboardingtype.id, recruiter = request.user, request_status=True, created_by = request.user, job_id = job_id, position_id = position_id, hiring_manager_user_id= hiring_manager_user)

            if 'save_for_step_1' in request.POST:
                #step 1
                bgv_due_date = request.POST.get('bgv_due_date')
                bgv_documents = request.POST.getlist('bgv_document')
                bgv_comment = request.POST.get('bgv_comment')
                bgv_vendor = request.POST.get('bgv_vendor')
                task_name_step_one = request.POST.get('task_name_step_one')
                bgv_task_id = request.POST.get('bgv_task_id')
                bgv_company = request.POST.get('bgv_company')

                if my_request and len(bgv_documents) > 0:
                    try:
                        myrequest_bgv_task_create = MyRequestTasksInfo.objects.create(step_id = 1, myrequest_id = my_request.id, task_name = task_name_step_one, vendor_id = bgv_vendor, comments = bgv_comment, request_due_date = bgv_due_date, co_onboarding_type_id = coonboardingtype.id, company_id = bgv_company, task_id = bgv_task_id, owner = request.user)
                    except:
                        myrequest_bgv_task_create = None

                    for document in bgv_documents:
                        MyRequestTaskBGV.objects.create(myrequest_tasks_info = myrequest_bgv_task_create, document_id = document)

                    html_message = "Dear "+my_request.applicant.user.first_name+", <br><br>We are sending this email to inform you that "+my_request.company.company_name+" company has assigned onboarding tasks to you. <br><br>please check spam folder and mark project x in your contact if you do not find the email in your inbox.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                    email_message = EmailMessage('Onboarding Task Assigned', html_message, settings.EMAIL_HOST_USER, [],[my_request.applicant.user.email])
                    email_message.content_subtype = "html"
                    email_message.send()

                    messages.success(request, 'Background Verification Step is sent to the applicant.')

            if 'save_for_step_2' in request.POST:
                #step 2
                ref_checks = request.POST.getlist('ref_check')
                ref_no_of_reference = request.POST.getlist('ref_no_of_reference')
                ref_due_date = request.POST.get('ref_due_date')
                ref_comment = request.POST.get('ref_comment')
                ref_vendor = request.POST.get('ref_vendor')
                task_name_step_two = request.POST.get('task_name_step_two')
                ref_task_id = request.POST.get('ref_task_id')
                ref_company = request.POST.get('ref_company')

                if my_request and len(ref_no_of_reference) > 0:
                    try:
                        myrequest_ref_task_create = MyRequestTasksInfo.objects.create(step_id = 2, myrequest_id = my_request.id, task_name = task_name_step_two, vendor_id = ref_vendor, comments = ref_comment, request_due_date = ref_due_date, co_onboarding_type_id = coonboardingtype.id, task_id = ref_task_id, company_id = ref_company, owner = request.user)
                    except:
                        myrequest_ref_task_create = None

                    ref = []
                    [ref.append(reference) for reference in ref_no_of_reference if reference != '']

                    for idx, ref_check in enumerate(ref_checks):
                        MyRequestTaskRefCheck.objects.create(myrequest_tasks_info = myrequest_ref_task_create, reference_check_id = ref_check, no_of_references = ref[idx])

                    html_message = "Dear "+my_request.applicant.user.first_name+", <br><br>We are sending this email to inform you that "+my_request.company.company_name+" company has assigned onboarding tasks to you. <br><br>please check spam folder and mark project x in your contact if you do not find the email in your inbox.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                    email_message = EmailMessage('Onboarding Task Assigned', html_message, settings.EMAIL_HOST_USER, [],[my_request.applicant.user.email])
                    email_message.content_subtype = "html"
                    email_message.send()

                    messages.success(request, 'Reference Check Step is sent to the applicant.')

            if 'save_for_step_3' in request.POST:
                #step 3
                hr_templates = request.POST.getlist('hr_template')
                hr_due_date = request.POST.get('hr_due_date')
                hr_vendor = request.POST.get('hr_vendor')
                hr_comment = request.POST.get('hr_comment')
                task_name_step_three = request.POST.get('task_name_step_three')
                hr_task_id = request.POST.get('hr_task_id')
                hr_company = request.POST.get('hr_company')

                if my_request and len(hr_templates) > 0:
                    try:
                        myrequest_hr_task_create = MyRequestTasksInfo.objects.create(step_id = 3, myrequest_id = my_request.id, task_name = task_name_step_three, vendor_id = hr_vendor, co_onboarding_type_id = coonboardingtype.id, comments = hr_comment, request_due_date = hr_due_date, task_id = hr_task_id, company_id = hr_company, owner = request.user)
                    except:
                        myrequest_hr_task_create = None

                    for hr_template in hr_templates:
                        MyRequestTaskHrForm.objects.create(myrequest_tasks_info = myrequest_hr_task_create, template_id = hr_template)

                    html_message = "Dear "+my_request.applicant.user.first_name+", <br><br>We are sending this email to inform you that "+my_request.company.company_name+" company has assigned onboarding tasks to you. <br><br>please check spam folder and mark project x in your contact if you do not find the email in your inbox.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                    email_message = EmailMessage('Onboarding Task Assigned', html_message, settings.EMAIL_HOST_USER, [],[my_request.applicant.user.email])
                    email_message.content_subtype = "html"
                    email_message.send()

                    messages.success(request, 'Employment Forms Step is sent to the applicant.')

            if 'save_for_step_4' in request.POST:
                #step 4
                medical_templates = request.POST.getlist('medical_template')
                medical_due_date = request.POST.get('medical_due_date')
                medical_vendor = request.POST.get('medical_vendor')
                medical_task_name_step_four = request.POST.get('medical_task_name_step_four')
                medical_comment = request.POST.get('medical_comment')
                medical_task_id = request.POST.get('medical_task_id')
                medical_company = request.POST.get('medical_company')
                send_to_candidate = request.POST.get('send_to_candidate')
                medical_cmo_user = request.POST.get('medical_cmo_user')

                if send_to_candidate == "on":
                    send_to_candidate = True
                else:
                    send_to_candidate = False

                if my_request and len(medical_templates) > 0:
                    try:
                        myrequest_medical_task_create = MyRequestTasksInfo.objects.create(step_id = 4, myrequest_id = my_request.id, task_name = medical_task_name_step_four, vendor_id = medical_vendor, co_onboarding_type_id = coonboardingtype.id, comments = medical_comment, task_id = medical_task_id, company_id = medical_company, request_due_date = medical_due_date, owner = request.user, medical_cmo_user_id = medical_cmo_user, send_to_candidate = send_to_candidate)
                    except:
                        myrequest_medical_task_create = None

                    for medical_template in medical_templates:
                        MyRequestTaskMedicalForm.objects.create(myrequest_tasks_info = myrequest_medical_task_create, template_id = medical_template)

                    html_message = "Dear "+my_request.applicant.user.first_name+", <br><br>We are sending this email to inform you that "+my_request.company.company_name+" company has assigned onboarding tasks to you. <br><br>please check spam folder and mark project x in your contact if you do not find the email in your inbox.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                    email_message = EmailMessage('Onboarding Task Assigned', html_message, settings.EMAIL_HOST_USER, [],[my_request.applicant.user.email])
                    email_message.content_subtype = "html"
                    email_message.send()

                    messages.success(request, 'Medical Check Step is sent to the applicant.')
                elif send_to_candidate == True:                    
                    try:
                        myrequest_medical_task_create = MyRequestTasksInfo.objects.create(step_id = 4, myrequest_id = my_request.id, task_name = medical_task_name_step_four, send_to_candidate = send_to_candidate, co_onboarding_type_id = coonboardingtype.id, comments = medical_comment, task_id = medical_task_id, company_id = medical_company, request_due_date = medical_due_date, owner = request.user, medical_cmo_user_id = medical_cmo_user)
                    except:
                        myrequest_medical_task_create = None
                    
                    html_message = "Dear "+my_request.applicant.user.first_name+", <br><br>We are sending this email to inform you that "+my_request.company.company_name+" company has assigned onboarding tasks to you. <br><br>please check spam folder and mark project x in your contact if you do not find the email in your inbox.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                    email_message = EmailMessage('Onboarding Task Assigned', html_message, settings.EMAIL_HOST_USER, [],[my_request.applicant.user.email])
                    email_message.content_subtype = "html"
                    email_message.send()

                    messages.success(request, 'Medical Check Step is sent to the applicant.')
                elif medical_vendor != "":
                    try:
                        myrequest_medical_task_create = MyRequestTasksInfo.objects.create(step_id = 4, myrequest_id = my_request.id, task_name = medical_task_name_step_four, vendor_id = medical_vendor, co_onboarding_type_id = coonboardingtype.id, comments = medical_comment, task_id = medical_task_id, company_id = medical_company, request_due_date = medical_due_date, owner = request.user, medical_cmo_user_id = medical_cmo_user)
                    except:
                        myrequest_medical_task_create = None
                    
                    html_message = "Dear "+my_request.applicant.user.first_name+", <br><br>We are sending this email to inform you that "+my_request.company.company_name+" company has assigned onboarding tasks to you. <br><br>please check spam folder and mark project x in your contact if you do not find the email in your inbox.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                    email_message = EmailMessage('Onboarding Task Assigned', html_message, settings.EMAIL_HOST_USER, [],[my_request.applicant.user.email])
                    email_message.content_subtype = "html"
                    email_message.send()

                    messages.success(request, 'Medical Check Step is sent to the applicant.')

        myrequest_task_info_bgv = MyRequestTasksInfo.objects.filter(step_id = 1, myrequest__applicant_id = applicant_id,co_onboarding_type_id = coonboardingtype.id)

        if myrequest_task_info_bgv:
            is_step_one_sent = True

        myrequest_task_info_ref = MyRequestTasksInfo.objects.filter(step_id = 2, myrequest__applicant_id = applicant_id,co_onboarding_type_id = coonboardingtype.id)

        if myrequest_task_info_ref:
            is_step_two_sent = True

        myrequest_task_info_hr = MyRequestTasksInfo.objects.filter(step_id = 3, myrequest__applicant_id = applicant_id,co_onboarding_type_id = coonboardingtype.id)

        if myrequest_task_info_hr:
            is_step_three_sent = True

        myrequest_task_info_medical = MyRequestTasksInfo.objects.filter(step_id = 4, myrequest__applicant_id = applicant_id,co_onboarding_type_id = coonboardingtype.id)

        if myrequest_task_info_medical:
            is_step_four_sent = True


    return render(request, 'projectx_app/create-onboarding-request.html', { "my_request": my_request, "coonboardings": coonboardings, "applicant_id": applicant_id, "onboarding_id": onboarding_id, "document_types": document_types, "document_type_names": document_type_names, "vendors": vendors, "templates": templates, "sysrefchecks": sysrefchecks, "coonboardingtype": coonboardingtype, "co_onboarding_bgv_task": co_onboarding_bgv_task, "coonboardingtaskbgv": coonboardingtaskbgv, "co_onboarding_ref_task": co_onboarding_ref_task,  "coonboardingtaskref": coonboardingtaskref, "co_onboarding_hr_task": co_onboarding_hr_task,  "coonboardingtaskhr": coonboardingtaskhr, "co_onboarding_medical_task": co_onboarding_medical_task, "coonboardingtaskmedical": coonboardingtaskmedical, "applicant": applicant, "is_step_one_sent": is_step_one_sent, "is_step_two_sent": is_step_two_sent, "is_step_three_sent": is_step_three_sent, "is_step_four_sent": is_step_four_sent, "cmo_users": cmo_users, "company": company, "hiring_manager_users": hiring_manager_users, "medical_vendors": medical_vendors })
