from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'
#class ProfileForm(forms.ModelForm):
    #class Meta:
        #model = Profile
        #fields = []
        #widgets = {
           # 'date': DateInput(),
            #'shift':TimeInput()
        #}
        #exclude = ['present','updated']

    # def __init__(self, *args, **kwargs):
       # super(ProfileForm, self).__init__(*args, **kwargs)
        #self.fields['first_name'].widget.attrs['class'] = 'form-control'
        #self.fields['last_name'].widget.attrs['class'] = 'form-control'
        #self.fields['date'].widget.attrs['class'] = 'form-control'
        #self.fields['phone'].widget.attrs['class'] = 'form-control'
        #self.fields['email'].widget.attrs['class'] = 'form-control'
        #self.fields['ranking'].widget.attrs['class'] = 'form-control'
        #self.fields['profession'].widget.attrs['class'] = 'form-control'
        #self.fields['status'].widget.attrs['class'] = 'form-control'
        #self.fields['username'].widget.attrs['class'] = 'form-control'
        #self.fields['shift'].widget.attrs['class'] = 'form-control'
        
        #self.fields['fname'].widget.attrs['class'] = 'form-control'
        #self.fields['lname'].widget.attrs['class'] = 'form-control'
        #self.fields['gender'].widget.attrs['class'] = 'form-control'
        #self.fields['age'].widget.attrs['class'] = 'form-control'
        #self.fields['salary'].widget.attrs['class'] = 'form-control'
        #self.fields['exp'].widget.attrs['class'] = 'form-control'
        #self.fields['role'].widget.attrs['class'] = 'form-control'
        #self.fields['gfrom'].widget.attrs['class'] = 'form-control'
        #self.fields['gyear'].widget.attrs['class'] = 'form-control'
        #self.fields['bcmgpa'].widget.attrs['class'] = 'form-control'
        
        #self.fields['bach'].widget.attrs['class'] = 'form-control'
        #self.fields['msc'].widget.attrs['class'] = 'form-control'
        #self.fields['phd'].widget.attrs['class'] = 'form-control'
        #self.fields['mcmgpa'].widget.attrs['class'] = 'form-control'
        #self.fields['pcmgpa'].widget.attrs['class'] = 'form-control'
      
        
        
        
        