from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Shoe)
admin.site.register(Review)
admin.site.register(Style)
admin.site.register(StyleImage)
admin.site.register(StyleMatch)
admin.site.register(UserStyle)
