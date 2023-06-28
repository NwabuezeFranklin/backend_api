from django.shortcuts import redirect, render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.views import View
from django.conf import settings
from rest_framework import viewsets, status, permissions
from django.http import HttpResponse  # Import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from .models import Link
from .serializer import LinkSerializer
from random import choices
from string import ascii_letters
from django.conf import settings

from django.core.exceptions import ValidationError

class ShortenerListAPIView(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    
    def get_queryset(self):
        try:
            user = self.request.user.id
            return Link.objects.filter(user=user)
        except:
            return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)
        
        
    @swagger_auto_schema(operation_summary="Create a Shortened Link for the current user. Note that only the original_link field is required.")
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        original_link = serializer.validated_data['original_link']
        if not request.user.is_authenticated:
            return Response("Please login first.", status=status.HTTP_401_UNAUTHORIZED)
    
        # Check if the user already has a link with the same original_link
        if Link.objects.filter(user=user, original_link=original_link).exists():
            return Response("User already has a link with the same original_link.", status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique shortened_link
        while True:
            random_string = ''.join(choices(ascii_letters, k=6))
            new_link = settings.HOST_URL + '/' + random_string
            
            # Check if the shortened_link already exists
            if not Link.objects.filter(shortened_link=new_link).exists():
                break
        
        serializer.save(user=user, shortened_link=new_link)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_summary="Edit the Shortened Link. Note that only the shortened_link field can be modified.")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        shortened_link = serializer.validated_data['shortened_link']
        
        # Check if the user already has a link with the same shortened_link
        if Link.objects.filter(user=instance.user, shortened_link=shortened_link).exclude(pk=instance.pk).exists():
            return Response("User already has a link with the same shortened_link.", status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)



# class ShortenerCreateApiView(CreateAPIView):
#     serializer_class=LinkSerializer


class Redirector(View):
    def get(self, request, shortener_link, *args, **kwargs):
        shortener_link = settings.HOST_URL + '/' + self.kwargs['shortener_link']
        link = Link.objects.filter(shortened_link=shortener_link).first()
        if link:
            link.increase_count()  # Increase the count
            return redirect(link.original_link)
        else:
            return HttpResponse("Link not found", status=404)