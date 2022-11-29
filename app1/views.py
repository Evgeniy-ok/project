from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse
from .models import Posts
from django.core.files.storage import FileSystemStorage 
import xml.etree.ElementTree as ET 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Главная
def index(request):
    return render(request, 'home.html', {'user': request.user})

# Информация о сайте
def inf(request):
    print('user:', request.user)
    return render(request, 'inf.html')

# Карточки гостей
def guests(request):
    guests = Posts.objects.all()
    return render(request, 'guests.html', {'guests': guests})

# Ликбез
def likbez(request):
    return render(request, 'likbez.html')
    
# Новый гость
def newguest(request):
    name = request.POST.get('name')
    breed = request.POST.get('breed')
    age = request.POST.get('age')
    file = request.FILES['file']
    fss = FileSystemStorage('app1/static/images/')
    saved_file = fss.save(file.name, file)
    

    guest = Posts()
    guest.name = name
    guest.breed = breed
    guest.age = age
    guest.image = file.name
    guest.save()
    return HttpResponseRedirect('/guests')

# О собаке
def dog(request, id):
    dog = Posts.objects.get(id=id)
    return render(request, 'dog.html', {'dog': dog})

# Редактировать пост
def editpost(request, id):
    dog = Posts.objects.get(id=id)
    return render(request, 'editpost.html', {'dog': dog})

# Сохранить пост
def saveeditpost(request, id):
    dog = Posts.objects.get(id=id)
    name = request.POST.get('name')
    breed = request.POST.get('breed')
    age = request.POST.get('age')
    if 'file' in request.FILES:
        file = request.FILES['file']
        fss = FileSystemStorage('app1/static/images/')
        saved_file = fss.save(file.name, file)
        dog.image = file.name
    
    dog.name = name
    dog.breed = breed
    dog.age = age
    

    dog.save()
    return HttpResponseRedirect('/guests')

# Удалить пост
def deletepost(request, id):
    dog = Posts.objects.get(id=id)
    dog.delete()
    return HttpResponseRedirect('/guests')


# Выгрузка
def export(request):
    posts = Posts.objects.all()
    data = ET.Element('data')
    for post in posts:
        element = ET.SubElement(data, 'post')
        element.set('title', post.name)

    ET.ElementTree(data).write("posts.xml", encoding='UTF-8')
    return HttpResponseRedirect('/guests')


# Скачать XML
def download(request):
    f = open('posts.xml', 'rb')
    return FileResponse(f,as_attachment=True)

# Регистрация 
def registration(request):
    
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(name, email, password)
        user.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, "registration.html")

# Вход
def login_user(request):
    
    if request.method =='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login')
    else:
        return render(request, "login.html")

# Выход
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

    
