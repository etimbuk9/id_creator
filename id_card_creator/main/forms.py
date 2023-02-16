from django.forms import Form, CharField, ChoiceField, FileField, FileInput, ModelChoiceField
from .models import Programme, Level

class IDCardForm(Form):
    first_name= CharField()
    last_name = CharField()
    department = ModelChoiceField(queryset=Programme.objects.all())
    level = ModelChoiceField(queryset=Level.objects.all())
    user_number = CharField()
    # level = 
    photo = FileField(widget=FileInput(attrs={'accept':'image/*'}))
