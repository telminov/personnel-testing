from django.shortcuts import render


def doc(request):
    return render(request, 'core/doc.html', {'title': 'Инструкция'})