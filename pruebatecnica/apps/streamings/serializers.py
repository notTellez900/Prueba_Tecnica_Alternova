from rest_framework import serializers

from .models import CustomerStreaming, Streamings

class StreamingSerializer(serializers.ModelSerializer):
    
    average_rating = serializers.CharField(read_only=True)

    class Meta:
        model = Streamings
        fields = '__all__'
    
    

class CustomerStreamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerStreaming
        fields = '__all__'