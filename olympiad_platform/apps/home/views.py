from django.conf import settings
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import translation

from ..courses.models import Course
from ..olympiads.models import Olympiad


def index(request):
    courses = Course.objects.annotate(participant_count=Count('participants')) \
        .select_related('teacher') \
        .order_by('-participant_count')[:6]
    olympiads = Olympiad.objects.annotate(participant_count=Count('participants')).order_by('-participant_count')[:3]
    context = {
        'courses': courses,
        'olympiads': olympiads
    }
    return render(request, 'home/index.html', context)


def is_not_ready(request):
    return render(request, 'home/is_not_ready.html')


def page_not_found(request, exception):
    return render(request, 'home/404-error-page.html', status=404)


def set_language(request, lang_code):
    if lang_code in dict(settings.LANGUAGES):
        translation.activate(lang_code)
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
        return response
    return redirect('home:index')
