from django.contrib import admin
from .models import Booking 

class BookingAdmin(admin.ModelAdmin):
    # OVO SU STUPCI: Sada se točno poklapaju s tvojim models.py
    list_display = ('user', 'phone_number', 'start_date', 'end_date', 'total_price')
    
    # Filteri s desne strane po datumima dolaska i odlaska
    list_filter = ('start_date', 'end_date')
    
    # Tražilica na vrhu (sada možeš tražiti rezervaciju po broju mobitela ili po korisničkom imenu gosta)
    search_fields = ('phone_number', 'user__username')

admin.site.register(Booking, BookingAdmin)