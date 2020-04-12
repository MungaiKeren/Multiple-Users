from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating users"""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)
    
    def clean_password2(self):
        # check that the two password fields match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 !== password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
    
    def save(self, commit=True):
        # save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email","password","active","admin")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value
        # This is done here rather than on the field, 
        # because the field does not have the initial value 
        return self.initial["password"]
        