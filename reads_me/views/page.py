from django.shortcuts import render

from reads_me.constants import APP_NAME


def about(request):
    return render(request, f'{APP_NAME}/about.html', {'title': 'About'})
