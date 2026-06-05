from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Course, Teacher, Tag, Student
from .forms import CourseForm, StudentForm

def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    
    # Teglar bo'yicha filterlash logikasi
    tag_id = request.GET.get('tag')
    if tag_id:
        courses = courses.filter(tags__id=tag_id)
        
    # Rasmga asosan fayl nomi: 'kurs_list.html'
    return render(request, 'kurs_list.html', {'courses': courses, 'tags': tags})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Agar kurslar uchun alohida html bo'lsa, nomini to'g'rilang yoki kurs_list ichida ishlating
    return render(request, 'kurs_list.html', {'course': course})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    # Rasmda 'teacher_detail.html' bor
    return render(request, 'teacher_detail.html', {'teacher': teacher})

@login_required
def course_add(request):
    if not hasattr(request.user, 'teacher_profile'):
        return redirect('course_list') # '_list' o'rniga to'g'ri url nomi yozildi
        
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.teacher_profile
            course.save()
            form.save_m2m()
            return redirect('course_list')
    else:
        form = CourseForm()
    # Rasmda 'update_form.html' bor
    return render(request, 'update_form.html', {'form': form, 'title': "Yangi Kurs Qo'shish"})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.teacher != request.user.teacher_profile:
        return redirect('course_list')
        
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    # Rasmda 'update_form.html' bor
    return render(request, 'update_form.html', {'form': form, 'title': "Kursni Tahrirlash"})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('course_list')
    else:
        form = AuthenticationForm()
    # Login formasi uchun 'update_form.html' yoki mavjud bo'lsa login.html ishlating
    return render(request, 'update_form.html', {'form': form, 'title': 'Tizimga kirish'})

def logout_view(request):
    auth_logout(request)
    return redirect('course_list')

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save() # Ma'lumotlarni bazaga saqlash
            return redirect('kurs_list') # Kurslar ro'yxatiga qaytarish
    else:
        form = StudentForm()

    return render(request, 'oquvchilar_form.html', {'form': form, 'title': "Yangi O'quvchi Qo'shish"})

def student_list(request):
    students = Student.objects.all().order_by('-joined_at')
    return render(request, 'student_list.html', {'students': students})
