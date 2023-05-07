from django.urls import path
from .views import Home
from apps.streamings.apiViews import *

urlpatterns = [
    path('', Home, name='index'),
    
    path('getStreamings', get_streamings, name='getStreamings'),
    path('getStreamings/<str:filter_key>', get_streamings, name='getStreamings'),
    path('getRandomStreaming', get_random_streaming, name='getRandomStreaming'),
    path('markAsSeen/<str:key_value>', mark_as_seen, name='markAsSeen'),
    path('rateStreaming/<str:pk>', rate_streaming, name='rateStreaming'),

]