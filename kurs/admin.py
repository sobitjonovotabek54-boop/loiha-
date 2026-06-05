from django.contrib import admin 
from .models import Course, Teacher, Tag, Student 

# Register your models here.


from django.contrib import admin
from .models import Course, Teacher, Tag, Student 

admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Tag)
admin.site.register(Student)
