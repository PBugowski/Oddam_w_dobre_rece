from datetime import datetime

from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from .forms import (
    DonateToCharityForm,
    LoginUserForm,
    RegisterUserForm
)

from .models import (
    Category,
    Donation,
    Institution
)

User = get_user_model()


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        donated_bags = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags']
        donated_institutions = Institution.objects.annotate(
            donation_count=Count('donation')).filter(donation_count__gt=0).count()
        FF = Institution.objects.filter(type='FF')
        OP = Institution.objects.filter(type='OP')
        ZL = Institution.objects.filter(type='LZ')
        ctx = {
            'donated_bags': donated_bags,
            'donated_institutions': donated_institutions,
            'FF': FF,
            'OP': OP,
            'ZL': ZL,
        }
        return render(request, 'index.html', ctx)


class AddDonationView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        form = DonateToCharityForm()
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
            'form': form,
        }
        return render(request, 'form.html', ctx)

    def post(self, request):
        form = DonateToCharityForm(request.POST)
        if form.is_valid():
            user = request.user.id
            institution = request.POST['institution']
            donation = Donation.objects.create(**form.cleaned_data, user_id=user, institution_id=institution)
            categories = request.POST.getlist('categories')
            for category in categories:
                donation.categories.add(category)
            return render(request, 'form-confirmation.html')
        else:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            ctx = {
                'categories': categories,
                'institutions': institutions,
                'form': form,
            }
            return render(request, 'form.html', ctx)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        ctx = {'form': form}
        return render(request, 'login.html', ctx)

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("landing-page")
            else:
                return redirect("register")
        return render(request, 'login.html', form)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        ctx = {'form': form}
        return render(request, 'register.html', ctx)

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            del cd['repeat_password']
            cd['username'] = cd['email']
            User.objects.create_user(**form.cleaned_data)
            return render(request, "login.html")
        return render(request, "register.html", ctx)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('landing-page')


class ProfileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        user = request.user
        ctx = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_joined': user.date_joined,
        }
        return render(request, 'profile.html', ctx)


class MyDonationsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        user = request.user
        donations_list = Donation.objects.filter(user_id=user.pk).order_by('pick_up_date', 'pick_up_time')

        for donation in donations_list:
            donation.pick_up_datetime = timezone.make_aware(datetime.combine(donation.pick_up_date, donation.pick_up_time))

        current_time = timezone.now()
        ctx = {
            'donation_list': donations_list,
            'current_time': current_time,
        }
        return render(request, 'my-donations.html', ctx)