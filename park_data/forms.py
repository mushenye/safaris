

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Row, Column, HTML
from crispy_forms.bootstrap import  FormActions

from park_data.models import Park 

class ParkCreateForm(forms.ModelForm):
    
    class Meta:
        model = Park
        fields = [
        'country', 'size_sq_km', 'location', 'established_date', 'name',
        'history', 'description', 'flora_and_fauna', 'climate', 'booking_info',
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
                Column('description'),
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
                Submit('', 'Save',css_class='mx-4 px-4 btn btn-success'),
            )
        )

# 