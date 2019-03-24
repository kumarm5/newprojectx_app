from django.urls import path, re_path
from django.conf.urls import handler404, handler500, url, include

# from projectx_app.views.error_handle import (
#     error_404,
#     error_500,
# )

from django.contrib.auth import views as auth_views

from projectx_app.views.user_detail import *

from projectx_app.views.company import (
    CompanyAccountView,
    SystemCompanySetupView,
    SystemCompanySetupCreateView,
    SystemCompanySetupUpdateView,
    delete_systemcompanysetup_info,
    CompanyUserView,
    CompanyUserCreateView,
    CompanyUserUpdateView,
    delete_company_user_info,
    CompanyUserDashboard,
    CMOUserDashboard,
    CMOUserMyCaseForm,
    HiringManagerDashboard,
    HiringManagerUserMyCaseForm,
)

from projectx_app.views.applicant import (
    ApplicantUserView,
    ApplicantUserCreateView,
    ApplicantUserUpdateView,
    delete_applicant_info,
)

from projectx_app.views.rpo import (
    SysRPOView,
    RPOInfoCreateView,
    RPOInfoUpdateView,
    delete_rpo_info,
    RpoAccountView,
    rpo_company,
    RPOUserCreateView,
    RPOUserUpdateView,
)

from projectx_app.views.task import (
    MyTaskListView,
    get_my_task,
)

from projectx_app.views.vendor import (
    MyVendorListView,
    MyRpoVendorListView,
    MyVendorCreateView,
    MyVendorUpdateView,
    AddCompanyVendor,
    CompanyVendorUpdateView,
    search_vendor,
    vendor_email,
)

from projectx_app.views.document import (
    DocumentInfoView,
    DocumentInfoCreateView,
    DocumentInfoUpdateView,
    delete_document_info,
)

from projectx_app.views.template import (
    CompanyTemplateView,
    TemplateCreateView,
    TemplateUpdateView,
    delete_template_info,
    RpoCompanyTemplateView
)

from projectx_app.views.onboarding import (
    CoOnboardingTypeView,
    delete_onboarding_info,
    create_onboarding_steps,
    edit_onboarding_steps,
    RpoCoOnboardingTypeView,
)

from projectx_app.views.request import (
    create_request_listing,
    create_request_form,
    RequestApplicantCreateView,
    MyRequestView,
    my_request_detail,
    create_request,
    search_applicant,
    search_onboarding_tasks,
    MyRequestUpdateView,
    update_request,
    create_onboarding_request,
)

from projectx_app.views.auth import (
    Login,
    Register,
    logout_view,
    change_password,
    validate_email,
    send_otp,
)

from projectx_app.views.vendor_admin_account import (
    VendorAdminMyAccountView,
    VendorAccountUserCreateView,
    VendorAccountUserUpdateView,
)


from projectx_app.views.vendor_admin_order import (
    VendorAdminMyOrderList,
    vendor_admin_my_order_vender_update,
    vendor_documents,
    reference_details,
)

from projectx_app.views.vendor_user_cases import (
    VendorUserMyCase,
    VendorUserMyCaseForm,
)

from projectx_app.views.company import (
    CompanyUserDashboard,
)

from projectx_app.views.medical_check import (
    MedicalCheckCreateView,
)

from projectx_app.views.travel_booking import (
    TravelBookingCreateView,
    travel_booked_details,
    travel_booked_delete,
    travel_booked_update,
)

from projectx_app.views.reimbursement import (
    ReimbursementListView,
    ReimbursementCreateView,
    ReimbursementUpdateView,
)

from projectx_app.views.home import (
    Home,
    Platform,
    Products,
    Contact,
)

urlpatterns = [
    # landing pages
    path(r'', Home.as_view(), name='home'),
    path(r'platform/', Platform.as_view(), name='platform'),
    path(r'products/', Products.as_view(), name='products'),
    path(r'contact/', Contact.as_view(), name='contact'),

    path(r'login/', Login.as_view(), name='login'),
    path(r'register/', Register.as_view(), name='register'),
    path(r'logout/', logout_view, name='logout'),
    path(r'password/', change_password, name='change-password'),
    path(r'ajax/validate-email/<str:email>', validate_email, name='validate-email'),
    path(r'dashboard/', Dashboard.as_view(), name='dashboard'),
    path(r'contact-info/', ContactViewInfo.as_view(), name='contact-info'),
    path(r'ajax/send-otp/<str:mobile_number>', send_otp, name='send-otp'),


    path(r'id-info/', IDInfoView.as_view(), name='id-info-listing'),
    path(r'id-info-create/', IDInfoCreateView.as_view(), name='create-id-info'),
    path(r'id-info-edit/<int:id>', IDInfoUpdateView.as_view(), name='edit-id-info'),
    path(r'ajax/delete-identification-info/<int:gov_id>', delete_identification_info, name='delete-id-info'),


    path(r'work-info/', WorkInfoView.as_view(), name='work-info-listing'),
    path(r'work-info-create/', WorkInfoCreateView.as_view(), name='create-work-info'),
    path(r'work-info-edit/<int:id>', WorkInfoUpdateView.as_view(), name='edit-work-info'),
    path(r'ajax/delete-work-info/<int:work_id>', delete_work_info, name='delete-work-info'),


    path(r'education-info/', EducationInfoView.as_view(), name='education-info-listing'),
    path(r'education-info-create/', EducationInfoCreateView.as_view(), name='create-education-info'),
    path(r'education-info-edit/<int:id>', EducationInfoUpdateView.as_view(), name='edit-education-info'),
    path(r'ajax/delete-education-info/<int:education_id>', delete_education_info, name='delete-education-info'),


    path(r'document-info/', DocumentInfoView.as_view(), name='document-info-listing'),
    path(r'document-info-create/', DocumentInfoCreateView.as_view(), name='create-document-info'),
    path(r'document-info-edit/<int:id>', DocumentInfoUpdateView.as_view(), name='edit-document-info'),
    path(r'ajax/delete-document-info/<int:document_id>', delete_document_info, name='delete-document-info'),


    path(r'sysrpo_listing/', SysRPOView.as_view(), name='sysrpo-listing'),
    path(r'sysrpo-info-create/', RPOInfoCreateView.as_view(), name='create-sysrpo-info'),
    path(r'sysrpo-info-edit/<int:id>', RPOInfoUpdateView.as_view(), name='edit-rpo-info'),
    path(r'ajax/delete-rpo-info/<int:rpo_id>', delete_rpo_info, name='delete-rpo-info'),


    path(r'company_listing/', SystemCompanySetupView.as_view(), name='company-listing'),
    path(r'company-info-create/', SystemCompanySetupCreateView.as_view(), name='create-company-info'),
    path(r'company-info-edit/<int:id>', SystemCompanySetupUpdateView.as_view(), name='edit-company-info'),
    path(r'ajax/delete-company-info/<int:systemcompanysetup_id>', delete_systemcompanysetup_info, name='delete-company-info'),


    path(r'company-user-listing/', CompanyUserView.as_view(), name='company-user-listing'),
    path(r'company-user-create/', CompanyUserCreateView.as_view(), name='create-company-user-info'),
    path(r'company-user-edit/<int:id>', CompanyUserUpdateView.as_view(), name='edit-company-user-info'),
    path(r'ajax/delete-company-user-info/<int:company_user_id>', delete_company_user_info, name='delete-company-user-info'),


    # path(r'vendor_listing/', VendorUserView.as_view(), name='vendor-listing'),
    # path(r'vendor-info-create/', VendorUserCreateView.as_view(), name='create-vendor-info'),
    # path(r'vendor-info-edit/<int:id>', VendorUserUpdateView.as_view(), name='edit-vendor-info'),
    # path(r'ajax/delete-vendor-info/<int:vendor_id>', delete_vendor_info, name='delete-vendor-info'),


    path(r'applicant_listing/', ApplicantUserView.as_view(), name='applicant-listing'),
    path(r'applicant-info-create/', ApplicantUserCreateView.as_view(), name='create-applicant-info'),
    path(r'applicant-info-edit/<int:id>', ApplicantUserUpdateView.as_view(), name='edit-applicant-info'),
    path(r'ajax/delete-applicant-info/<int:applicant_id>', delete_applicant_info, name='delete-applicant-info'),


    path(r'template_listing/', CompanyTemplateView.as_view(), name='template-listing'),
    path(r'rpo-template_listing/', RpoCompanyTemplateView.as_view(), name='rpo-template-listing'),
    path(r'template-info-create/', TemplateCreateView.as_view(), name='create-template-info'),
    path(r'template-info-edit/<int:id>', TemplateUpdateView.as_view(), name='edit-template-info'),
    path(r'ajax/delete-template-info/<int:template_id>', delete_template_info, name='delete-template-info'),


    path(r'company-account/', CompanyAccountView.as_view(), name='company-account'),
    path(r'rpo-account/', RpoAccountView.as_view(), name='rpo-account'),


    path(r'onboarding_listing/', CoOnboardingTypeView.as_view(), name='onboarding-listing'),
    path(r'rpo-onboarding_listing/', RpoCoOnboardingTypeView.as_view(), name='rpo-onboarding_listing'),
    path(r'onboarding-info-create/', create_onboarding_steps, name='create-onboarding-info'),
    path(r'onboarding-info-edit/<int:id>', edit_onboarding_steps, name='edit-onboarding-info'),
    path(r'ajax/delete-onboarding-info/<int:onboarding_id>', delete_onboarding_info, name='delete-onboarding-info'),


    path(r'request_listing/', create_request_listing, name='request-listing'),
    # path(r'my_dashboard/', companyuser_dashboard, name='my-dashboard'),
    path(r'create-request-form/<int:type_id>/<int:user_id>/', create_request_form, name='create-request-form'),
    path(r'create_request_applicant/', RequestApplicantCreateView.as_view(), name='create-request-applicant'),
    # path(r'create-request/<int:id>/', create_request, name='create-request'),

    path(r'create-request/<int:applicant_id>/', create_onboarding_request, name='create-request'),
    path(r'create-request/<int:applicant_id>/<int:onboarding_id>/', create_onboarding_request, name='create-onboarding-request'),

    path(r'ajax/search-onboarding-tasks/<int:id>/<int:applicant_id>/', search_onboarding_tasks, name='search-onboarding-tasks'),
    # path(r'update-request/<int:id>', MyRequestUpdateView.as_view(), name='update-request'),
    path(r'update-request/<int:id>', update_request, name='update-request'),


    path(r'my-request', MyRequestView.as_view(), name='my-request'),
    path(r'request-detail/<int:type_id>', my_request_detail, name='request-detail'),
    path(r'ajax/search-applicant/', search_applicant, name='search-applicant'),


    path(r'vendor-user-listing/', MyVendorListView.as_view(), name='vendor-user-listing'),
    path(r'rpo-vendor-user-listing/', MyRpoVendorListView.as_view(), name='rpo-vendor-user-listing'),
    path(r'vendor-user-create/', MyVendorCreateView.as_view(), name='vendor-user-create'),
    path(r'vendor-user-edit/<int:id>', MyVendorUpdateView.as_view(), name='vendor-user-edit'),
    path(r'ajax/add-company-vendor/<int:id>', AddCompanyVendor.as_view(), name='add-company-vendor'),
    path(r'company-vendor-edit/<int:id>', CompanyVendorUpdateView.as_view(), name='company-vendor-edit'),
    path(r'ajax/search-vendor/', search_vendor, name='search-vendor'),
    path(r'ajax/vendor-email/<int:id>', vendor_email, name='vendor-email'),


    path(r'my-task-listing/', MyTaskListView.as_view(), name='my-task'),
    path(r'my-task/<int:id>', get_my_task, name='get-my-task'),


    # path(r'vendor-my-account/', MyVendorAccount, name='vendor-my-account'),
    # path(r'vendor-my-orders/', MyVendorOrders, name='vendor-my-orders'),
    # path(r'vendor-account-details/', MyVendorAccount, name='vendor-account-detailsas'),
    # path(r'vendor-account-detail/', VendorAccountDetails, name='vendor-account-detail'),

    path(r'company-user-dashboard/', CompanyUserDashboard.as_view(), name='company-user-dashboard'),

    # cmo-user-account
    path(r'cmo-dashboard/', CMOUserDashboard.as_view(), name='cmo-dashboard'),
    path(r'cmo-user-case/<int:id>', CMOUserMyCaseForm.as_view(), name='cmo-user-case-form'),

    # hiring-manager-user
    path(r'hiring-manager-dashboard/', HiringManagerDashboard.as_view(), name='hiring-manager-dashboard'),
    path(r'hiring-manager-user-case-form/<int:id>', HiringManagerUserMyCaseForm.as_view(), name='hiring-manager-user-case-form'),

    #vendor admin menu views
    path(r'vendor-account-detail/', VendorAdminMyAccountView.as_view(), name='vendor-admin-account-detail'),
    path(r'create-vendor-user/', VendorAccountUserCreateView.as_view(), name='create-vendor-user'),
    path(r'vendor-account-user-edit/<int:id>', VendorAccountUserUpdateView.as_view(), name='vendor-account-user-edit'),
    path(r'vendor-admin-my-order/', VendorAdminMyOrderList.as_view(), name='vendor-admin-my-order'),
    path(r'ajax/vendor-admin-my-order-vender/<int:request_id>/<int:vendor_id>/', vendor_admin_my_order_vender_update, name='vendor-admin-my-order-vender'),
    path(r'ajax/vendor-documents/<int:myrequest_id>/<int:step_id>/', vendor_documents, name='vendor-documents'),
    path(r'ajax/reference-details/<int:myrequest_id>/<int:step_id>/', reference_details, name='reference-details'),

    #vendor user menu views
    path(r'vendor-user-my-cases/', VendorUserMyCase.as_view(), name='vendor-user-my-cases'),
    path(r'vendor-user-my-case-form/<int:id>', VendorUserMyCaseForm.as_view(), name='vendor-user-my-case-form'),

    path(r'medical-check/<int:request_id>', MedicalCheckCreateView.as_view(), name='medical-check'),
    path(r'travel-booking/<int:request_id>', TravelBookingCreateView.as_view(), name='travel-booking'),
    path(r'ajax/travel-booked-details/<int:request_id>', travel_booked_details, name='travel-details'),
    path(r'ajax/travel-booked-delete/<int:travel_id>', travel_booked_delete, name='travel-delete'),
    path(r'ajax/travel-booked-update/', travel_booked_update, name='travel-update'),


    # rpo company
    path(r'ajax/rpo-company/<int:company_id>', rpo_company, name='rpo-company'),
    path(r'ajax/rpo-company/', rpo_company, name='rpo-company'),

    path(r'my-reimbursement/', ReimbursementListView.as_view(), name='my-reimbursement'),
    path(r'create-reimbursement/', ReimbursementCreateView.as_view(), name='create-reimbursement'),
    path(r'edit-reimbursement/<int:reimbursement_id>', ReimbursementUpdateView.as_view(), name='edit-reimbursement'),

    # rpo user
    path(r'create-rpo-user', RPOUserCreateView.as_view(), name='create-rpo-user'),
    path(r'edit-rpo-user/<int:rpo_id>', RPOUserUpdateView.as_view(), name='edit-rpo-user'),

    url('^', include('django.contrib.auth.urls')),
]

# handler404 = error_404
# handler500 = error_500
