from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/")
    color = models.CharField(null=True, blank=True, max_length=200)
    review = models.IntegerField(null=True,blank=True)
    size = models.CharField(null=True, blank=True, max_length=200)
    gender = models.CharField(null=True, blank=True, max_length=200)
    stock = models.IntegerField(null=True,blank=True)

    #product desc = ?

    def __str__(self):
        return self.name
