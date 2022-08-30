
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from user.utils import generate_token, send_activation_email

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic.edit import FormView

from user.models import CustomUser
from user.forms import UserCreationForm, CustomAuthenticationForm


class LoginPage(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    form_class = CustomAuthenticationForm
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
            if user.is_email_verified:
                login(self.request, user)
            else:
                send_activation_email(user, self.request)

        return super(RegisterPage, self).form_valid(form)

    # for redirect authenticated user
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("base:tasks")
        return super().get(request, *args, **kwargs)


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        login(request, user)

        return redirect('base:tasks')

    return render(request, 'user/activate-failed.html', {"user": user})
