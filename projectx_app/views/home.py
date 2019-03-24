from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import EmailMessage


class Home(generic.TemplateView):
    template_name = 'home/index.html'

    def post(self, request, *args, **kwargs):

        contact_phone = request.POST['contact_phone']
        company_name = request.POST['company_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        designation = request.POST['designation']
        company_email = request.POST['company_email']

        html_message = "Dear Team,<br>\
        The demo is booked:<br>\
        contact phone: "+company_email+"<br>\
        company name: "+company_name+"<br>\
        first name: "+first_name+"<br>\
        last name: "+last_name+"<br>\
        designation: "+designation+"<br>\
        company email: "+company_email+"<br>\
        <br><br>Cheers,<br>Team 360degree<br>"
        email_message = EmailMessage('Demo Booked - Information', html_message, settings.EMAIL_HOST_USER, [],['info@360degree.ai'])
        email_message.content_subtype = "html"
        email_message.send()

        return render(request, self.template_name, {})

class Platform(generic.TemplateView):
    template_name = 'home/platform.html'

class Products(generic.TemplateView):
    template_name = 'home/products.html'

class Contact(generic.TemplateView):
    template_name = 'home/contactus.html'

