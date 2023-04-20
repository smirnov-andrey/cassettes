from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator

# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView, DetailView, UpdateView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy, reverse

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ProfileForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('users:profile')
    template_name = 'users/signup.html'


    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class Profile(DetailView):
    model = User
    template_name = 'users/user-profile.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = User
    template_name = 'users/user-settings.html'
    form_class = ProfileForm
    success_url = '/auth/profile/'

    def get_object(self, queryset=None):
        user = self.request.user
        return user
