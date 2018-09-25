from django.shortcuts import render


def output(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'articles.html', context)