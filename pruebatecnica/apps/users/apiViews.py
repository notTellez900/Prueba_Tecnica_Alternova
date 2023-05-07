#librerias de restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import  User

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.response import Response
from rest_framework.authtoken.models import Token

def show_info_data(data, status):
    showdata = {}

    if(status == 200):
        showdata = {
            'message': 'success',
            'result': data,
        }
    else:
        showdata = {
            'message':'error',
            'result': data,
        }

    return showdata

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data = request.data
    email = data['email']
    password = data['password']
    try:
        account = User.objects.get(email=email)
    except BaseException as e:
        return Response(show_info_data({"message": str(e)},400), status=400)

    token = Token.objects.get_or_create(user=account)[0].key
    if not check_password(password, account.password):
        return Response(show_info_data({"message": "Incorrect Login credentials"},400), status=400)

    if account:
        if account.is_active:
            login(request, account)
            return Response(show_info_data({"email": account.email, "token": token},200), status=200)
        else:
            return Response(show_info_data({"message": "Account not active"},400), status=400)
    else:
        return Response(show_info_data({"message": "Account does not exist"},400), status=400)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response(show_info_data({"message": 'User Logged out successfully'},200), status=200)