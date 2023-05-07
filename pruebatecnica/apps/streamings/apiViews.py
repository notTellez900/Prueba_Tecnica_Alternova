import random

#librerias de restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.db.models import F, Q, Case, When, Avg, FloatField

from .models import Streamings, CustomerStreaming
from apps.users.models import Customer

from .serializers import StreamingSerializer, CustomerStreamingSerializer

from apps.users.apiViews import show_info_data



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_streamings(request, filter_key=''):
    if(request.method == 'GET'):

        if(filter_key == '1'):
            queryset = Streamings.objects.all().order_by('-name')
        elif(filter_key == '2'):
            queryset = Streamings.objects.all().order_by('-stream_type')
        elif(filter_key == '3'):
            queryset = Streamings.objects.all().order_by('-gender')
        elif(filter_key == '4'):
            queryset = Streamings.objects.all().order_by('-rating')
        else:
            queryset = Streamings.objects.all().order_by('name','gender','stream_type','rating')
        
        if(len(filter_key) > 1):
            queryset = queryset.filter(
                Q(name__icontains=filter_key) | 
                Q(gender__icontains=filter_key) |
                Q(stream_type__icontains=filter_key)
                )
            
        #Agregar un campo adicional sin la necesidad de estar en el modelo.
        queryset = queryset.annotate(average_rating=Avg(
            Case(When(num_ratings=0, then=0), default= F('rating')/F('num_ratings'), output_field=FloatField())
        ))
        serializer = StreamingSerializer(queryset, many=True)
        return Response(show_info_data(serializer.data, 200), status=200)
    elif(request.method == 'POST'):
        data = request.data
        serializer = StreamingSerializer(data = data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(show_info_data(serializer.data, 200), status=200)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_random_streaming(request):
    if(request.method == 'GET'):
        queryset = Streamings.objects.all()
        queryset = queryset.annotate(average_rating=Avg(
            Case(When(num_ratings=0.00, then=0.00), default= F('rating')/F('num_ratings'), output_field=FloatField())
        ))
        random_id = random.randint(0, len(queryset)-1)
        queryset = queryset[random_id]
        serializer = StreamingSerializer(queryset, many=False)

        return Response(show_info_data(serializer.data, 200), status=200)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_seen(request, key_value):
    if(request.method == 'PUT'):
        queryset = Streamings.objects.get(id = key_value)
        queryset2 = CustomerStreaming.objects.filter(
            Q(user=Customer.objects.get(user_id=request.user.id)) &
            Q(streaming=queryset) 
        )
        data = {
            'num_visualizations': queryset.num_visualizations + 1
        }
        print(queryset)
        if( not queryset2 ):
            
            data2 = {
                'user': Customer.objects.get(user_id=request.user.id),
                'streaming': queryset.id,
                'was_seen': True,
                'is_rated': False
            }
            serializer2 = CustomerStreamingSerializer(data=data2)
        elif(queryset2 and not queryset2[0].was_seen):
            data2 = {
                'user': Customer.objects.get(user_id=request.user.id),
                'streaming': queryset.id,
                'was_seen': True
            }
            serializer2 = CustomerStreamingSerializer(queryset2[0], data=data2)
   
        else:
            return Response(show_info_data({
                'message': 'Streaming already seen'
            }, 400), status=400)
        
        serializer = StreamingSerializer(queryset, data=data)
        if(serializer.is_valid() & serializer2.is_valid()):
            serializer.save()
            serializer2.save()

            return Response(show_info_data({
                'message': 'Succesfully updated'
            }, 200), status=200)
        else:
            return Response(show_info_data({
                'message': 'algopaso',
                'error': serializer2.errors
            }, 400), status=500)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rate_streaming(request, pk):
    
    if(request.method == 'PUT'):
        queryset = Streamings.objects.get(id = pk)
        queryset2 = CustomerStreaming.objects.filter(
            Q(user=Customer.objects.get(user_id=request.user.id)) &
            Q(streaming=queryset) 
        )
        if(int(request.data['rating'])>5 and int(request.data['rating'])<1):
            return Response(show_info_data({
                'message': 'Invalid input'
            },400), status=400)
        data = {
            'rating': int(request.data['rating']) + queryset.rating,
            'num_ratings': queryset.num_ratings + 1
        }
        print(queryset2 and not queryset2[0].is_rated)
        if( not queryset2 ):
            
            data2 = {
                'user': Customer.objects.get(user_id=request.user.id),
                'streaming': queryset.id,
                'was_seen': False,
                'is_rated': True
            }
            serializer2 = CustomerStreamingSerializer(data=data2)
        elif(queryset2 and not queryset2[0].is_rated):
            print(queryset2)
            data2 = {
                'user': Customer.objects.get(user_id=request.user.id),
                'streaming': queryset.id,
                'is_rated': True
            }
            serializer2 = CustomerStreamingSerializer(queryset2[0], data=data2)
   
        else:
            return Response(show_info_data({
                'message': 'Streaming already rated'
            }, 400), status=400)
        
        serializer = StreamingSerializer(queryset, data=data)

        if(serializer.is_valid() & serializer2.is_valid()):
            serializer.save()
            serializer2.save()

            return Response(show_info_data({
                'message': 'Succesfully rated'
            }, 200), status=200)  
        
        else:
            return Response(show_info_data({
                'message': 'Something goes wrong',
                'error': serializer2.errors
            }, 400), status=400)      
        
                

            



        

    