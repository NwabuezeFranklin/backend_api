from django.db import models
from random import choices
from string import ascii_letters
from django.conf import settings

class Link(models.Model):
    id = models.AutoField(primary_key=True)
    original_link=models.CharField(max_length=2550)
    shortened_link=models.URLField(blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(default=0, editable=False)


    def shortener(self):
        while True:
            random_string=''.join(choices(ascii_letters,k=6))
            new_link=settings.HOST_URL+'/'+random_string
    
            if not Link.objects.filter(shortened_link=new_link).exists():
                break

        return new_link
    
    
    def get_count(self):
        return self.count

    def save(self,*args, **kwargs):
        if not self.shortened_link:
            new_link=self.shortener()
            self.shortened_link=new_link
        return super().save(*args, **kwargs)
    
    
    def increase_count(self):
        self.count += 1
        self.save()
