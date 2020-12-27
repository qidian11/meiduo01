from django.urls import path
from . import views

urlpatterns = [
    path('usernames/<username>/count/',views.CheckUsernameView.as_view()),
    path('mobiles/<mobile>/count/',views.CheckMobileView.as_view()),
    path('register/',views.RegisterView.as_view())
]