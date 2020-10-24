from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import logout as do_logout, authenticate, login as do_login
from .forms import LoginForm, FilterForm, DetailForm
from .models import Estate, City, RentDate, Reservation, Service
from datetime import datetime
from decimal import *
from django.db.models import Count
from airbnb.settings import DATE_INPUT_FORMATS, EMAIL_FROM
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

def index(request):
    cities = City.objects.all()
    rentDates = RentDate.objects.all()
    form = FilterForm()
    return render(request, 'myapp/filter.html',{'cities':cities,'rentDates':rentDates, 'form':form})

def home(request):
    form = FilterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            estates = Estate.objects.filter(
                city=request.POST['city']
            ).filter(
                rentdate__dateFrom__gte=request.POST['dateFrom'], 
                rentdate__dateTo__lte=request.POST['dateTo'],
                rentdate__reservation__isnull=True,
                pax__gte=request.POST['pax']
            ).distinct()
            return render(request, 'myapp/home.html', {'estates': estates})
        else:
            return render(request, 'myapp/filter.html', {'form': form})
    else:
        return redirect('/')


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    do_login(request, user)
                    return redirect('/admin/')
        return render(request, 'myapp/login.html', {'form': form})


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def reservations(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            rents_per_reservation = []
            reservations = Reservation.objects.filter(
                rentdate__estate__owner__id= request.user.id
            ).distinct().order_by('code')
            for r in reservations:
                rents = RentDate.objects.filter(reservation=r.id) #array de fechas de alquiler con id de reserva
                rents_per_reservation.append(rents)#array de array
            return render(request, 'myapp/reservations.html',{'rents_per_reservation': rents_per_reservation})
    return redirect('/admin/')


def detail(request, id=0):   
    form = DetailForm(id)
    if request.method == "GET":
        estate = Estate.objects.get(id=id)
        services = Service.objects.filter(estate=id)
        return render(request,'myapp/product_detail.html', {'estate':estate, 'form':form, 'services':services,})  
    return redirect('/')

def thanks(request, id=0):
    if request.method == "POST":
        
        form = DetailForm(data=request.POST, estateId=id)
           
        prop = Estate.objects.get(id=id)
        cod = datetime.today().strftime('%y-%m-%d-%H-%M-%S') + "-" + str(id) + "-" + str(prop.user.id)
        getcontext().prec = 10
        total = (prop.dailyRate * form['date'].value().__len__()) * Decimal(1.08)
        user = form['user'].value()
        email = form['email'].value()
        city = prop.city.title
        r = Reservation(code=cod, user=user, total=total)
        r.save()
        
        for i in form['date'].value():
            dte = int(i)
            rd = RentDate.objects.get(id=dte)
            rd.reservation = r
            rd.save()
        finalDates = RentDate.objects.filter(reservation=r.id)
        
        # SENDING EMAIL
        subject = 'Su reserva en MiniAirbnb ha sido realizada exitosamente'
        temp = 'myapp/email.html'
        ctx = {
            "user": user,
            "total": total,
            "prop": prop.title,
            "code": cod,
            "pax": prop.pax,
            "dates": finalDates,
            "city": city,
        }
        html_content = render_to_string(temp, ctx)
        msg = EmailMultiAlternatives(subject, html_content, EMAIL_FROM, to=[email,])
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()
        return render(request,'myapp/thanks.html', {'form':form, 'estate':prop, 'reservation':r, 'dates':finalDates, 'total':round(r.total, 2)},)  
    return redirect('/')

