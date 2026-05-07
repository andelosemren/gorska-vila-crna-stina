from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    # 1. Eksplicitno dodajemo email polje i kažemo da je obavezno
    email = forms.EmailField(required=True, label=_("Email adresa"))

    class Meta:
        model = User
        # 2. Ovdje govorimo formi koja polja da prikaže (lozinke on doda sam)
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # 3. Provjera postoji li već korisnik s ovim mailom
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Korisnik s ovom email adresom već postoji."))
            
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        # Ovdje smo maknuli ime i prezime, a ubacili username
        fields = ['username', 'email']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }