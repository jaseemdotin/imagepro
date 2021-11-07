from django.shortcuts import redirect,render

def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "404.html")
    return wrap

def staff_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "404.html")
    return wrap