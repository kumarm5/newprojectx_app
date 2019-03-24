from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.travel_booking import *
from projectx_app.forms.travel_booking import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class TravelBookingCreateView(LoginRequiredMixin, generic.CreateView):
    model = TravelBooking
    form_class = TravelBookingForm
    template_name = 'projectx_app/travel-booking-form.html'

    def get_form_kwargs(self):
        kwargs = super(TravelBookingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            my_request = MyRequest.objects.get(pk = int(self.kwargs['request_id']))
        except:
            my_request = None

        context['my_request'] = my_request
        return context

    def form_valid(self, form):
        work_listing = form.save()
        messages.success(self.request, 'Travel Booking information is updated successfully.')
        return redirect('company-user-dashboard')


def travel_booked_details(request, request_id=None):
    try:
        travel = TravelBooking.objects.filter(myrequest = request_id).last()
    except:
        travel = None

    if travel:
        data = {
            'travel_id': travel.id,
            'vendor': travel.vendor.vendor.vendor_company_name,
            'vendor_email': travel.vendor_email,
            'due_date': travel.due_date,
            'attached_template': travel.attached_template.name,
            'comments': travel.comments
        }

        if travel.attached_template:
            data = {
                'travel_attached_template_url': travel.attached_template.url,
                'travel_template_name': travel.attached_template.name
            }

    return JsonResponse(data)


def travel_booked_delete(request, travel_id=None):
    try:
        travel_delete = TravelBooking.objects.filter(pk = travel_id).delete()
    except:
        travel_delete = None

    if travel_delete:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


def travel_booked_update(request):
    model_travel_id = int(request.POST['model_travel_id'])
    modal_comments = request.POST['modal_comments']
    modal_due_date = request.POST['modal_due_date']
    modal_vendor_email = request.POST['modal_vendor_email']
    modal_vendor = request.POST['modal_vendor']

    try:
        travel_booked_update = TravelBooking.objects.filter(pk = model_travel_id).update(
            comments = modal_comments,
            due_date = modal_due_date,
            vendor_email = modal_vendor_email,
        )
    except:
        travel_booked_update = None

    if travel_booked_update:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }
    return JsonResponse(data)
