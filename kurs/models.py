from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon raqam")

    def __str__(self):
        return self.username

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(verbose_name="O'qituvchi haqida")
    avatar = models.ImageField(upload_to='teachers/', blank=True, null=True, verbose_name="Rasm")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Teg nomi")

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="Kurs haqida batafsil")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses', verbose_name="O'qituvchi")
    tags = models.ManyToManyField(Tag, related_name='courses', verbose_name="Teglar")
    image = models.ImageField(upload_to='courses/', verbose_name="Kurs rasmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return self.title
    

    

class Student(models.Model):
   
    full_name = models.CharField(max_length=150, verbose_name="O'quvchi ismi")
    
   
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    
   
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students', verbose_name="Kursi")
    

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
 