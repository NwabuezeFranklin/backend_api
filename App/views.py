from django.shortcuts import redirect, render
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.response import Response
from django.views import View
from django.conf import settings
from rest_framework import viewsets, status, permissions

from .models import Link
from .serializer import LinkSerializer

class ShortenerListAPIView(viewsets.ModelViewSet):
    # queryset=Link.objects.all()
    serializer_class=LinkSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Link.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class ShortenerCreateApiView(CreateAPIView):
#     serializer_class=LinkSerializer


class Redirector(View):
    def get(self,request,shortener_link,*args, **kwargs):
        shortener_link=settings.HOST_URL+'/'+self.kwargs['shortener_link']
        redirect_link=Link.objects.filter(shortened_link=shortener_link).first().original_link
        return redirect(redirect_link)
