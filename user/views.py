from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic.edit import FormView

from .forms import UserCreationForm


class LoginPage(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('base:tasks')


class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('base:tasks')

    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        if user is not None:           
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    ## for redirect authenticated user
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("base:tasks")
        return super().get(request, *args, **kwargs)
