from django.db import models

class Record(models.Model):
    name = models.CharField(max_length=70, blank=False, default='')
    recdate = models.DateField(auto_created=False, auto_now_add=False, default='')
    count = models.IntegerField(default=0)
    