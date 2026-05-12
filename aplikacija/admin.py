from django.contrib import admin
from .models import Booking 
from .models import Recenzija

class BookingAdmin(admin.ModelAdmin):
    # OVO SU STUPCI: Sada se točno poklapaju s tvojim models.py
    list_display = ('user', 'phone_number', 'start_date', 'end_date', 'total_price')
    
    # Filteri s desne strane po datumima dolaska i odlaska
    list_filter = ('start_date', 'end_date')
    
    # Tražilica na vrhu (sada možeš tražiti rezervaciju po broju mobitela ili po korisničkom imenu gosta)
    search_fields = ('phone_number', 'user__username')

admin.site.register(Booking, BookingAdmin)



@admin.register(Recenzija)
class RecenzijaAdmin(admin.ModelAdmin):
    # Što želimo vidjeti u tablici
    list_display = ('ime_gosta', 'ocjena', 'datum', 'odobreno')
    
    # OVO JE MAGIJA: Omogućava ti da staviš kvačicu za odobrenje bez ulaska u samu recenziju!
    list_editable = ('odobreno',) 
    
    # Filteri sa strane (npr. prikaži mi samo neodobrene ili samo one s 5 zvjezdica)
    list_filter = ('odobreno', 'ocjena', 'datum')
    
    # Polje za pretraživanje po imenu gosta
    search_fields = ('ime_gosta', 'tekst')