from django import forms
from submissions.models import Submission

class UploadAnswerForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("file",)