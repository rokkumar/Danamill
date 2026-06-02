from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
     return render(request, 'about.html')

def quality(request):
     return render(request, 'quality.html')

def products(request):
     return render(request, 'products.html')

def infrastructure(request):
     return render(request, 'infrastructure.html')

def contact(request):
     return render(request, 'contact.html')