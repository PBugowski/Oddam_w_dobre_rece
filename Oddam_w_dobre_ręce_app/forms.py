from django import forms
from django.contrib.auth.models import User


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Imię", max_length=100, required=True)
    last_name = forms.CharField(label="Nazwisko", max_length=100, required=True)
    email = forms.EmailField(label="Adres email", required=True)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput, required=True)
    repeat_password = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "repeat_password",
        ]


class LoginUserForm(forms.Form):
    email = forms.EmailField(label="Adres email")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class DonateToCharityForm(forms.Form):
    quantity = forms.IntegerField()
    address = forms.CharField(max_length=128)
    phone_number = forms.IntegerField()
    city = forms.CharField(max_length=128)
    zip_code = forms.CharField(max_length=6)
    pick_up_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'RRRR-MM-DD'}))
    pick_up_time = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': '--:--'}))
    pick_up_comment = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), required=False)
