from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Animal)
admin.site.register(Tip)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Answer)