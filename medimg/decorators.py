from django.http import HttpResponse
from django.shortcuts import redirect
# the decorator let us add fonctions before the view function is called 
def unauthenticated_user(view_func):
    def wrapper_func(request , *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        
        return view_func(request , *args, **kwargs)
    
    return wrapper_func

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request , *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to view this page ')
        return wrapper_func
    return decorator