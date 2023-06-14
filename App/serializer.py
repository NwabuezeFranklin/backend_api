from rest_framework.serializers import ModelSerializer
from .models import Link

class LinkSerializer(ModelSerializer):
    
    class Meta:
        model=Link
        fields= ['id', 'original_link', 'shortened_link', ]
        read_only_fields = ['shortened_link']