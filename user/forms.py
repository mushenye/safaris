from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,SetPasswordForm,PasswordResetForm


from user.models import CustomUser

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Row, Column, HTML
from crispy_forms.bootstrap import FormActions 


class MyPasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(label='old Password',widget= forms.PasswordInput(attrs={'autofocus': 'True','autocomplete':'current-password','class': 'form-control'}))
    new_password1= forms.CharField(label='New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))



class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))



class MySetPasswordForm(SetPasswordForm):
    new_password1= forms.CharField(label='New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML("<b class='text-dark'> Personal Details</b><hr>"),
            Row(
                Column('username'),
                Column('email'),
            ),
            HTML("<b class='text-dark'> Enter your password - Must Contain (@ # $ % & ?)</b><hr>"),
            Row(
                Column('password1'),
                Column('password2'),
            ),
            HTML("<hr>"),
            FormActions(
                
                Submit('save', 'Save', css_class='mx-4 px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel', css_class='mx-4 px-4 btn btn-sm btn-warning'),
            )
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email



class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout= Layout(
            'username',
            'password',
             FormActions(
                Submit('Login', 'Login', css_class='mx-5 px-4 btn btn-sm btn-success'),
                
            )

        )