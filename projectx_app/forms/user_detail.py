from django import forms
from PIL import Image
from projectx_app.models.user import User
from projectx_app.models.user_detail import *
from django.conf import settings
from django.core.files import File
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from .common_fn import get_initial_values
from .common_fn import get_initial_values

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['last_name'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PersonalInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)

        self.fields['x'].required = False
        self.fields['y'].required = False
        self.fields['width'].required = False
        self.fields['height'].required = False

        self.fields['salutation'].widget.attrs['class'] = 'form-control salutation r-0 light s-12'
        self.fields['gender'].widget.attrs['class'] = 'form-control gender r-0 light s-12'
        
        self.fields['dateOfBirth'].widget.attrs['class'] = 'form-control date-picker dateOfBirth r-0 light s-12'        
        self.fields['dateOfBirth'].widget.attrs['autocomplete'] = "off"

        self.fields['maritalStatus'].widget.attrs['class'] = 'form-control maritalStatus r-0 light s-12'

        self.fields['nameChanged'].widget.attrs['class'] = 'form-control nameChanged r-0 light s-12'

        self.fields['first_name'].widget.attrs['class'] = 'form-control firstName r-0 light s-12'
        self.fields['middleName'].widget.attrs['class'] = 'form-control middleName r-0 light s-12'
        self.fields['last_name'].widget.attrs['class'] = 'form-control lastName r-0 light s-12'
        self.fields['previousName'].widget.attrs['class'] = 'form-control previousName r-0 light s-12'
        self.fields['previousNameStatus'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['beforeMarriage'].widget.attrs['class'] = 'form-control previousNameStatus r-0 light s-12'
        self.fields['fatherFirstName'].widget.attrs['class'] = 'form-control fatherFirstName r-0 light s-12'
        self.fields['fatherMiddleName'].widget.attrs['class'] = 'form-control fatherMiddleName r-0 light s-12'
        self.fields['fatherLastName'].widget.attrs['class'] = 'form-control fatherLastName r-0 light s-12'

        self.fields['motherFirstName'].widget.attrs['class'] = 'form-control motherFirstName r-0 light s-12'
        self.fields['motherMiddleName'].widget.attrs['class'] = 'form-control motherMiddleName r-0 light s-12'
        self.fields['motherLastName'].widget.attrs['class'] = 'form-control motherLastName r-0 light s-12'

        self.fields['spouseFirstName'].widget.attrs['class'] = 'form-control spouseFirstName r-0 light s-12'
        self.fields['spouseMiddleName'].widget.attrs['class'] = 'form-control spouseMiddleName r-0 light s-12'
        self.fields['spouseLastName'].widget.attrs['class'] = 'form-control spouseLastName r-0 light s-12'
        self.fields['profile_pic'].widget.attrs['class'] = 'form-control spouseLastName r-0 light s-12'

    class Meta:
        model = PersonalInfo
        fields = ('__all__')

    def save(self, request, commit=True):
        personalinfo = super(PersonalInfoForm, self).save(commit=False)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if personalinfo.profile_pic:
            image = Image.open(personalinfo.profile_pic)

        if x and y and width and height:
            cropped_image = image.crop((x, y, width+x, height+y))
            resized_image = cropped_image.resize((80, 80), Image.ANTIALIAS)
            resized_image.save('projectx_app/static/img/profile_files/'+personalinfo.profile_pic.name)

        return personalinfo


class ContactInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode = get_initial_values()
        super(ContactInfoForm, self).__init__(*args, **kwargs)

        self.fields['primaryEmail'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['alternateEmail'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['mobileNumber'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['workNumber'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['homeNumber'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['preferredNumber'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['preferredEmail'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['mobileNumberCode'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['mobileNumberCode'].initial = initial_countrycode.id if initial_country_code_exist else ""
        self.fields['preferredNumbermobile'].widget.attrs['class'] = 'form-control form-check-input r-0 light s-12'
        self.fields['preferredNumberwork'].widget.attrs['class'] = 'form-control form-check-input r-0 light s-12'
        self.fields['preferredNumberhome'].widget.attrs['class'] = 'form-control form-check-input r-0 light s-12'
        self.fields['preferredPrimaryEmail'].widget.attrs['class'] = 'form-control form-check-input r-0 light s-12'
        self.fields['preferredAlternateEmail'].widget.attrs['class'] = 'form-control form-check-input r-0 light s-12'

    class Meta:
        model = ContactInfo
        fields = ('__all__')

    def save(self, commit=True):
        instance = super(ContactInfoForm, self).save(commit=False)

        mobileNumber = self.cleaned_data.get('mobileNumber')
        primaryEmail = self.cleaned_data.get('primaryEmail')

        user = User.objects.filter(email = primaryEmail).update(mobile_number = mobileNumber)

        return instance

class AddressInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode = get_initial_values()
        super(AddressInfoForm, self).__init__(*args, **kwargs)
        self.fields['permanentAddressSame'].widget.attrs['class'] = 'form-control form-check-input r-0 light s-12'
        self.fields['temp_addressLine1'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['temp_addressLine2'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['temp_country'].widget.attrs['class'] = 'form-control r-0 light s-12'        
        self.fields['temp_country'].initial = initial_country.id if initial_country_exist else ""
        self.fields['temp_state'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['temp_city'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['temp_postalCode'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['perm_addressLine1'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['perm_addressLine2'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['perm_country'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['perm_country'].initial = initial_country.id if initial_country_exist else ""
        self.fields['perm_state'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['perm_city'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['perm_postalCode'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = AddressInfo
        fields = ('__all__')


class GovernmentIssuedIDsForm(forms.ModelForm):
    idType = forms.CharField(max_length=20, required=False)
    idName = forms.CharField(max_length=30, required=True)

    def __init__(self, *args, **kwargs):
        initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode = get_initial_values()
        super(GovernmentIssuedIDsForm, self).__init__(*args, **kwargs)

        self.fields['document_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['user'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['idType'].widget.attrs['class'] = 'form-control idType r-0 light s-12'
        self.fields['idName'].widget.attrs['class'] = 'form-control idName r-0 light s-12'
        self.fields['idSize'].widget.attrs['class'] = 'form-control idSize r-0 light s-12'
        self.fields['idNumber'].widget.attrs['class'] = 'form-control idNumber r-0 light s-12'
        self.fields['issueDate'].widget.attrs['class'] = 'issueDate form-control date-picker r-0 light s-12'
        self.fields['expiryDate'].widget.attrs['class'] = 'expiryDate form-control date-picker r-0 light s-12'
        self.fields['issueDate'].widget.attrs['input_formats'] = settings.DATE_INPUT_FORMATS
        self.fields['expiryDate'].widget.attrs['input_formats'] = settings.DATE_INPUT_FORMATS

        self.fields['issueDate'].widget.attrs['autocomplete'] = "off"
        self.fields['expiryDate'].widget.attrs['autocomplete'] = "off"

        self.fields['country'].widget.attrs['class'] = 'issueCountry form-control r-0 light s-12'
        self.fields['country'].initial = initial_country.id if initial_country_exist else ""
        self.fields['state'].widget.attrs['class'] = 'issueState form-control r-0 light s-12'

        self.fields['issueCity'].widget.attrs['class'] = 'issueCity form-control r-0 light s-12'
        self.fields['documentId'].widget.attrs['class'] = 'documentId form-control r-0 light s-12'

    class Meta:
        model = GovernmentIssuedIDs
        fields = ('__all__')


class WorkInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkInfoForm, self).__init__(*args, **kwargs)

        self.fields['country'].widget.attrs['class'] = 'form-control country r-0 light s-12'
        self.fields['companyName'].widget.attrs['class'] = 'form-control companyName r-0 light s-12'
        self.fields['position'].widget.attrs['class'] = 'form-control position r-0 light s-12'
        self.fields['location'].widget.attrs['class'] = 'form-control location r-0 light s-12'
        self.fields['from_f'].widget.attrs['class'] = 'from_f form-control date-picker r-0 light s-12'
        self.fields['to'].widget.attrs['class'] = 'to form-control date-picker r-0 light s-12'

        self.fields['from_f'].widget.attrs['autocomplete'] = "off"
        self.fields['to'].widget.attrs['autocomplete'] = "off"

        self.fields['description'].widget.attrs['class'] = 'description form-control r-0 light s-12'
        self.fields['basePay'].widget.attrs['class'] = 'basePay form-control r-0 light s-12'
        self.fields['ctc'].widget.attrs['class'] = 'ctc form-control r-0 light s-12'
        self.fields['currency'].widget.attrs['class'] = 'currency form-control r-0 light s-12'
        self.fields['resume'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = WorkInfo
        fields = ('__all__')


class EducationInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EducationInfoForm, self).__init__(*args, **kwargs)

        self.fields['degree'].widget.attrs['class'] = 'form-control degree r-0 light s-12'
        self.fields['university'].widget.attrs['class'] = 'form-control university r-0 light s-12'
        self.fields['college'].widget.attrs['class'] = 'form-control college r-0 light s-12'
        self.fields['from_f'].widget.attrs['class'] = 'from_f form-control date-picker r-0 light s-12'
        self.fields['to'].widget.attrs['class'] = 'to form-control date-picker r-0 light s-12'

        self.fields['from_f'].widget.attrs['autocomplete'] = "off"
        self.fields['to'].widget.attrs['autocomplete'] = "off"

        self.fields['cca'].widget.attrs['class'] = 'cca form-control r-0 light s-12'
        self.fields['description'].widget.attrs['class'] = 'description form-control r-0 light s-12'
        self.fields['documentPath'].widget.attrs['class'] = 'documentPath form-control r-0 light s-12'
        self.fields['documentSize'].widget.attrs['class'] = 'documentSize form-control r-0 light s-12'
        self.fields['grade'].widget.attrs['class'] = 'grade form-control r-0 light s-12'
        self.fields['document'].widget.attrs['class'] = 'form-control r-0 light s-12'        

        self.fields['degree'].queryset = DocumentTypeName.objects.filter(documenttype__document_type_name__icontains = 'Education Documents').order_by('id')

    class Meta:
        model = EducationInfo
        fields = ('__all__')

