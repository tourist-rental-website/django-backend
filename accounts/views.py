from django.shortcuts import render

def login_view(request):
    
    return render(request, 'accounts/login.html')

def register_view(request):
    context = {
        'title': ("Register"),
        'page_title': ("Register Account"),
        'page_description': ('this is the registration page'),
    }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    return render(request, 'accounts/login.html')