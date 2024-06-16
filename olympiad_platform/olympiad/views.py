from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, '404-error-page.html', status=404)
