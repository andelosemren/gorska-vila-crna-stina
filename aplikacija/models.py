from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator # <--- DODAJ OVO NA VRH
from django.core.validators import MinValueValidator, MaxValueValidator

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
    



class Recenzija(models.Model):
    ime_gosta = models.CharField(max_length=100, verbose_name="Ime i prezime")
    tekst = models.TextField(verbose_name="Dojam o boravku")
    ocjena = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Ocjena (1-5)"
    )
    odobreno = models.BooleanField(default=False, verbose_name="Odobreno za prikaz")
    datum = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recenzija"
        verbose_name_plural = "Recenzije"
        ordering = ['-datum'] # Najnovije idu prve

    def __str__(self):
        return f"{self.ime_gosta} - {self.ocjena} zvjezdica"
