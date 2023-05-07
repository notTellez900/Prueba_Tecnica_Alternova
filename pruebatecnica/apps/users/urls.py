from django.urls import path
from apps.users.views import *
from apps.users.apiViews import *

urlpatterns = [
    #---------apis APP ---------
    path(r'login', login_user, name='login'),
    path(r'logout', logout_user, name='logout'),


]