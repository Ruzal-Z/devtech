from django.shortcuts import render
from posts.utils import menu


# class ServicesMain:
def services_main(request):
    return render(
        request, 'services/main.html', {'menu': menu, 'title': 'Services'}
    )


def password_generator(request):
    return render(
        request,
        'services/password_generator.html',
        {'menu': menu, 'title': 'Password_Generate'},
    )
