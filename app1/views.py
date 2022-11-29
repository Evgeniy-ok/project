from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Posts
from django.core.files.storage import FileSystemStorage


# Главная
def index(request):
    return render(request, 'home.html')

# Информация о сайте
def inf(request):
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
    editpost = Posts.objects.get(id=id)
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



