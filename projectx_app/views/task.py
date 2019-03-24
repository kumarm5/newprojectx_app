from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.onboarding import *
from projectx_app.models.request import *
from projectx_app.models.task import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from datetime import timedelta
from projectx_app.views.generic import *


class MyTaskListView(LoginRequiredMixin, ApplicantGeneric, generic.ListView):
    template_name = 'projectx_app/task-list.html'
    model = MyRequest
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        try:
            applicant = Applicant.objects.get(user = self.request.user)
        except:
            applicant = None

        tasks = self.model.objects.filter(applicant=applicant)
        return tasks


def get_my_task(request, id=None):
    bgv_documents = []
    no_of_reference = []
    my_requested_tasks_count = 0
    profile_pic, personal_info, my_request, bgv_details, bgv_due_date, ref_details, ref_due_date, hr_details, hr_due_date, completed_task, hr_vendor_id, hr_task_name, hr_task_id, hr_step_id, ref_vendor_id, ref_task_name, ref_step_id, ref_task_id, bgv_vendor_id, bgv_task_name, bgv_step_id, bgv_task_id, bgv_myrequest_task, bgv_update, hr_myrequest_task, medical_due_date = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    myrequest_tasks_bgv_info, myrequest_tasks_ref_info, myrequest_tasks_hr_info = None, None, None
    medical_details, medical_task_id, medical_step_id, medical_vendor_id = None, None, None, None
    medical_task_name, medical_templates, medical_cmo_user, medical_vendor, medical_task_name_step_four, medical_comment, medical_task_id, medical_company, medical_send_to_candidate = None, None, None, None, None, None, None, None, None
    # task_count = MyRequestTasks.objects.filter(myrequest__applicant__user = request.user, mark_complete = False).count()

    try:
        personal_info = PersonalInfo.objects.get(user = request.user)
    except:
        personal_info = None


    if personal_info:
        profile_pic = personal_info.profile_pic.name

    try:
        my_request = MyRequest.objects.get(pk=id)
    except:
        my_request = None

    try:
        myrequest_tasks_bgv_info = MyRequestTasksInfo.objects.get(co_onboarding_type_id = my_request.co_onboarding_type.id, step_id = '1', myrequest__applicant__user_id = request.user.id)
    except:
        myrequest_tasks_bgv_info = None

    if myrequest_tasks_bgv_info:
        bgv_details = MyRequestTaskBGV.objects.filter(myrequest_tasks_info = myrequest_tasks_bgv_info)
        bgv_due_date = myrequest_tasks_bgv_info.created_at + timedelta(days=int(myrequest_tasks_bgv_info.request_due_date))
        bgv_task_id = myrequest_tasks_bgv_info.id
        bgv_step_id = myrequest_tasks_bgv_info.step_id
        bgv_task_name = myrequest_tasks_bgv_info.task_name
        bgv_vendor_id = myrequest_tasks_bgv_info.vendor_id


    try:
        myrequest_tasks_ref_info = MyRequestTasksInfo.objects.get(co_onboarding_type_id = my_request.co_onboarding_type.id, step_id = '2', myrequest__applicant__user_id = request.user.id)
    except:
        myrequest_tasks_ref_info = None

    if myrequest_tasks_ref_info:
        ref_details = MyRequestTaskRefCheck.objects.filter(myrequest_tasks_info = myrequest_tasks_ref_info)
        ref_due_date = myrequest_tasks_ref_info.created_at + timedelta(days=int(myrequest_tasks_ref_info.request_due_date))
        ref_task_id = myrequest_tasks_ref_info.id
        ref_step_id = myrequest_tasks_ref_info.step_id
        ref_task_name = myrequest_tasks_ref_info.task_name
        ref_vendor_id = myrequest_tasks_ref_info.vendor_id

    if ref_details:
        for ref_detail in ref_details:
            number_of_reference = []
            for i in range(0, int(ref_detail.no_of_references)):
                number_of_reference.append(i)
            no_of_reference.append(number_of_reference)

    try:
        myrequest_tasks_hr_info = MyRequestTasksInfo.objects.get(co_onboarding_type_id = my_request.co_onboarding_type.id, step_id = '3', myrequest__applicant__user_id = request.user.id)
    except:
        myrequest_tasks_hr_info = None

    if myrequest_tasks_hr_info:
        hr_details = MyRequestTaskHrForm.objects.filter(myrequest_tasks_info = myrequest_tasks_hr_info)
        hr_due_date = myrequest_tasks_hr_info.created_at + timedelta(days=int(myrequest_tasks_hr_info.request_due_date))
        hr_task_id = myrequest_tasks_hr_info.id
        hr_step_id = myrequest_tasks_hr_info.step_id
        hr_task_name = myrequest_tasks_hr_info.task_name
        hr_vendor_id = myrequest_tasks_hr_info.vendor_id

    try:
        myrequest_tasks_medical_info = MyRequestTasksInfo.objects.get(co_onboarding_type_id = my_request.co_onboarding_type.id, step_id = '4', myrequest__applicant__user_id = request.user.id)
    except:
        myrequest_tasks_medical_info = None

    if myrequest_tasks_medical_info:

        medical_details = MyRequestTaskMedicalForm.objects.filter(myrequest_tasks_info = myrequest_tasks_medical_info)
        medical_due_date = myrequest_tasks_medical_info.created_at + timedelta(days=int(myrequest_tasks_medical_info.request_due_date))
        medical_task_id = myrequest_tasks_medical_info.id
        medical_step_id = myrequest_tasks_medical_info.step_id
        medical_task_name = myrequest_tasks_medical_info.task_name
        medical_vendor_id = myrequest_tasks_medical_info.vendor_id
        medical_send_to_candidate = myrequest_tasks_medical_info.send_to_candidate

    #check if bgv my request task is already created or not
    try:
        bgv_myrequest_task = MyRequestTasks.objects.get(myrequest = my_request, task_id = bgv_task_id)
    except:
        bgv_myrequest_task = None

    #check if hr my request task is already created or not
    try:
        hr_myrequest_task = MyRequestTasks.objects.get(myrequest = my_request, task_id = hr_task_id)
    except:
        hr_myrequest_task = None

    #check if ref my request task is already created or not
    try:
        ref_myrequest_task = MyRequestTasks.objects.get(myrequest = my_request, task_id = ref_task_id)
    except:
        ref_myrequest_task = None

    #check if medical my request task is already created or not
    try:
        medical_myrequest_task = MyRequestTasks.objects.get(myrequest = my_request, task_id = medical_task_id)
    except:
        medical_myrequest_task = None

    if request.method == 'POST':
        # step 1
        # get the step 1 field values
        if 'bgv_step_id' in request.POST:
            bgv_step_id = int(request.POST['bgv_step_id'])
            bgvdue_date = request.POST['bgv_due_date']
            bgv_task_id = int(request.POST['bgv_task_id'])
            bgv_task_name = request.POST['bgv_task_name']
            bgv_vendor_id = int(request.POST['bgv_vendor'])
            bgv_document_ids = request.POST.getlist('bgv_document_id')
            bgv_files = request.FILES.getlist('bgv_file')
            bgv_mark_complete = request.POST.getlist('bgv_mark_complete_value')
            bgv_mark_applicable = request.POST.getlist('bgv_mark_applicable_value')
            bgv_update = request.POST['bgv_update']
            bgv_submit = request.POST['bgv_submit']

            file_list = request.POST.getlist('file_list')

            for index, filelist in enumerate(file_list):
                if filelist == 'False':
                    bgv_files.insert(index, None)

            #if my request task in not found then create my request task
            if bgv_myrequest_task is None:
                bgv_myrequest_task = MyRequestTasks.objects.create(myrequest = my_request, task_id = bgv_task_id, co_onboarding_type = my_request.co_onboarding_type, step_id = bgv_step_id, task_name = bgv_task_name, vendor_id = bgv_vendor_id, request_due_date = bgvdue_date, mark_complete = False)

            # create task
            if bgv_update == 'None':

                for index, mark_complete in enumerate(bgv_mark_complete):

                    if mark_complete == 'False':
                        mark_complete = False
                    else:
                        mark_complete = True

                    if bgv_mark_applicable[index] == 'False':
                        mark_applicable = False
                    else:
                        mark_applicable = True

                    try:
                        bgv_file = bgv_files[index]
                    except IndexError:
                        bgv_file = None

                    myrequest_task_bgv = MyRequestTasksBgvDocs.objects.create(myrequest_task = bgv_myrequest_task, document_id = int(bgv_document_ids[index]), document_file = bgv_file, mark_complete = mark_complete, not_applicable = mark_applicable)

                messages.success(request, 'You documents are saved successfully.')
            else:
                # update task
                for index, mark_complete in enumerate(bgv_mark_complete):

                    if mark_complete == 'False':
                        mark_complete = False
                    else:
                        mark_complete = True

                    if bgv_mark_applicable[index] == 'False':
                        mark_applicable = False
                    else:
                        mark_applicable = True

                    try:
                        bgv_file = bgv_files[index]
                    except IndexError:
                        bgv_file = None

                    if bgv_file is None:
                        myrequest_task_bgv = MyRequestTasksBgvDocs.objects.filter(myrequest_task = bgv_myrequest_task, document_id = int(bgv_document_ids[index])).update(mark_complete = mark_complete, not_applicable = mark_applicable)
                    else:
                        myrequest_task_bgv = MyRequestTasksBgvDocs.objects.filter(myrequest_task = bgv_myrequest_task, document_id = int(bgv_document_ids[index])).update(mark_complete = mark_complete, not_applicable = mark_applicable, document_file = bgv_file)

                messages.success(request, 'You documents are saved successfully.')

            if bgv_submit == 'True':
                bgv_myrequest_task.mark_complete = True
                bgv_myrequest_task.save()


        # step 2
        if 'ref_step_id' in request.POST:

            refdue_date = request.POST['ref_due_date']
            ref_step_id = int(request.POST['ref_step_id'])
            ref_task_id = int(request.POST['ref_task_id'])
            ref_task_name = request.POST['ref_task_name']
            ref_vendor_id = int(request.POST['ref_vendor'])
            ref_update = request.POST['ref_update']
            ref_submit = request.POST['ref_submit']

            ref_name = request.POST.getlist('ref_name')
            ref_organisation = request.POST.getlist('ref_organisation')
            ref_phone = request.POST.getlist('ref_phone')
            ref_office_email = request.POST.getlist('ref_office_email')
            ref_relation = request.POST.getlist('ref_relation')
            reference_id = request.POST.getlist('reference_id')

            ref_mark_complete = request.POST.getlist('ref_mark_complete_value')
            ref_mark_applicable = request.POST.getlist('ref_mark_applicable_value')

            if ref_myrequest_task is None:
                ref_myrequest_task = MyRequestTasks.objects.create(myrequest = my_request, task_id = ref_task_id, co_onboarding_type = my_request.co_onboarding_type, step_id = ref_step_id, task_name = ref_task_name, vendor_id = ref_vendor_id, request_due_date = refdue_date, mark_complete = False)

            # create task
            if ref_update == 'None':

                for index, ref in enumerate(ref_name):

                    if ref_mark_complete[index] == 'False':
                        mark_complete = False
                    else:
                        mark_complete = True

                    if ref_mark_applicable[index] == 'False':
                        mark_applicable = False
                    else:
                        mark_applicable = True

                    myrequest_task_ref = MyRequestTasksRefDocs.objects.create(myrequest_task = ref_myrequest_task,  reference_id = reference_id[index], mark_complete = mark_complete, ref_name = ref_name[index], ref_organisation = ref_organisation[index], ref_phone = ref_phone[index], ref_office_email = ref_office_email[index], ref_relation = ref_relation[index], not_applicable = mark_applicable, row_index = str(index))

                messages.success(request, 'Details are saved successfully.')
            else:
                # update
                for index, ref in enumerate(ref_name):

                    if ref_mark_complete[index] == 'False':
                        mark_complete = False
                    else:
                        mark_complete = True

                    if ref_mark_applicable[index] == 'False':
                        mark_applicable = False
                    else:
                        mark_applicable = True

                    myrequest_task_ref = MyRequestTasksRefDocs.objects.filter(myrequest_task = ref_myrequest_task, reference_id = reference_id[index], row_index = str(index)).update(mark_complete = mark_complete, ref_name = ref_name[index], ref_organisation = ref_organisation[index], ref_phone = ref_phone[index], ref_office_email = ref_office_email[index], ref_relation = ref_relation[index], not_applicable = mark_applicable)

                messages.success(request, 'Details are saved successfully.')

            if ref_submit == 'True':
                ref_myrequest_task.mark_complete = True
                ref_myrequest_task.save()

        #step 3
        if 'hr_step_id' in request.POST:

            hrdue_date = request.POST['hr_due_date']
            hr_step_id = int(request.POST['hr_step_id'])
            hr_task_id = int(request.POST['hr_task_id'])
            hr_task_name = request.POST['hr_task_name']
            hr_vendor_id = int(request.POST['hr_vendor'])
            hr_document_ids = request.POST.getlist('hr_document_id')
            hr_files = request.FILES.getlist('hr_file')

            hr_mark_complete = request.POST.getlist('hr_mark_complete_value')
            hr_mark_applicable = request.POST.getlist('hr_mark_applicable_value')
            hr_update = request.POST['hr_update']
            hr_submit = request.POST['hr_submit']

            file_list = request.POST.getlist('hr_file_list')

            for index, filelist in enumerate(file_list):
                if filelist == 'False':
                    hr_files.insert(index, None)
            

            #if my request task in not found then create my request task
            if hr_myrequest_task is None:
                hr_myrequest_task = MyRequestTasks.objects.create(myrequest = my_request, task_id = hr_task_id, co_onboarding_type = my_request.co_onboarding_type, step_id = hr_step_id, task_name = hr_task_name, vendor_id = hr_vendor_id, request_due_date = hrdue_date, mark_complete = False)


            # create task
            if hr_update == 'None':

                for index, mark_complete in enumerate(hr_mark_complete):

                    if mark_complete == 'False':
                        mark_complete = False
                    else:
                        mark_complete = True

                    if hr_mark_applicable[index] == 'False':
                        mark_applicable = False
                    else:
                        mark_applicable = True

                    try:
                        hr_file = hr_files[index]
                    except IndexError:
                        hr_file = None

                    myrequest_task_hr = MyRequestTasksHrDocs.objects.create(myrequest_task = hr_myrequest_task, template_id = hr_document_ids[index], document_name = hr_file, mark_complete = mark_complete, not_applicable = mark_applicable)

                messages.success(request, 'You documents are saved successfully.')
            else:
                #update task
                for index, mark_complete in enumerate(hr_mark_complete):

                    if mark_complete == 'False':
                        mark_complete = False
                    else:
                        mark_complete = True

                    if hr_mark_applicable[index] == 'False':
                        mark_applicable = False
                    else:
                        mark_applicable = True

                    try:
                        hr_file = hr_files[index]
                    except IndexError:
                        hr_file = None

                    if hr_file is None:
                        myrequest_task_hr = MyRequestTasksHrDocs.objects.filter(myrequest_task = hr_myrequest_task, template_id = int(hr_document_ids[index])).update(mark_complete = mark_complete, not_applicable = mark_applicable)
                    else:
                        myrequest_task_hr = MyRequestTasksHrDocs.objects.filter(myrequest_task = hr_myrequest_task, template_id = int(hr_document_ids[index])).update(mark_complete = mark_complete, not_applicable = mark_applicable, document_name = hr_file)

                messages.success(request, 'You documents are saved successfully.')

            if hr_submit == 'True':
                hr_myrequest_task.mark_complete = True
                hr_myrequest_task.save()


        #step 4
        if 'medical_step_id' in request.POST:
            medical_step_id = int(request.POST['medical_step_id'])
            medical_task_id = int(request.POST['medical_task_id'])
            medical_task_name = request.POST['medical_task_name']
            medicaldue_date = request.POST['medical_due_date']

            if request.POST['medical_vendor'] == 'None' or request.POST['medical_vendor'] == '':
                medical_vendor_id = ''
            else:
                medical_vendor_id = int(request.POST['medical_vendor'])

            medical_document_ids = request.POST.getlist('medical_document_id')
            medical_files = request.FILES.getlist('medical_file')            
            send_to_candidate = request.POST['send_to_candidate']

            if send_to_candidate == "True":
                send_to_candidate = True
            else:
                send_to_candidate = False

            medical_mark_complete = request.POST.getlist('medical_mark_complete_value')
            medical_mark_applicable = request.POST.getlist('medical_mark_applicable_value')
            medical_update = request.POST['medical_update']
            medical_submit = request.POST['medical_submit']

            file_list = request.POST.getlist('medical_file_list')

            for index, filelist in enumerate(file_list):
                if filelist == 'False':
                    medical_files.insert(index, None)

            #if my request task is not found then create my request task
            if medical_myrequest_task is None:
                if send_to_candidate == True:
                    medical_myrequest_task = MyRequestTasks.objects.create(myrequest = my_request, task_id = medical_task_id, co_onboarding_type = my_request.co_onboarding_type, step_id = medical_step_id, task_name = medical_task_name, send_to_candidate = send_to_candidate, mark_complete = False, request_due_date = medicaldue_date)
                else:
                    medical_myrequest_task = MyRequestTasks.objects.create(myrequest = my_request, task_id = medical_task_id, co_onboarding_type = my_request.co_onboarding_type, step_id = medical_step_id, task_name = medical_task_name, vendor_id = medical_vendor_id, mark_complete = False, request_due_date = medicaldue_date, send_to_candidate = send_to_candidate)
            
            # create task
            if medical_update == 'None':
                if send_to_candidate == True and len(medical_document_ids) == 0:
                    for medical_file in medical_files:
                        myrequest_task_medical = MyRequestTasksMedicalDocs.objects.create(myrequest_task = medical_myrequest_task, document_name = medical_file)

                    messages.success(request, 'You documents are saved successfully.')
                else:
                    for index, mark_complete in enumerate(medical_mark_complete):

                        if mark_complete == 'False':
                            mark_complete = False
                        else:
                            mark_complete = True

                        if medical_mark_applicable[index] == 'False':
                            mark_applicable = False
                        else:
                            mark_applicable = True

                        try:
                            medical_file = medical_files[index]
                        except IndexError:
                            medical_file = None

                        myrequest_task_medical = MyRequestTasksMedicalDocs.objects.create(myrequest_task = medical_myrequest_task, template_id = medical_document_ids[index], document_name = medical_file, mark_complete = mark_complete, not_applicable = mark_applicable)

                messages.success(request, 'You documents are saved successfully.')
            else:
                #update task
                if send_to_candidate == True and len(medical_document_ids) == 0:
                    for medical_file in medical_files:
                        myrequest_task_medical = MyRequestTasksMedicalDocs.objects.create(myrequest_task = medical_myrequest_task, document_name = medical_file)

                    messages.success(request, 'You documents are saved successfully.')
                else:
                    for index, mark_complete in enumerate(medical_mark_complete):

                        if mark_complete == 'False':
                            mark_complete = False
                        else:
                            mark_complete = True

                        if medical_mark_applicable[index] == 'False':
                            mark_applicable = False
                        else:
                            mark_applicable = True

                        try:
                            medical_file = medical_files[index]
                        except IndexError:
                            medical_file = None

                        if medical_file is None:
                            myrequest_task_medical = MyRequestTasksMedicalDocs.objects.filter(myrequest_task = medical_myrequest_task, template_id = int(medical_document_ids[index])).update(mark_complete = mark_complete, not_applicable = mark_applicable)
                        else:
                            myrequest_task_medical = MyRequestTasksMedicalDocs.objects.filter(myrequest_task = medical_myrequest_task, template_id = int(medical_document_ids[index])).update(mark_complete = mark_complete, not_applicable = mark_applicable, document_name = medical_file)

                    messages.success(request, 'You documents are saved successfully.')

            if medical_submit == 'True':
                medical_myrequest_task.mark_complete = True
                medical_myrequest_task.save()

    
    try:
        candidate_medical_files = MyRequestTasksMedicalDocs.objects.filter(myrequest_task_id = medical_myrequest_task)
    except:
        candidate_medical_files = None

    completed_task = MyRequestTasks.objects.filter(myrequest = my_request, mark_complete = True).values_list('task_id', flat=True)

    # get the total task from the request task table for the applicant
    try:
        my_requested_tasks = MyRequestTasksInfo.objects.filter(myrequest__applicant__user = request.user)
    except:
        my_requested_tasks = None

    if my_requested_tasks:
        my_requested_tasks_count = my_requested_tasks.count()

        for my_request in my_requested_tasks:
            try:
                mark_complete_count = MyRequestTasks.objects.get(myrequest = my_request.myrequest, step_id = my_request.step_id, mark_complete = True)
            except:
                mark_complete_count = None

            if mark_complete_count:
                my_requested_tasks_count = my_requested_tasks_count - 1

    return render(request, 'projectx_app/my-task-form.html', {"profile_pic": profile_pic, "my_request": my_request, "ref_details": ref_details, "hr_details": hr_details, "bgv_details": bgv_details, "bgv_due_date": bgv_due_date, "ref_due_date": ref_due_date, "hr_due_date": hr_due_date, "bgv_task_id": bgv_task_id, "bgv_step_id": bgv_step_id, "bgv_task_name": bgv_task_name, "bgv_vendor_id": bgv_vendor_id, "ref_task_id": ref_task_id, "ref_step_id": ref_step_id, "ref_task_name": ref_task_name, "ref_vendor_id": ref_vendor_id, "completed_task": completed_task, "hr_step_id": hr_step_id, "hr_task_id": hr_task_id, "hr_task_name": hr_task_name, "hr_vendor_id": hr_vendor_id, "bgv_myrequest_task": bgv_myrequest_task, "hr_myrequest_task": hr_myrequest_task, "ref_myrequest_task": ref_myrequest_task,"no_of_reference": no_of_reference, "open_task": my_requested_tasks_count, "myrequest_tasks_bgv_info": myrequest_tasks_bgv_info, "myrequest_tasks_ref_info": myrequest_tasks_ref_info, "myrequest_tasks_hr_info": myrequest_tasks_hr_info, "myrequest_tasks_medical_info": myrequest_tasks_medical_info, "medical_details": medical_details, "medical_step_id": medical_step_id, "medical_myrequest_task": medical_myrequest_task, "medical_task_id": medical_task_id, "medical_task_name": medical_task_name, "medical_vendor_id": medical_vendor_id, "medical_due_date": medical_due_date, "medical_send_to_candidate": medical_send_to_candidate, "candidate_medical_files": candidate_medical_files, "personal_info": personal_info })
