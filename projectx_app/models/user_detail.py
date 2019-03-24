from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('Refuse to answer','Refuse to answer'),
)

MARITAL_STATUS = (
    ('MARRIED', 'Married'),
    ('UNMARRIED', 'Unmarried'),
    ('Refuse to answer','Refuse to answer'),
)

NAMECHANGED = (
    (True, 'Yes'),
    (False, 'No')
)

STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)


class PersonalInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_personal_info')
    middleName = models.CharField(max_length=256, blank=True, null=True)    
    salutation = models.CharField(max_length=256, blank=True, null=True)
    dateOfBirth = models.DateField(max_length=256, blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=256, blank=True, null=True)
    maritalStatus = models.CharField(choices=MARITAL_STATUS, max_length=256, blank=True, null=True)
    nameChanged = models.BooleanField(choices=NAMECHANGED, default=False, blank=True, null=True)
    previousName = models.CharField(max_length=256, blank=True, null=True)
    previousNameStatus = models.BooleanField(default=False, blank=True, null=True)
    beforeMarriage = models.CharField(max_length=256, blank=True, null=True)
    fatherFirstName = models.CharField(max_length=256, blank=True, null=True)
    fatherMiddleName = models.CharField(max_length=256, blank=True, null=True)
    fatherLastName = models.CharField(max_length=256, blank=True, null=True)
    motherFirstName = models.CharField(max_length=256, blank=True, null=True)
    motherMiddleName = models.CharField(max_length=256, blank=True, null=True)
    motherLastName = models.CharField(max_length=256, blank=True, null=True)
    spouseFirstName = models.CharField(max_length=256, blank=True, null=True)
    spouseMiddleName = models.CharField(max_length=256, blank=True, null=True)
    spouseLastName = models.CharField(max_length=256, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, verbose_name='Profile Picture')

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Personal Info"
        verbose_name_plural = "Personal Infos"

@receiver(post_save, sender=User)
def create_or_update_user_personalinfo(sender, instance, created, **kwargs):
    if created:
        PersonalInfo.objects.create(user=instance)
    instance.user_personal_info.save()


class ContactInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contact_info')
    primaryEmail = models.EmailField(max_length=256, blank=True, null=True)
    alternateEmail = models.EmailField(max_length=256, blank=True, null=True)
    mobileNumber = models.CharField(max_length=256, blank=True, null=True)
    workNumber = models.CharField(max_length=256, blank=True, null=True)
    homeNumber = models.CharField(max_length=256, blank=True, null=True)
    preferredNumber = models.CharField(max_length=256, blank=True, null=True)
    preferredEmail = models.EmailField(max_length=256, blank=True, null=True)
    mobileNumberCode = models.ForeignKey(CountryCode, on_delete=models.CASCADE, blank=True, null=True, related_name='mobile_number_code')
    preferredNumbermobile = models.BooleanField(default=False)
    preferredNumberwork = models.BooleanField(default=False)
    preferredNumberhome = models.BooleanField(default=False)
    preferredPrimaryEmail = models.BooleanField(default=False)
    preferredAlternateEmail = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Infos"


class AddressInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_address_info')
    permanentAddressSame = models.BooleanField(default=False)

    temp_addressLine1 = models.CharField(max_length=256, blank=True, null=True)
    temp_addressLine2 = models.CharField(max_length=256, blank=True, null=True)
    temp_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='user_temp_country')
    temp_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='user_temp_state')
    temp_city = models.CharField(max_length=256, blank=True, null=True)
    temp_postalCode = models.CharField(max_length=256, blank=True, null=True)

    perm_addressLine1 = models.CharField(max_length=256, blank=True, null=True)
    perm_addressLine2 = models.CharField(max_length=256, blank=True, null=True)
    perm_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='user_perm_country')
    perm_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='user_perm_state')
    perm_city = models.CharField(max_length=256, blank=True, null=True)
    perm_postalCode = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Address Info"
        verbose_name_plural = "Address Infos"


class GovernmentIssuedIDs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_government_ids_info')
    document_type = models.ForeignKey(IDDocumentType, blank=True, null=True, on_delete=models.CASCADE, related_name='government_document_type')
    idName = models.CharField(max_length=256, blank=True, null=True)
    idSize = models.IntegerField(blank=True, null=True)
    idNumber = models.CharField(max_length=256, blank=True, null=True)
    issueDate = models.DateField(max_length=256, blank=True, null=True)
    expiryDate = models.DateField(max_length=256, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True,related_name='government_id_countries')
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True, related_name='government_id_states')
    issueCity = models.CharField(max_length=256, blank=True, null=True)
    documentId = models.CharField(max_length=256, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Government Issued Id Info"
        verbose_name_plural = "Government Issued Id Infos"


class WorkInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_work_info')    
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True,related_name='work_countries')
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    companyName = models.CharField(max_length=256, blank=True, null=True)
    position = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    from_f = models.DateField(max_length=256, blank=True, null=True)
    to = models.DateField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    basePay = models.CharField(max_length=256, blank=True, null=True)
    ctc = models.CharField(max_length=256, blank=True, null=True)
    currency = models.CharField(max_length=256, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Work Info"
        verbose_name_plural = "Work Infos"



class EducationInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_education_info')
    degree = models.ForeignKey(DocumentTypeName, on_delete=models.CASCADE, blank=True, null=True, related_name='education_degree')
    university = models.CharField(max_length=256, blank=True, null=True)
    college = models.CharField(max_length=256, blank=True, null=True)
    from_f = models.DateField(max_length=256, blank=True, null=True)
    to = models.DateField(max_length=256, blank=True, null=True)
    grade = models.CharField(max_length=256, blank=True, null=True)
    cca = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    documentPath = models.CharField(max_length=256, blank=True, null=True)
    documentSize = models.IntegerField(blank=True, null=True)
    document = models.FileField(upload_to='degree/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Education Info"
        verbose_name_plural = "Education Infos"

