from django.db import models
from django.conf import settings

# Create your models here.

ram_choices = (("4GB","4GB"),("6GB","6GB"),("8GB","8GB"))
rom_choices = (("64GB","64GB"),("128GB","128GB"),("256GB","256GB"))
front_cam_choices = (("8px","8px"),("16px","16px"))
back_cam_choices = (("16px","16px"),("32px","32px"),("64px","64px"),("108px","108px"))
network_choices = (("4G","4G"),("5G","5G"))
class Mobile(models.Model):
    name = models.CharField(max_length=100,default=0)
    price = models.IntegerField(default=None)
    description =models.TextField(max_length=500,default=0)
    previewImage = models.ImageField(upload_to="mobile_images/",default=None)
    discountPrice = models.IntegerField(default=0)
    Process = models.CharField(max_length=100,default=0)
    def __str__ (self):
        return f"{self.id}-{self.name}"
    

class Ram(models.Model):
    ram = models.CharField(max_length=100,choices=ram_choices,default=0)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="ram")
    def __str__ (self):
        return f"{self.mobile.name}-{self.ram}"
    

class Rom(models.Model):
    rom = models.CharField(max_length=100,choices = rom_choices,default=0)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="rom")
    def __str__ (self):
        return f"{self.mobile.name}-{self.rom}"
    

class Front_cam(models.Model):
    front_cam = models.CharField(max_length=100,choices = front_cam_choices,default=0)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="front_cam")
    def __str__ (self):
        return f"{self.mobile.name}-{self.front_cam}"
    

class back_cam(models.Model):
    back_cam = models.CharField(max_length=100,choices = back_cam_choices,default=0)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="back_cam")
    def __str__ (self):
        return f"{self.mobile.name}-{self.back_cam}"
    

class mobileImage(models.Model):
    image = models.ImageField(upload_to="mobile_images/")
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="images")
    def __str__ (self):
        return f"{self.mobile.name}-{self.image}"
    

class Network(models.Model):
    mobile_network = models.CharField(max_length=10,choices=network_choices,default=0)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="mobile_network")
    def __str__ (self):
        return f"{self.mobile.name}-{self.mobile_network}"
    


class wishlist(models.Model):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="wishlist")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
        default=None,
    )

    def __str__(self):
        return f"{self.mobile.name} - {self.user.username}"
    

class Cart(models.Model):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="cart")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        default=None,
    )
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.mobile.name}-{self.mobile.id}"




    
