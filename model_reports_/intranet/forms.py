# -*- coding: utf-8 -*-
from django import forms
from intranet.models import SystemPreferences
from django.utils.translation import ugettext_lazy as _

class PatronPhotosForm(forms.Form):
    imagefile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class EditSystemPreferenceForm(forms.Form):
    variable = forms.CharField(required=False,max_length=50,disabled=True)
    value = forms.CharField(
        help_text="Enter value depending on type : Text for Text Type; 0,1,.. for YesNo/Choice; min<=value<=max for MinMax"
        ,max_length=255)
    options = forms.CharField(required=False,max_length=255,disabled=True)
    descriptive_options = forms.CharField(required=False,max_length=1000,disabled=True)
    explanation = forms.CharField(required=False,max_length=255,disabled=True,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}))
    vartype = forms.CharField(required=False,max_length=20,disabled=True) #YesNo - Choice - TextInput

    class Meta:
       model = SystemPreferences
       fields = '__all__'

    def __init__(self,*args,**kwargs):
       self.instance=kwargs.get('instance',None)
       if self.instance is not None:
          del kwargs['instance']
       super(EditSystemPreferenceForm, self).__init__(*args, **kwargs)

    def clean_value(self,*args,**kwargs):
        value = self.cleaned_data['value']
        choices = self.instance.options.split('|')
        vartype = self.instance.vartype
        if vartype=='MinMax':
           min = int(choices[0])
           max = int(choices[1])
           if not (int(value) >= min and int(value) <= max):
               raise forms.ValidationError(
                  _('%(value)s It is not within the valid range [%(min)-%(max)] of values'),
                  params={'value': value,'min':min,'max':max},
               )
        if vartype=='YesNo':
           if int(value) not in [0,1]:
              raise forms.ValidationError(
                  _("%(value)s?  It should be either 0 or 1"),
                  params={'value': value},
              )
        elif vartype=='Choice':
           if not (value in choices):
              raise forms.ValidationError(
                  _('%(value)s? It is not one of valid choices %(choices)s'),
                  params={'value': value,'choices':choices},
              )
        return value
