from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='')
def Home(request):
    return render(request, 'streamings/streamings_list.html')
    



