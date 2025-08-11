from django.urls import path
from accounts.views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
]
