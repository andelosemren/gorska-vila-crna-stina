from django.urls import path
from . import views
from .views import LoginUser, RegisterUser
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="pocetna"),
    path("onama/", views.onama, name="onama"),
    path("galerija/", views.galerija, name="galerija"),
    path("kucnired/", views.kucnired, name="kucnired"),
    path("login/", views.LoginUser, name="login"),
    path("register/", views.RegisterUser, name="register"), 
    path("logout/", views.LogoutUser, name='logout'),   
    path("booking/", views.booking, name="booking"),
    path('profil/', views.uredi_profil, name='profil'),
    path('chatbot-odgovor/', views.chatbot_odgovor, name='chatbot_odgovor'),
    path('otkazi-rezervaciju/<int:rezervacija_id>/', views.otkazi_rezervaciju, name='otkazi_rezervaciju'),
    path('promijeni-lozinku/', views.promijeni_lozinku, name='promijeni_lozinku'),
    path('reset-lozinke/', auth_views.PasswordResetView.as_view(template_name="aplikacija/reset_lozinke.html"), name="reset_password"),
    path('reset-lozinke/poslano/', auth_views.PasswordResetDoneView.as_view(template_name="aplikacija/reset_poslano.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="aplikacija/reset_potvrda.html"), name="password_reset_confirm"),
    path('reset-lozinke/zavrseno/', auth_views.PasswordResetCompleteView.as_view(template_name="aplikacija/reset_zavrseno.html"), name="password_reset_complete"),
    
]



#pasvord je andelo za superusera