from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['subject', 'message', 'recipient']
        
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].required = True
        
class EmailReplyForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['message']
