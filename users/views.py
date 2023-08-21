from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator

# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormMixin

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy, reverse

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ProfileForm, CollectorFeedbackForm
from .models import CollectorFeedback

from allauth.account.views import SignupView, LoginView, PasswordResetView


class GoogleSignInView(SignupView):
    template_name = 'users/google-signup.html'


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

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['feedbacks'] = CollectorFeedback.published_objects.filter(user=self.get_object())
        return context


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = User
    template_name = 'users/user-settings.html'
    form_class = ProfileForm
    success_url = '/auth/profile/'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class Collectors(ListView):
    """Список коллекционеров"""
    model = User
    template_name = 'users/collectors.html'
    context_object_name = 'collector_list'


class Collector(FormMixin, DetailView):
    model = User
    template_name = 'users/collector.html'
    context_object_name = 'object'
    form_class = CollectorFeedbackForm

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        feedbacks = CollectorFeedback.published_objects.filter(collector=self.get_object())
        context = super(Collector, self).get_context_data(**kwargs)
        context['feedbacks'] = feedbacks
        context['feedback_provided'] = self.request.user.is_anonymous or feedbacks.filter(user=self.request.user).exists() or self.request.user == self.object
        context['feedback_form'] = CollectorFeedbackForm(
            initial={
                'user': self.request.user,
                'collector': self.object,
            }
        )
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        # form.user = request.user
        # form.collector = self.object
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(Collector, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:collector', kwargs={'id': self.object.id})
