

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Row, Column, HTML
from crispy_forms.bootstrap import  FormActions

from park_data.models import BookPark, Customer, Park ,ParkImage

class ParkCreateForm(forms.ModelForm):
    
    class Meta:
        model = Park
        fields = [
        'country', 'size_sq_km', 'location', 'established_date','name',
        'history', 'journey_description', 'flora_and_fauna', 'climate', 'booking_info',
    ]
    

    def __init__(self, *args, **kwargs):
        super(ParkCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(

                 HTML(""" <b class="text-dark">About the Park </b> <hr>  """),
             Row(
               
                Column('name'),
                Column('established_date'),
            
            ),
            Row(
                Column( 'country'),
                Column('size_sq_km'),
                Column('location'),
            ),

           

            HTML("""<b class="text-dark"> History of the park and Description </b> <hr>"""),
            Row(
                Column('history'),
                    #    HTML("""<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>""")),
                Column('journey_description'),
            ),
            HTML("""</div> <div class="col-sm-5"> <b class="text-dark"> Flora and Fauna, Climate  </b> <hr>"""),
            Row(
                Column('flora_and_fauna'),
                Column('climate'),
            ),

            HTML("""<b class="text-dark"> Booking to visit  </b> <hr>"""),
            Row(
                Column('booking_info'),
               
            ),
             HTML("""<hr> """),
            FormActions(
                Submit('save', 'Save',css_class='mx-4 px-4 btn btn-success'),
                Submit('Add another', 'Add another',css_class='mx-4 px-4 btn btn-warning'),
            )
        )

class ParkImageForm(forms.ModelForm):
    class Meta:

        model=ParkImage
        fields= ['image', 'caption']

    def __init__(self, *args, **kwargs):
        super(ParkImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                 HTML(""" <b class="text-dark">Upload Your image </b> <hr>  """),
             Row(
               
                Column('image'),   
            
            ),
             HTML(""" <b class="text-dark">More about this image </b> <hr>  """),
            Row(
                Column( 'caption'),
                
            ),

            HTML("""  <hr>  """),

            FormActions(
                Submit('save', 'Save',css_class='mx-4 px-4 btn btn-success'),
                Submit('Add another', 'Add Another',css_class='mx-4 px-4 btn btn-warning'),
            ),
            HTML("""  <hr>  """),
        )



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'middle_name', 'last_name',
            'country','id_or_passport' ,'phone_number', 'email',
            'facebook', 'Twitter', 'instagram',
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML("<h4 class='mb-4'>👤 Personal Details</h4>"),
            Row(
                Column('first_name', css_class='col-md-4'),
                Column('last_name', css_class='col-md-4'),
                Column('middle_name', css_class='col-md-4'),
            ),
            Row(
                Column('country', css_class='col-md-4'),
                
                Column('id_or_passport', css_class='col-md-4'),
            ),
            HTML("<h4 class='mt-4 mb-3'>📧 Contact Information</h4>"),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone_number', css_class='col-md-4'),
            ),
            HTML("<h4 class='mt-4 mb-3'>🌐 Social Media</h4>"),
            Row(
                Column('facebook', css_class='col-md'),
                Column('Twitter', css_class='col-md'),
                Column('instagram', css_class='col-md'),
            ),
            HTML(""" <div class="text-end"> """),
            Submit('submit', 'Save to continue', css_class='btn btn-success text-end mt-3'),
            HTML(""" </div>  """),
        )

class BookingForm(forms.ModelForm):
    class Meta:
        model = BookPark
        fields = ['due_date' ,'message']  # customer will usually be set from request.user or separately
        widgets = {
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'id': 'datepicker',
            }), 

        }
        
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML("<div class='card p-2'> "),
            Row(

                 Column('due_date', css_class='col-md-6'),
            ),
            Row(
                Column('message', css_class='col-md-12'),
            ),
            HTML(""" <div class=" text-end"> """),
            Submit('submit', 'Submit ', css_class='btn btn-success mt-3'),
            HTML(""" </div></div>  """),
        )




# Sending Email form 


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'fw-bold'
        self.helper.field_class = 'mb-3'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-4'),
                Column('email', css_class='col-md-6'),
            ),
           
            'subject',
            'message',

            Submit('submit', 'Send Message', css_class='btn btn-success px-4')
        )