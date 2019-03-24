from projectx_app.models.task import *
from projectx_app.models.request import *
from django.conf import settings
from django.core.mail import EmailMessage
from celery import task

@task
def task_completion_reminder():
    my_request_tasks = MyRequestTasks.objects.filter(mark_complete = False)

    for my_request_task in my_request_tasks:
        html_message = "Dear Applicant,"+"<br><br>Your Task is still pending, please complete your task.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team 360degree.ai<br>"
        email_message = EmailMessage('Task Completion Reminder', html_message, settings.EMAIL_HOST_USER, [],[my_request_task.myrequest.applicant.user.email])
        email_message.content_subtype = "html"
        email_message.send()

    return 'Task Completion Reminder is sent.'
