from django import template
from projectx_app.models.task import *
from projectx_app.models.request import *
from projectx_app.models.onboarding import *
from projectx_app.models.reimbursement import *
from projectx_app.models.travel_booking import *
from django.db.models import Count

register = template.Library()

def bgv_ischecked(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.document_id:
                return 'checked'
    return ''


def ref_ischecked(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.reference_check_id:
                return 'checked'
    return ''


def hr_ischecked(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.template_id:
                return 'checked'
    return ''


def medical_ischecked(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.template_id:
                return 'checked'
    return ''


def is_requested(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.applicant_id:
                return 'disabled'
    return ''

def is_requested_button(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.applicant_id:
                return 'btn btn-sm'
    return 'btn btn-sm btn-success'

def ref_no_reference(value, arg):
    if arg:
        for arguement in arg:
            if value == arguement.reference_check_id:
                return arguement.no_of_references
    return ''


def document_file_name(value):
    value = str(value)
    result_str = value
    if 'document_files/' in value:
        result_str = value.replace('document_files/','')
    elif 'resume/' in value:
        result_str = value.replace('resume/','')
    return result_str


def step_one_status(value):
    try:
        requested_task = MyRequestTasksInfo.objects.get(myrequest_id = value, step_id = '1')
    except:
        requested_task = None

    try:
        myrequesttask = MyRequestTasks.objects.get(myrequest_id = value, step_id = '1')
    except:
        myrequesttask = None

    if requested_task:
        if requested_task.hiring_manager_status:
            if requested_task.hiring_manager_status == 'Approve':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-hiring_manager_comment="'+str(requested_task.hiring_manager_comment)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
            else:
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-hiring_manager_comment="'+str(requested_task.hiring_manager_comment)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        elif requested_task.progress_status:
            if requested_task.progress_status == 'Assigned':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-blue not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'In Progress':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'Completed':
                if requested_task.result == 'All Clear':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
                elif requested_task.result == 'Request can not be processed':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Document Requested again':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Failed':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        else:
            if myrequesttask:
                if myrequesttask.mark_complete == False:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'                    
                else:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Completed</a>'
            else:
                return '<u><i><a href="javascript:void();" class="not-complete" \
                data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'
    else:
        return 'NA'


def step_two_status(value):
    try:
        requested_task = MyRequestTasksInfo.objects.get(myrequest_id = value, step_id = '2')
    except:
        requested_task = None

    try:
        myrequesttask = MyRequestTasks.objects.get(myrequest_id = value, step_id = '2')
    except:
        myrequesttask = None

    if requested_task:
        if requested_task.hiring_manager_status:
            if requested_task.hiring_manager_status == 'Approve':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-hiring_manager_comment="'+str(requested_task.hiring_manager_comment)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
            else:
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-hiring_manager_comment="'+str(requested_task.hiring_manager_comment)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        elif requested_task.progress_status:
            if requested_task.progress_status == 'Assigned':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-blue not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'In Progress':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'Completed':
                if requested_task.result == 'All Clear':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
                elif requested_task.result == 'Request can not be processed':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Document Requested again':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Failed':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        else:
            if myrequesttask:
                if myrequesttask.mark_complete == False:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'                    
                else:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Completed</a>'
            else:
                return '<u><i><a href="javascript:void();" class="not-complete" \
                data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'
    else:
        return 'NA'


def step_three_status(value):
    try:
        requested_task = MyRequestTasksInfo.objects.get(myrequest_id = value, step_id = '3')
    except:
        requested_task = None

    try:
        myrequesttask = MyRequestTasks.objects.get(myrequest_id = value, step_id = '3')
    except:
        myrequesttask = None

    if requested_task:
        if requested_task.progress_status:
            if requested_task.progress_status == 'Assigned':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-blue not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'In Progress':
                return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'Completed':
                if requested_task.result == 'All Clear':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
                elif requested_task.result == 'Request can not be processed':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Document Requested again':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Failed':
                    return '<span data-toggle="modal" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        else:
            if myrequesttask:
                if myrequesttask.mark_complete == False:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'
                else:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Completed</a>'
            else:
                return '<u><i><a href="javascript:void();" class="not-complete" \
                data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'
    else:
        return 'NA'


def step_four_status(value):
    try:
        requested_task = MyRequestTasksInfo.objects.get(myrequest_id = value, step_id = '4')
    except:
        requested_task = None

    try:
        myrequesttask = MyRequestTasks.objects.get(myrequest_id = value, step_id = '4')
    except:
        myrequesttask = None

    if requested_task:
        if requested_task.cmo_manager_status:
            if requested_task.cmo_manager_status == 'Approve':
                return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-cmo_manager_comment="'+str(requested_task.cmo_manager_comment)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
            else:
                return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-cmo_manager_comment="'+str(requested_task.cmo_manager_comment)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        elif requested_task.progress_status:
            if requested_task.progress_status == 'Assigned':
                return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-blue not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'In Progress':
                return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
            elif requested_task.progress_status == 'Completed':
                if requested_task.result == 'All Clear':
                    return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-success r-10">&nbsp;</span>'
                elif requested_task.result == 'Minor Issues':
                    return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-orange not-complete r-10">&nbsp;</span>'
                elif requested_task.result == 'Serious medical condition':
                    return '<span data-toggle="modal" data-step-id="'+str(4)+'" data-status="'+str(requested_task.progress_status)+'" data-resultstatus="'+str(requested_task.result)+'" data-comments="'+str(requested_task.result_comment)+'" data-filename="'+str(requested_task.file_name)+'" data-target="#exampleModal" class="badge badge-danger not-complete r-10">&nbsp;</span>'
        else:
            if myrequesttask:
                if requested_task.vendor:
                    if myrequesttask.mark_complete == False:
                        return '<u><i><a href="javascript:void();" class="not-complete" \
                        data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                        +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'
                    else:
                        return '<u><i><a href="javascript:void();" class="not-complete" \
                        data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                        +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Completed</a>'
                else:
                    if myrequesttask.mark_complete == False:
                        return '<u><i><a href="javascript:void();" class="not-complete" \
                        data-toggle="popover" title="CMO" data-content="CMO Name: '\
                        +str(requested_task.medical_cmo_user)+' Email:'+requested_task.medical_cmo_user.user.email+'">Task Assigned</a>'
                    else:
                        return '<u><i><a href="javascript:void();" class="not-complete" \
                        data-toggle="popover" title="CMO" data-content="CMO Name: '\
                        +str(requested_task.medical_cmo_user)+' Email:'+requested_task.medical_cmo_user.user.email+'">Task Completed</a>'
            else:
                if requested_task.vendor:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="Vendor" data-content="Vendor Name: '\
                    +requested_task.vendor.vendor.vendor_company_name+' Email:'+requested_task.vendor.vendor.email+'">Task Assigned</a>'
                else:
                    return '<u><i><a href="javascript:void();" class="not-complete" \
                    data-toggle="popover" title="CMO" data-content="CMO Name: '\
                    +str(requested_task.medical_cmo_user)+' Email:'+requested_task.medical_cmo_user.user.email+'">Task Assigned</a>'
    else:
        return 'NA'


def get_graph_percentage_for_bgv_step(value):
    percentage = 0
    count = 0
    result = MyRequestTasksBgvDocs.objects.filter(myrequest_task = value)

    for res in result:
        if res.mark_complete or res.not_applicable:
            count = count + 1

        percentage = count/result.count() * 100

    if result:
        return int(percentage)
    else:
        return 0


def get_bgv_step_one_files(value, arg):
    try:
        result = MyRequestTasksBgvDocs.objects.get(myrequest_task = value, document_id = arg)
    except:
        result = None

    if result:
        if result.document_file:
            return '<a href="'+result.document_file.url+'" class="document-file">'+result.document_file.name+'</a>'
        else:
            return ''
    else:
        return ''


def get_hr_step_three_files(value, arg):    
    try:
        result = MyRequestTasksHrDocs.objects.get(myrequest_task = value, template_id = arg)
    except:
        result = None

    if result:
        if result.document_name:
            return '<a href="'+result.document_name.url+'" class="document-file">'+result.document_name.name+'</a>'
        else:
            return ''
    else:
        return ''


def get_medical_step_four_files(value, arg):
    try:
        result = MyRequestTasksMedicalDocs.objects.get(myrequest_task = value, template_id = arg)
    except:
        result = None

    if result:
        if result.document_name:
            return '<a href="'+result.document_name.url+'" class="document-file">'+result.document_name.name+'</a>'
        else:
            return ''
    else:
        return ''


def get_bgv_step_one_mark_complete(value, arg):
    try:
        result = MyRequestTasksBgvDocs.objects.get(myrequest_task = value, document_id = arg)
    except:
        result = None

    if result:
        return result.mark_complete
    else :
        return False


def get_bgv_step_one_mark_applicable(value, arg):
    try:
        result = MyRequestTasksBgvDocs.objects.get(myrequest_task = value, document_id = arg)
    except:
        result = None

    if result:
        return result.not_applicable
    else:
        return False


def get_hr_step_three_mark_complete(value, arg):
    try:
        result = MyRequestTasksHrDocs.objects.get(myrequest_task = value, template_id = arg)
    except:
        result = None

    if result:
        return result.mark_complete
    else :
        return False


def get_medical_step_four_mark_complete(value, arg):
    try:
        result = MyRequestTasksMedicalDocs.objects.get(myrequest_task = value, template_id = arg)
    except:
        result = None

    if result:
        return result.mark_complete
    else :
        return False


def get_hr_step_three_mark_applicable(value, arg):
    try:
        result = MyRequestTasksHrDocs.objects.get(myrequest_task = value, template_id = arg)
    except:
        result = None

    if result:
        return result.not_applicable
    else :
        return False


def get_medical_step_four_mark_applicable(value, arg):
    try:
        result = MyRequestTasksMedicalDocs.objects.get(myrequest_task = value, template_id = arg)
    except:
        result = None

    if result:
        return result.not_applicable
    else :
        return False


def get_graph_percentage_for_hr_step(value):
    percentage = 0
    count = 0
    result = MyRequestTasksHrDocs.objects.filter(myrequest_task = value)

    for res in result:
        if res.mark_complete or res.not_applicable:
            count = count + 1

        percentage = count/result.count() * 100

    if result:
        return int(percentage)
    else:
        return 0


def get_graph_percentage_for_medical_step(value):
    percentage = 0
    count = 0
    result = MyRequestTasksMedicalDocs.objects.filter(myrequest_task = value)

    for res in result:
        if res.mark_complete or res.not_applicable:
            count = count + 1

        percentage = count/result.count() * 100

    if result:
        return int(percentage)
    else:
        return 0


def get_graph_percentage_for_ref_step(value):
    percentage = 0
    count = 0
    reference = {}

    result = MyRequestTasksRefDocs.objects.filter(myrequest_task = value)

    for res in result:
        if res.reference_id not in reference:
            reference[res.reference_id] = 'True'
            if res.mark_complete or res.not_applicable:
                count = count + 1

            percentage = count/len(reference) * 100


    if result:
        return int(percentage)
    else:
        return 0


def get_ref_step_two_ref_organisation_second(value, arg):
    try:
        data = MyRequestTasksRefDocs.objects.get(id = value)
    except:
        data = None    

    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = data.myrequest_task, reference_id = data.reference_id).order_by('id')[arg]
    except:
        result = None

    if result:
        return result.ref_organisation
    else:
        return ''


def get_ref_step_two_ref_phone_second(value, arg):

    try:
        data = MyRequestTasksRefDocs.objects.get(id = value)
    except:
        data = None

    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = data.myrequest_task, reference_id = data.reference_id).order_by('id')[arg]
    except:
        result = None

    if result:
        return result.ref_phone
    else:
        return ''



def get_ref_step_two_ref_office_email_second(value, arg):
    try:
        data = MyRequestTasksRefDocs.objects.get(id = value)
    except:
        data = None

    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = data.myrequest_task, reference_id = data.reference_id).order_by('id')[arg]
    except:
        result = None

    if result:
        return result.ref_office_email
    else:
        return ''



def get_ref_step_two(value, arg):
    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = value, reference_id = arg).last()
    except:
        result = None

    if result:
        return result.id
    else:
        return ''


def get_ref_step_two_ref_relation_second(value, arg):    
    try:
        data = MyRequestTasksRefDocs.objects.get(id = value)
    except:
        data = None

    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = data.myrequest_task, reference_id = data.reference_id).order_by('id')[arg]
    except:
        result = None

    if result:
        return result.ref_relation
    else:
        return ''


def get_ref_step_two_ref_mark_complete(value, arg):
    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = value, reference_id = arg).last()
    except:
        result = None

    if result:
        return result.mark_complete
    else:
        return False


def get_ref_step_two_ref_mark_applicable(value, arg):
    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = value, reference_id = arg).last()
    except:
        result = None

    if result:
        return result.not_applicable
    else:
        return False


def get_ref_step_two_ref_name_second(value, arg):

    try:
        data = MyRequestTasksRefDocs.objects.get(id = value)
    except:
        data = None    

    try:
        result = MyRequestTasksRefDocs.objects.filter(myrequest_task = data.myrequest_task, reference_id = data.reference_id).order_by('id')[arg]
    except:
        result = None

    if result:
        return result.ref_name
    else:
        return ''


def request_details(value, arg):
    myrequesttaskinfo = None

    try:
        myrequesttaskinfo = MyRequestTasksInfo.objects.get(myrequest = value, step_id = arg)
    except:
        myrequesttaskinfo = None

    if myrequesttaskinfo:
        if arg =='1':
            return '<a href="javascript:void();" data-step_id="'+str(myrequesttaskinfo.step_id)+'" data-result="'+str(myrequesttaskinfo.result)+'" data-progress_status="'+str(myrequesttaskinfo.progress_status)+'" data-comments="'+str(myrequesttaskinfo.result_comment)+'" data-file_name="'+str(myrequesttaskinfo.file_name)+'" data-toggle="modal" data-target="#exampleModal2" class="btn btn-success s-12 detail-model">Details</a>'
        elif arg == '3':
            return '<a href="javascript:void();" data-step_id="'+str(myrequesttaskinfo.step_id)+'" data-comments="'+str(myrequesttaskinfo.result_comment)+'" data-file_name="'+str(myrequesttaskinfo.file_name)+'" data-toggle="modal" data-target="#exampleModal2" class="btn btn-success s-12 detail-model">Details</a>'
        elif arg == '4':
            return '<a href="javascript:void();" data-step_id="'+str(myrequesttaskinfo.step_id)+'" data-comments="'+str(myrequesttaskinfo.result_comment)+'" data-file_name="'+str(myrequesttaskinfo.file_name)+'" data-toggle="modal" data-target="#exampleModal2" class="btn btn-success s-12 detail-model">Details</a>'
        elif arg == '2':
            return '<a href="javascript:void();" data-step_id="'+str(myrequesttaskinfo.step_id)+'" data-myrequest_id="'+str(myrequesttaskinfo.myrequest_id)+'" data-comments="'+str(myrequesttaskinfo.result_comment)+'" data-file_name="'+str(myrequesttaskinfo.file_name)+'" data-toggle="modal" data-target="#exampleModal2" class="btn btn-success s-12 step_two_details">Details</a>'

    return '<a href="javascript:void();" data-toggle="modal" data-target="#exampleModal2" class="btn btn-success s-12 detail-model">Details</a>'


def get_reimbursement_files(value):
    li_list = ''
    reimbursements = ReimbursementDocument.objects.filter(reimbursement_id = value)

    for reimbursement in reimbursements:
        li_list = li_list + '<a href="'+str(reimbursement.document_file.url)+'">'+str(reimbursement.document_file)+'</a><br>'

    return li_list

def company_logo_url(value):
    value = value.replace('https://s3-project-application-drive.s3.amazonaws.com/','')
    return value


def travel_book(value):    
    try:
        travel = TravelBooking.objects.filter(myrequest_id = value).last()
    except:
        travel = None

    if travel:
        return '\
        <a href="#" class="btn btn-success btn-xs travel-info" data-toggle="modal" data-id="'+str(value)+'" data-target="#travelModal">Travel Booked</a>\
        '
    else:
        return '\
        <a href="/travel-booking/'+str(value)+'" class="btn btn-success btn-xs travel-booking">GO</a>\
        <br><br>\
        <input type="checkbox" class="form-control override"> Override\
        '

register.filter('document_file_name', document_file_name)
register.filter('bgv_ischecked', bgv_ischecked)
register.filter('ref_ischecked', ref_ischecked)
register.filter('hr_ischecked', hr_ischecked)
register.filter('medical_ischecked', medical_ischecked)

register.filter('ref_no_reference', ref_no_reference)
register.filter('is_requested', is_requested)
register.filter('step_one_status', step_one_status)
register.filter('step_two_status', step_two_status)
register.filter('step_three_status', step_three_status)
register.filter('step_four_status', step_four_status)

register.filter('is_requested_button', is_requested_button)

register.filter('get_graph_percentage_for_bgv_step', get_graph_percentage_for_bgv_step)

register.filter('get_bgv_step_one_files', get_bgv_step_one_files)
register.filter('get_bgv_step_one_mark_complete', get_bgv_step_one_mark_complete)
register.filter('get_bgv_step_one_mark_applicable', get_bgv_step_one_mark_applicable)
register.filter('get_hr_step_three_files', get_hr_step_three_files)
register.filter('get_medical_step_four_files', get_medical_step_four_files)
register.filter('get_hr_step_three_mark_complete', get_hr_step_three_mark_complete)
register.filter('get_medical_step_four_mark_complete', get_medical_step_four_mark_complete)
register.filter('get_hr_step_three_mark_applicable', get_hr_step_three_mark_applicable)
register.filter('get_medical_step_four_mark_applicable', get_medical_step_four_mark_applicable)
register.filter('get_graph_percentage_for_hr_step', get_graph_percentage_for_hr_step)
register.filter('get_graph_percentage_for_ref_step', get_graph_percentage_for_ref_step)
register.filter('get_graph_percentage_for_medical_step', get_graph_percentage_for_medical_step)

register.filter('get_ref_step_two', get_ref_step_two)

register.filter('get_ref_step_two_ref_mark_complete', get_ref_step_two_ref_mark_complete)

register.filter('get_ref_step_two_ref_name_second', get_ref_step_two_ref_name_second)
register.filter('get_ref_step_two_ref_organisation_second', get_ref_step_two_ref_organisation_second)
register.filter('get_ref_step_two_ref_phone_second', get_ref_step_two_ref_phone_second)
register.filter('get_ref_step_two_ref_office_email_second', get_ref_step_two_ref_office_email_second)
register.filter('get_ref_step_two_ref_relation_second', get_ref_step_two_ref_relation_second)
register.filter('get_ref_step_two_ref_mark_applicable', get_ref_step_two_ref_mark_applicable)
register.filter('request_details', request_details)
register.filter('get_reimbursement_files', get_reimbursement_files)
register.filter('company_logo_url', company_logo_url)
register.filter('travel_book', travel_book)
