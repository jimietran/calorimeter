from django.contrib.auth.models import User
from calorimeter_site.models import UserProfile
from django import forms
from django.forms import ModelForm, Form

class UserForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'age', 'gender', 'weight', 'height')

class ChangePasswordForm(forms.Form):

	newpassword1 = forms.CharField(max_length=100)
	newpassword2 = forms.CharField(max_length=100)

	def clean(self):
		data = self.cleaned_data
		if "newpassword1" in data and "newpassword2" in data:
			if data["newpassword1"] != data["newpassword2"]:
				raise forms.ValidationError(("The two password fields did not match!"), code="invalid")
		return data
