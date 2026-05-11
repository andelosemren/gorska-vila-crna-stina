import json
from datetime import datetime, date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse

from .models import Booking
from .forms import RegisterForm, UserEditForm
# Create your views here.

def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
   

        if username and password:
            user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pocetna') 
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'aplikacija/login.html')

def RegisterUser(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # Prvo spremimo korisnika
            
            # SLANJE EMAILA DOBRODOŠLICE
            naslov = 'Dobrodošli u Gorsku Vilu Crna Stina'
            poruka = f'Poštovani {user.username},\n\nHvala vam na registraciji! Dobrodošli u našu luksuznu oazu mira. Vaš profil je uspješno kreiran i sada možete rezervirati svoj termin.\n\nVaša Gorska Vila Crna Stina.'
            
            try:
                send_mail(
                    naslov,
                    poruka,
                    'luxurycrnastina@gmail.com', # S kojeg maila šalješ
                    [user.email], # Na koji mail šalješ (onaj koji je korisnik upisao)
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Greška pri slanju maila: {e}") # Ako mail ne prođe, da aplikacija ne pukne
            
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "aplikacija/register.html", {'form':form})

def LogoutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('pocetna')
    return redirect('pocetna')

@login_required
def booking(request):
    if request.method == "POST":
        start_str = request.POST.get("start_date")
        end_str = request.POST.get("end_date")
        phone = request.POST.get("phone_number")
        promoKod = request.POST.get("promokod")

        if start_str and end_str and phone and promoKod:
            start_date= datetime.strptime(start_str, '%Y-%m-%d',).date()
            end_date= datetime.strptime(end_str, '%Y-%m-%d').date()

            if start_date >= end_date:
                messages.error(request, "Datum odlaska mora biti nakon datuma dolaska.")
                return redirect("booking")
            
            preklapanje = Booking.objects.filter(
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()

            if preklapanje:
                messages.error(request, "Žao nam je, vila je već rezervirana u odabranom terminu.")
                return redirect("booking")
            
            broj_noci = (end_date - start_date).days
            
            if broj_noci >= 10:
                cijena_po_noci = 200
            elif broj_noci >= 5:
                cijena_po_noci = 250
            elif broj_noci >= 3:
                cijena_po_noci = 300
            else:
                cijena_po_noci = 500
                
            ukupna_cijena = broj_noci * cijena_po_noci

            Booking.objects.create(
                user=request.user,
                start_date=start_date,
                end_date=end_date,
                phone_number=phone,
                total_price=ukupna_cijena
            )
            
            messages.success(request, f"Bravo! Uspješno ste rezervirali vilu. Cijena za {broj_noci} noći iznosi {ukupna_cijena} €.")
            return redirect("booking")
    sve_rezervacije = Booking.objects.all()
    zauzeti_datumi = []

    for rez in sve_rezervacije:
        zauzeti_datumi.append({
            "from": str(rez.start_date),
            "to": str(rez.end_date)
        })

    context = {
        "zauzeti_datumi_json": json.dumps(zauzeti_datumi)
    }

    return render(request, "aplikacija/booking.html", context)
def home(request):
    return render(request,"aplikacija/home.html")

def onama(request):
    return render(request,'aplikacija/onama.html')

def kucnired(request):
    return render(request,'aplikacija/kucnired.html')

def galerija(request):
    return render(request,'aplikacija/galerija.html')

def registrirajSe(request):
    return render(request,'aplikacija/registracija.html')

@login_required  # Samo prijavljeni korisnici mogu vidjeti ovo
def uredi_profil(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/') # Ili ga vrati na profil
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'aplikacija/profil.html', {'form': form})


@login_required 
def uredi_profil(request):
    # Dohvaćamo sve rezervacije ovog korisnika (najnovije prve)
    moje_rezervacije = Booking.objects.filter(user=request.user).order_by('-id')

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profil/') # Ostavljamo ga na profilu da vidi izmjene
    else:
        form = UserEditForm(instance=request.user)
    
    # Šaljemo i formu i rezervacije u profil.html
    return render(request, 'aplikacija/profil.html', {
        'form': form,
        'rezervacije': moje_rezervacije
    })

# NOVA FUNKCIJA ZA OTKAZIVANJE
@login_required
def otkazi_rezervaciju(request, rezervacija_id):
    # Tražimo rezervaciju, ali samo ako pripada ovom korisniku (sigurnost!)
    rezervacija = get_object_or_404(Booking, id=rezervacija_id, user=request.user)
    
    if request.method == 'POST':
        # Opcija 1: Brisanje iz baze
        rezervacija.delete()
        
        # Opcija 2 (Bolja za statistiku): Ako imaš polje 'status' u modelu, onda umjesto delete() staviš:
        # rezervacija.status = 'Otkazano'
        # rezervacija.save()
        
    return redirect('/profil/')


@login_required
def promijeni_lozinku(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Ovo je ključno: Django te inače izbaci kad promijeniš lozinku. 
            # Ova linija ispod mu kaže "Nemoj ga odjaviti, samo mu osvježi sesiju!"
            update_session_auth_hash(request, user) 
            messages.success(request, 'Vaša lozinka je uspješno promijenjena!')
            return redirect('profil')
        else:
            messages.error(request, 'Molimo ispravite greške ispod.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'aplikacija/promijeni_lozinku.html', {'form': form})

def chatbot_odgovor(request):
    if request.method == "POST":
        try:
            # Čitamo podatke u modernom JSON formatu
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user_poruka = body_data.get('poruka')
            
            genai.configure(api_key=settings.AI_API_KEY)
            
            # PROŠIRENO ZNANJE BOTA
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction="""
                Ti si ekskluzivni asistent luksuzne vile 'Gorska Vila Crna Stina'.
                Tvoj ton je profesionalan, uslužan i srdačan. Odgovaraj na hrvatskom jeziku.
                
                INFORMACIJE O VILI:
                - Lokacija: Livno, Bosna i Hercegovina. Oaza mira u prirodi.
                - Sadržaj: Vila nudi vrhunski vanjski bazen, modernu opremu i unikatni hrastov blagovaonski stol s epoksijem.
                - Cijene noćenja: 
                  * 1 do 2 noći = 500 € po noći
                  * 3 do 4 noći = 300 € po noći
                  * 5 do 9 noći = 250 € po noći
                  * 10 i više noći = 200 € po noći
                - Dodatni troškovi: Jednokratna naknada za čišćenje iznosi 50 €.
                - Popusti: Za rezervacije od 7 ili više noćenja, gosti ostvaruju 10% popusta na ukupnu cijenu.
                - Nagrade: Imamo aktualnu nagradnu igru i poklon bon u iznosu od 1000 KM.
                - Rezervacije: Uvijek uputi goste da koriste kalendar na web stranici za odabir datuma.
                
                Pravila ponašanja: Odgovaraj kratko (maksimalno 2-3 rečenice), jasno i bez previše kompliciranja. Ako ne znaš odgovor, uputi gosta da ispuni kontakt formu.
                """
            )

            response = model.generate_content(user_poruka)
            return JsonResponse({'odgovor': response.text})
            
        except Exception as e:
            return JsonResponse({'odgovor': "Oprostite, trenutno ažuriram sustav. Molim Vas pokušajte ponovno za par sekundi."}, status=500)

    return JsonResponse({'odgovor': 'Pogrešan zahtjev.'}, status=400)