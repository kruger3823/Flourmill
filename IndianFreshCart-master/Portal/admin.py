from django.contrib import admin
from . models import Profile,Product,Order,Comment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Comment)