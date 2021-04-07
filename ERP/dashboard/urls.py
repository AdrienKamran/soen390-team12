# Paths to the index page are organized here.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"), # default home view
    path('login/', views.loginPage, name="login"), # login page view
    path('register/', views.register, name="register"), # register page view
    path('logout/', views.logoutUser, name="logout"), # logout page view
    path('generate/', views.generateReport, name='generate'), # generate a report view
    path('get-user-groups/', views.getUserGroups, name='get-user-groups'),
    path('update-user-groups/', views.updateUserGroups, name="update-user-groups"),
]
