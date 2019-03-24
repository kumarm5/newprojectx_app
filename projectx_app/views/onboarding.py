from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.onboarding import *
from projectx_app.views.generic import *
from projectx_app.models.user_detail import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q


class CoOnboardingTypeView(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    model = CoOnboardingType
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        company = None

        if 'company_id' in self.request.session:
            try:
                company = SystemCompanySetup.objects.get(pk = self.request.session['company_id'])
            except:
                company = None
        else:
            try:
                companyuser = CompanyUser.objects.get(user = self.request.user)
            except:
                companyuser = None

            if companyuser:
                company = companyuser.company

        onboarding_types = self.model.objects.filter(is_deleted=False, company = company)
        return onboarding_types


class RpoCoOnboardingTypeView(LoginRequiredMixin, generic.ListView):
    model = CoOnboardingType
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        company = None

        getDetails = SysRpo.objects.get(user_id=self.request.user)
        getUsers = SystemCompanySetup.objects.filter(rpo=getDetails)
        company = []
        for CUsers in getUsers:
            try:
                companyuser = CompanyUser.objects.get(company=CUsers)
            except:
                companyuser = None

            if companyuser:
                company.append(companyuser.company)

        onboarding_types = self.model.objects.filter(is_deleted=False, company__in=company)
        return onboarding_types

def delete_onboarding_info(request, onboarding_id=None):
    '''
        This function is used to delete onboarding.
    '''
    try:
        delete_applicant = CoOnboardingType.objects.filter(pk = int(onboarding_id)).update(is_deleted = True)
    except:
        delete_applicant = None

    if delete_applicant:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


def create_onboarding_steps(request):
    company, company_name, company_logo, cmo_users = None, None, None, None
    
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

    cmo_users = CompanyUser.objects.filter(user__user_type = 7, company = company)
    medical_vendors = CompanyVendor.objects.filter(company = company, sys_vendor_type__type_description = 'Medical')

    document_types = DocumentType.objects.all()
    document_type_names = DocumentTypeName.objects.all()    

    vendors = CompanyVendor.objects.filter(
        company = company, 
        user__user_type = 3,
    ).filter(~Q(sys_vendor_type__type_description = 'Medical')) # vendor admin type

    templates = Template.objects.filter(company = company)
    sysrefchecks = SysRefCheck.objects.all()

    if request.method == 'POST':        
        #step 1
        boarding_type_name = request.POST.get('boarding_type_name')
        bgv_due_date = request.POST.get('bgv_due_date')
        bgv_documents = request.POST.getlist('bgv_document')
        bgv_comment = request.POST.get('bgv_comment')
        bgv_vendor = request.POST.get('bgv_vendor')
        task_name_step_one = request.POST.get('task_name_step_one')

        # create onboarding type
        if boarding_type_name != '':
            co_onboarding_type = CoOnboardingType.objects.create(co_onboarding_type_name = boarding_type_name, company = company)
        else:
            co_onboarding_type = None

        #Create CoOnboardingTask
        if co_onboarding_type and len(bgv_documents) > 0:
            co_onboarding_bgv_task = CoOnboardingTask.objects.create(step_id = 1, task_name = task_name_step_one, vendor_id = bgv_vendor, co_onboarding_type = co_onboarding_type, comment = bgv_comment, due_date = bgv_due_date)

            # Create background verification task
            if co_onboarding_bgv_task:
                for document in bgv_documents:
                    CoOnboardingTaskBGV.objects.create(co_onboarding_task = co_onboarding_bgv_task, document_id = document)


        #step 2
        ref_checks = request.POST.getlist('ref_check')
        ref_no_of_reference = request.POST.getlist('ref_no_of_reference')
        ref_due_date = request.POST.get('ref_due_date')
        ref_comment = request.POST.get('ref_comment')
        ref_vendor = request.POST.get('ref_vendor')
        task_name_step_two = request.POST.get('task_name_step_two')

        #Create CoOnboardingTask
        if co_onboarding_type and len(ref_no_of_reference) > 0:
            co_onboarding_ref_task = CoOnboardingTask.objects.create(step_id = 2, task_name = task_name_step_two, vendor_id = ref_vendor, co_onboarding_type = co_onboarding_type, comment = ref_comment, due_date = ref_due_date)

            ref = []
            [ref.append(reference) for reference in ref_no_of_reference if reference != '']

            #Create CoOnboarding ref Task
            if co_onboarding_ref_task:
                for idx, ref_check in enumerate(ref_checks):
                    CoOnboardingTaskRefCheck.objects.create(onboarding_ref_task = co_onboarding_ref_task, reference_check_id = ref_check, no_of_references = ref[idx])

        #step 3
        hr_templates = request.POST.getlist('hr_template')
        hr_due_date = request.POST.get('hr_due_date')
        hr_vendor = request.POST.get('hr_vendor')
        hr_comment = request.POST.get('hr_comment')
        task_name_step_three = request.POST.get('task_name_step_three')

        #Create CoOnboardingTask
        if co_onboarding_type and len(hr_templates) > 0:
            co_onboarding_hr_task = CoOnboardingTask.objects.create(step_id = 3, task_name = task_name_step_three, vendor_id = hr_vendor, co_onboarding_type = co_onboarding_type, comment = hr_comment, due_date = hr_due_date)

            #Create CoOnboarding Hr Task
            if co_onboarding_hr_task:
                for hr_template in hr_templates:
                    CoOnboardingTaskHrForm.objects.create(onboarding_hr_task = co_onboarding_hr_task, template_id = hr_template)

             # if co_onboarding_hr_task:
                # messages.success(request, 'On-Boarding Steps Saved Successfully.')
                # return redirect('onboarding-listing')

        #step 4
        medical_templates = request.POST.getlist('medical_template')
        medical_due_date = request.POST.get('medical_due_date')
        medical_vendor = request.POST.get('medical_vendor')
        medical_task_name_step_four = request.POST.get('medical_task_name_step_four')
        medical_comment = request.POST.get('medical_comment')
        send_to_candidate = request.POST.get('send_to_candidate')

        # get the medical company user
        try:
            medical_cmo_user = CompanyUser.objects.filter(user__user_type = 7, company = company).last()
        except:
            medical_cmo_user = None

        if send_to_candidate == "on":
            send_to_candidate = True
        else:
            send_to_candidate = False

        if co_onboarding_type and len(medical_templates) > 0:
            co_onboarding_medical_task = CoOnboardingTask.objects.create(step_id = 4, task_name = medical_task_name_step_four, vendor_id = medical_vendor, send_to_candidate = send_to_candidate, co_onboarding_type = co_onboarding_type, comment = medical_comment, due_date = medical_due_date, medical_cmo_user_id = medical_cmo_user.id)

            if co_onboarding_medical_task:
                for medical_template in medical_templates:
                    CoOnboardingTaskMedicalForm.objects.create(onboarding_medical_task = co_onboarding_medical_task, template_id = medical_template)
        elif send_to_candidate == True:
            co_onboarding_medical_task = CoOnboardingTask.objects.create(step_id = 4, task_name = medical_task_name_step_four, co_onboarding_type = co_onboarding_type, comment = medical_comment, due_date = medical_due_date, send_to_candidate = send_to_candidate, medical_cmo_user_id = medical_cmo_user.id)
        elif medical_vendor != "":
            co_onboarding_medical_task = CoOnboardingTask.objects.create(step_id = 4, task_name = medical_task_name_step_four, vendor_id = medical_vendor, co_onboarding_type = co_onboarding_type, comment = medical_comment, due_date = medical_due_date, medical_cmo_user_id = medical_cmo_user.id)

        return redirect('onboarding-listing')

    return render(request, 'projectx_app/create-onboarding.html', {"document_types":document_types, "document_type_names": document_type_names, "vendors":vendors, "templates": templates, "sysrefchecks": sysrefchecks, "company_logo": company_logo, "company_name": company_name, "cmo_users": cmo_users, "medical_vendors": medical_vendors })


def edit_onboarding_steps(request, id=None):
    company, company_logo, company_name, cmo_users = None, None, None, None


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
        coonboardingtype = CoOnboardingType.objects.get(pk = id)
    except:
        coonboardingtype = None

    try:
        co_onboarding_bgv_task = CoOnboardingTask.objects.get(step_id = 1, co_onboarding_type_id = id)
    except:
        co_onboarding_bgv_task = None

    try:
        coonboardingtaskbgv = CoOnboardingTaskBGV.objects.filter(co_onboarding_task_id = co_onboarding_bgv_task.id)
    except:
        coonboardingtaskbgv = None

    # step 2 data
    try:
        co_onboarding_ref_task = CoOnboardingTask.objects.get(step_id = 2, co_onboarding_type_id = id)
    except:
        co_onboarding_ref_task = None

    try:
        coonboardingtaskref = CoOnboardingTaskRefCheck.objects.filter(onboarding_ref_task_id = co_onboarding_ref_task.id)
    except:
        coonboardingtaskref = None

    # step 3 data
    try:
        co_onboarding_hr_task = CoOnboardingTask.objects.get(step_id = 3, co_onboarding_type_id = id)
    except:
        co_onboarding_hr_task = None

    try:                
        coonboardingtaskhr = CoOnboardingTaskHrForm.objects.filter(onboarding_hr_task = co_onboarding_hr_task.id)
    except:
        coonboardingtaskhr = None

    # step 4 data
    try:
        co_onboarding_medical_task = CoOnboardingTask.objects.get(step_id = 4, co_onboarding_type_id = id)
    except:
        co_onboarding_medical_task = None

    try:
        coonboardingtaskmedical = CoOnboardingTaskMedicalForm.objects.filter(onboarding_medical_task = co_onboarding_medical_task.id)
    except:
        coonboardingtaskmedical = None


    if request.method == "POST":
        #step 1
        boarding_type_name = request.POST.get('boarding_type_name')
        bgv_due_date = request.POST.get('bgv_due_date')
        bgv_documents = request.POST.getlist('bgv_document')
        bgv_comment = request.POST.get('bgv_comment')
        bgv_vendor = request.POST.get('bgv_vendor')
        task_name_step_one = request.POST.get('task_name_step_one')

        # update
        try:
            coonboardingtype_update = CoOnboardingType.objects.filter(pk = id).update(co_onboarding_type_name = boarding_type_name)
        except:
            coonboardingtype_update = None

        # Create CoOnboardingTask
        if coonboardingtype_update and len(bgv_documents) > 0:
            co_onboarding_bgv_task_update = CoOnboardingTask.objects.filter(step_id = 1, co_onboarding_type_id = id).update(task_name = task_name_step_one, vendor_id = bgv_vendor, comment = bgv_comment, due_date = bgv_due_date)

            if co_onboarding_bgv_task_update == 0:
                co_onboarding_bgv_task_update = CoOnboardingTask.objects.create(task_name = task_name_step_one, vendor_id = bgv_vendor, comment = bgv_comment, due_date = bgv_due_date, step_id = 1, co_onboarding_type_id = id)

                try:
                    co_onboarding_bgv_task = CoOnboardingTask.objects.get(step_id = 1, co_onboarding_type_id = id)
                except:
                    co_onboarding_bgv_task = None

            # Create background verification task
            if co_onboarding_bgv_task_update:
                try:
                    coonboardingtaskbgv_delete = CoOnboardingTaskBGV.objects.filter(co_onboarding_task = co_onboarding_bgv_task).delete()
                except:
                    coonboardingtaskbgv_delete = None

                for document in bgv_documents:
                    CoOnboardingTaskBGV.objects.create(co_onboarding_task = co_onboarding_bgv_task, document_id = document)


        #step 2
        ref_checks = request.POST.getlist('ref_check')
        ref_no_of_reference = request.POST.getlist('ref_no_of_reference')
        ref_due_date = request.POST.get('ref_due_date')
        ref_comment = request.POST.get('ref_comment')
        ref_vendor = request.POST.get('ref_vendor')
        task_name_step_two = request.POST.get('task_name_step_two')


        #Create CoOnboardingTask
        if coonboardingtype_update and len(ref_no_of_reference) > 0:
            co_onboarding_ref_task_update = CoOnboardingTask.objects.filter(step_id = 2, co_onboarding_type_id = id).update(task_name = task_name_step_two, vendor_id = ref_vendor, comment = ref_comment, due_date = ref_due_date)

            if co_onboarding_ref_task_update == 0:
                co_onboarding_ref_task_update = CoOnboardingTask.objects.create(task_name = task_name_step_two, vendor_id = ref_vendor, comment = ref_comment, due_date = ref_due_date, step_id = 2, co_onboarding_type_id = id)

                try:
                    co_onboarding_ref_task = CoOnboardingTask.objects.get(step_id = 2, co_onboarding_type_id = id)
                except:
                    co_onboarding_ref_task = None

            #Create CoOnboarding ref Task
            if co_onboarding_ref_task_update:

                try:
                    coonboardingtaskref_delete = CoOnboardingTaskRefCheck.objects.filter(onboarding_ref_task = co_onboarding_ref_task).delete()
                except:
                    coonboardingtaskref_delete = None

                ref = []
                [ref.append(reference) for reference in ref_no_of_reference if reference != '']

                for idx, ref_check in enumerate(ref_checks):
                    CoOnboardingTaskRefCheck.objects.create(onboarding_ref_task = co_onboarding_ref_task, reference_check_id = ref_check, no_of_references = ref[idx])


        #step 3
        hr_templates = request.POST.getlist('hr_template')
        hr_due_date = request.POST.get('hr_due_date')
        hr_vendor = request.POST.get('hr_vendor')
        hr_comment = request.POST.get('hr_comment')
        task_name_step_three = request.POST.get('task_name_step_three')

        if coonboardingtype_update and len(hr_templates) > 0:
            co_onboarding_hr_task_update = CoOnboardingTask.objects.filter(step_id = 3, co_onboarding_type_id = id).update(task_name = task_name_step_three, vendor_id = hr_vendor, comment = hr_comment, due_date = hr_due_date)

            if co_onboarding_hr_task_update == 0:
                co_onboarding_hr_task_update = CoOnboardingTask.objects.create(task_name = task_name_step_three, vendor_id = hr_vendor, comment = hr_comment, due_date = hr_due_date, step_id = 3, co_onboarding_type_id = id)

                try:
                    co_onboarding_hr_task = CoOnboardingTask.objects.get(step_id = 3, co_onboarding_type_id = id)
                except:
                    co_onboarding_hr_task = None

            if co_onboarding_hr_task_update:
                try:
                    coonboardingtaskhr = CoOnboardingTaskHrForm.objects.filter(onboarding_hr_task = co_onboarding_hr_task).delete()
                except:
                    coonboardingtaskhr = None

                for hr_template in hr_templates:
                    CoOnboardingTaskHrForm.objects.create(onboarding_hr_task = co_onboarding_hr_task, template_id = hr_template)

        #step 4
        medical_templates = request.POST.getlist('medical_template')
        medical_due_date = request.POST.get('medical_due_date')
        medical_vendor = request.POST.get('medical_vendor')
        medical_task_name_step_four = request.POST.get('medical_task_name_step_four')
        medical_comment = request.POST.get('medical_comment')
        send_to_candidate = request.POST.get('send_to_candidate')

        # get the medical company user
        try:
            medical_cmo_user = CompanyUser.objects.filter(user__user_type = 7, company = company).last()
        except:
            medical_cmo_user = None

        if send_to_candidate == "on":
            send_to_candidate = True
        else:
            send_to_candidate = False

        if coonboardingtype_update and len(medical_templates) > 0:
            co_onboarding_medical_task_update = CoOnboardingTask.objects.filter(step_id = 4, co_onboarding_type_id = id).update(task_name = medical_task_name_step_four, vendor_id = medical_vendor, comment = medical_comment, due_date = medical_due_date, send_to_candidate = send_to_candidate)

            if co_onboarding_medical_task_update == 0:
                co_onboarding_medical_task_update = CoOnboardingTask.objects.create(task_name = medical_task_name_step_four, vendor_id = medical_vendor, comment = medical_comment, due_date = medical_due_date, step_id = 4, co_onboarding_type_id = id, medical_cmo_user_id = medical_cmo_user.id, send_to_candidate = send_to_candidate)

                try:
                    co_onboarding_medical_task = CoOnboardingTask.objects.get(step_id = 4, co_onboarding_type_id = id)
                except:
                    co_onboarding_medical_task = None

            if co_onboarding_medical_task_update:
                try:
                    coonboardingtaskmedical = CoOnboardingTaskMedicalForm.objects.filter(onboarding_medical_task = co_onboarding_medical_task).delete()
                except:
                    coonboardingtaskmedical = None

                for medical_template in medical_templates:
                    CoOnboardingTaskMedicalForm.objects.create(onboarding_medical_task = co_onboarding_medical_task, template_id = medical_template)
        elif send_to_candidate == True:
            co_onboarding_medical_task_update = CoOnboardingTask.objects.filter(step_id = 4, co_onboarding_type_id = id).update(task_name = medical_task_name_step_four, send_to_candidate = send_to_candidate, comment = medical_comment, due_date = medical_due_date)

            if co_onboarding_medical_task_update == 0:
                co_onboarding_medical_task_update = CoOnboardingTask.objects.create(task_name = medical_task_name_step_four, send_to_candidate = send_to_candidate, comment = medical_comment, due_date = medical_due_date, step_id = 4, co_onboarding_type_id = id, medical_cmo_user_id = medical_cmo_user.id)

                try:
                    co_onboarding_medical_task = CoOnboardingTask.objects.get(step_id = 4, co_onboarding_type_id = id)
                except:
                    co_onboarding_medical_task = None
        elif medical_vendor != "":
            co_onboarding_medical_task_update = CoOnboardingTask.objects.filter(step_id = 4, co_onboarding_type_id = id).update(task_name = medical_task_name_step_four, vendor_id = medical_vendor, comment = medical_comment, due_date = medical_due_date)

            if co_onboarding_medical_task_update == 0:
                co_onboarding_medical_task_update = CoOnboardingTask.objects.create(task_name = medical_task_name_step_four, vendor_id = medical_vendor, comment = medical_comment, due_date = medical_due_date, step_id = 4, co_onboarding_type_id = id, medical_cmo_user_id = medical_cmo_user.id)

                try:
                    co_onboarding_medical_task = CoOnboardingTask.objects.get(step_id = 4, co_onboarding_type_id = id)
                except:
                    co_onboarding_medical_task = None


        return redirect('onboarding-listing')

    return render(request, 'projectx_app/edit-onboarding.html', {"document_types":document_types, "document_type_names": document_type_names, "vendors":vendors, "templates": templates, "sysrefchecks": sysrefchecks, "coonboardingtype": coonboardingtype,"co_onboarding_bgv_task":co_onboarding_bgv_task,"coonboardingtaskbgv":coonboardingtaskbgv, "co_onboarding_ref_task": co_onboarding_ref_task, "coonboardingtaskref": coonboardingtaskref, "co_onboarding_hr_task": co_onboarding_hr_task, "coonboardingtaskhr":coonboardingtaskhr, "co_onboarding_medical_task": co_onboarding_medical_task, "coonboardingtaskmedical": coonboardingtaskmedical, "company_logo": company_logo, "company_name": company_name, "cmo_users": cmo_users, "medical_vendors": medical_vendors })

