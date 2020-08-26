from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'

# make migrations after setting these additions to the model
# python manage.py makemigrations
# python manage.py migrate
# then go to admins to register the new model


