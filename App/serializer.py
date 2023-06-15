from rest_framework.serializers import ModelSerializer
from .models import Link

class LinkSerializer(ModelSerializer):
    
    class Meta:
        model=Link
        fields= ['id', 'original_link', 'shortened_link', 'count' ]
        read_only_fields = [ 'count']