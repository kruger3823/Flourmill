from django.db import models
from django.contrib.auth.models import User

usertype_choices = (
    ('1','Customer'),('2','Farmer'),
)
gender_choices = (
    ('1','Male'),('2','Female'),('3','Other'),
)

class Profile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100,default="")
    last_name=models.CharField(max_length=100,default="")
    usertype=models.CharField(max_length=10,default='1')
    gender=models.CharField(max_length=10,choices= gender_choices,default='1')
    date_of_birth= models.CharField(max_length=10,default="")
    city=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=70,default="")
    country=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.first_name+"("+self.usertype+")"


class Product(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    farmer_name=models.CharField(max_length=100,default="")
    product_name=models.CharField(max_length=100,default="")
    product_price=models.FloatField(max_length=10,default="0.0")
    product_desc=models.TextField(default="")
    product_image=models.ImageField(upload_to="product_images/")
    location=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.product_name


class Order(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,default="")
    email=models.EmailField()
    address=models.CharField(max_length=500,default="")
    address_line_2=models.CharField(max_length=500,default="")
    city=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=100,default="")
    pin_code=models.CharField(max_length=10,default="")
    phone_number=models.CharField(max_length=10,default="")
    data=models.TextField(default="")
    total=models.CharField(max_length=200,default="")

    def __str__(self):
        return self.name
class Comment(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=300)

    def __str__(self):
        return self.name





class comp(models.Model):
    jbtitle=models.CharField(max_length=200,null=True)
    jbname=models.CharField(max_length=200,null=True)
    jbdes=models.CharField(max_length=200,null=True)


class report(models.Model):
    jbtitle=models.CharField(max_length=200,null=True)
    jbname=models.CharField(max_length=200,null=True)
    jbdes=models.CharField(max_length=200,null=True)


class delivery(models.Model):
    jbtitle=models.CharField(max_length=200,null=True)
    jbname=models.CharField(max_length=200,null=True)
    jbdes=models.CharField(max_length=200,null=True)



class info(models.Model):
    jbtitle=models.CharField(max_length=200,null=True)
    jbname=models.CharField(max_length=200,null=True)
    jbdes=models.CharField(max_length=200,null=True)
    mob=models.CharField(max_length=200, null=True)