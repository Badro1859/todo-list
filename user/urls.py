from django.urls import path

from django.contrib.auth.views import LogoutView

from . import views

app_name = "user"
urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('activate-user/<uidb64>/<token>',
         views.activate_user, name='activate'),

]
