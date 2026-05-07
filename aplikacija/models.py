from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator # <--- DODAJ OVO NA VRH

# ... tvoji ostali modeli ako ih imaš ...

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField("Dolazak")
    end_date = models.DateField("Odlazak")
    promokod = models.CharField("promo kod")
    
    # PRAVILO ZA BROJ TELEFONA: Dozvoljava opcionalni '+' na početku i 6 do 15 znamenki
    phone_validator = RegexValidator(
        regex=r'^\+?[0-9]{6,15}$',
        message="Unesite ispravan broj telefona. Dozvoljeni su samo brojevi i znak '+' na početku."
    )
    
    phone_number = models.CharField(
        "Broj mobitela", 
        max_length=20, 
        validators=[phone_validator] 
    )
    
    total_price = models.DecimalField("Ukupna cijena", max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | {self.start_date} - {self.end_date}"
    
