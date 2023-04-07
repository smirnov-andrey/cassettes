from django.contrib.auth import get_user_model
from django.shortcuts import render

# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView, DetailView, UpdateView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ProfileForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class Profile(DetailView):
    model = User
    template_name = 'users/user-profile.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class ProfileUpdate(UpdateView):
    model = User
    template_name = 'users/user-settings.html'
    form_class = ProfileForm
    success_url = '/auth/profile/'

    def get_object(self, queryset=None):
        user = self.request.user
        return user
