from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.onboarding import *
from projectx_app.models.request import *
from projectx_app.models.vendor import *
from projectx_app.models.task import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class VendorAdminMyOrderList(LoginRequiredMixin, generic.ListView):
    template_name = 'projectx_app/vendor-admin-my-orders.html'
    model = MyRequestTasksInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            vendor_user = CompanyVendor.objects.filter(user = self.request.user).last()
        except:
            vendor_user = None

        # get the company case worker to assign the task
        if vendor_user:
            context['vendors'] = CompanyVendor.objects.filter(company = vendor_user.company, user__user_type = 4, owner = self.request.user)
        else:
            context['vendors'] = None
        return context

    def get_queryset(self):
        request_info = self.model.objects.filter(vendor__user = self.request.user)
        return request_info


def vendor_admin_my_order_vender_update(request, request_id=None, vendor_id = None):
    '''
        This function is used to update vendor for request.
    '''
    try:
        update_myrequest = MyRequestTasksInfo.objects.filter(pk = int(request_id)).update(vendor_user_id = vendor_id, progress_status='Assigned')
    except:
        update_myrequest = None

    if update_myrequest:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


def vendor_documents(request, myrequest_id=None, step_id=None):
    my_request_task_docs = None

    try:
        myrequest_task = MyRequestTasks.objects.get(myrequest_id = myrequest_id, step_id = step_id)
    except:
        myrequest_task = None

    if myrequest_task and step_id == 1:
        my_request_task_docs = MyRequestTasksBgvDocs.objects.filter(myrequest_task = myrequest_task).values('document_file')
    elif myrequest_task and step_id == 3:
        my_request_task_docs = MyRequestTasksHrDocs.objects.filter(myrequest_task = myrequest_task).values('document_name')
    elif myrequest_task and step_id == 4:
        my_request_task_docs = MyRequestTasksMedicalDocs.objects.filter(myrequest_task = myrequest_task).values('document_name')
    else:
        my_request_task_docs = {}
    return JsonResponse(list(my_request_task_docs), safe=False)


def reference_details(request, myrequest_id=None, step_id=None):

    myrequesttask_ref = MyRequestTasksRefDocs.objects.filter(myrequest_task__myrequest_id = myrequest_id).values('reference__reference_name','ref_name', 'ref_organisation', 'ref_office_email', 'ref_relation', 'ref_phone')

    return JsonResponse(list(myrequesttask_ref), safe=False)
