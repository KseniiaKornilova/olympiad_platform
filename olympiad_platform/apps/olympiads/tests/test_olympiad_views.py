import json
from datetime import date, timedelta


from apps.olympiads.models import MultipleChoiceSubmission, OlympiadUser, OneChoiceSubmission, TrueFalseSubmission
from apps.olympiads.tests.factories import OlympiadFactory, OlympiadUserFactory, UserFactory
from apps.olympiads.views import compute_score, update_olympiad_user_ranking

from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils import timezone

import pytest


@pytest.mark.django_db
def test_user_olympiad_list_view(client, user_olympiad):
    user, olympiad = user_olympiad
    client.force_login(user)
    url = reverse_lazy('olympiads:olympiads_list')
    response = client.get(url)

    assert response.status_code == 200
    olympiads = response.context['olympiads']
    assert olympiad in olympiads


@pytest.mark.django_db
def test_user_previous_olympiad_list_view(client, user):
    olympiad = OlympiadFactory(date_of_start=timezone.now() - timedelta(days=10))
    OlympiadUserFactory(user=user, olympiad=olympiad)

    client.force_login(user)
    url = reverse_lazy('olympiads:previous_list')
    response = client.get(url)

    assert response.status_code == 200
    previous_olympiads = response.context['olympiads']
    for olympiad in previous_olympiads:
        assert olympiad.date_of_start.date() < date.today()


@pytest.mark.django_db
def test_user_coming_olympiad_list_view(client, user):
    olympiad = OlympiadFactory(date_of_start=timezone.now() + timedelta(days=10))
    OlympiadUserFactory(user=user, olympiad=olympiad)

    client.force_login(user)
    url = reverse_lazy('olympiads:coming_list')
    response = client.get(url)

    assert response.status_code == 200
    coming_olympiads = response.context['olympiads']
    for olympiad in coming_olympiads:
        assert olympiad.date_of_start.date() > date.today()


@pytest.mark.django_db
def test_olympiad_list_view(client, user, subjects):
    cache.clear()
    math = next(s for s in subjects if s.name == 'Математика')
    chemistry = next(s for s in subjects if s.name == 'Химия')

    for i in range(3):
        OlympiadFactory(stage='Всероссийский', subject=math)
    for i in range(2):
        OlympiadFactory(stage='Школьный', subject=chemistry)

    client.force_login(user)
    url = reverse_lazy('olympiads:olympiads')
    response = client.get(url)

    assert response.status_code == 200
    olympiads = response.context['olympiads']
    assert len(olympiads) == 5

    stage_response = client.get(url, {'stage': 'Всероссийский'})
    assert stage_response.status_code == 200
    filtered_olympiads = stage_response.context['olympiads']
    assert len(filtered_olympiads) == 3
    assert all(o.stage == 'Всероссийский' for o in filtered_olympiads)

    cached_context = cache.get('olympiad_stageВсероссийский')
    assert cached_context is not None
    assert len(cached_context) == 3

    subject_response = client.get(url, {'subject': str(chemistry.id)})
    assert subject_response.status_code == 200
    filtered_olympiads = subject_response.context['olympiads']
    assert len(filtered_olympiads) == 2

    cached_context = cache.get(f'olympiad_subject{chemistry.id}')
    assert cached_context is not None
    assert len(cached_context) == 2


@pytest.mark.django_db
def test_olympiad_page_view(client, user, olympiad):

    client.force_login(user)
    url = reverse_lazy('olympiads:olympiad_page', kwargs={'olympiad_id': olympiad.id})

    cached_context = cache.get(f'olympiad_page{olympiad.id}')
    assert cached_context is None

    response = client.get(url)
    assert response.status_code == 200

    submission = OlympiadUser.objects.get(user=user, olympiad=olympiad)
    assert submission is not None

    cached_context = cache.get(f'olympiad_page{olympiad.id}')
    assert cached_context is not None

    if not submission.is_finished:
        assert 'olympiads/olympiad_page.html' in [template.name for template in response.templates]
    else:
        assert 'olympiads/olympiad_page_results.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_submit_o_question_answer_success(client, user, olympiad):

    client.force_login(user)
    question = olympiad.onechoicequestion_set.first()

    data = {
        'olympiad_id': olympiad.id,
        'question_id': question.id,
        'answer': 'A'
    }

    url = reverse_lazy('olympiads:submit_o_question_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    submission = OneChoiceSubmission.objects.get(student=user, question=question)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Данные успешно обработаны.'

    assert submission.b is False
    assert submission.a is True
    assert submission.students_mark == question.mark


@pytest.mark.django_db
def test_submit_o_question_answer_failure(client, user, olympiad):

    client.force_login(user)
    question = olympiad.onechoicequestion_set.first()

    data = {
        'olympiad_id': olympiad.id,
        'question_id': question.id,
        'answer': 'B'
    }

    url = reverse_lazy('olympiads:submit_o_question_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    submission = OneChoiceSubmission.objects.get(student=user, question=question)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Данные успешно обработаны.'

    assert submission.b is True
    assert submission.a is False
    assert submission.students_mark == 0


@pytest.mark.django_db
def test_submit_o_question_answer_question_not_found(client, user, olympiad):

    client.force_login(user)

    data = {
        'olympiad_id': olympiad.id,
        'question_id': 9999,
        'answer': 'A'
    }

    url = reverse_lazy('olympiads:submit_o_question_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status'] == 'error'
    assert response_data['message'] == 'вопрос не найден'


@pytest.mark.django_db
def test_submit_o_question_answer_invalid_json(client, user):
    client.force_login(user)

    data = 'invalid json'

    url = reverse_lazy('olympiads:submit_o_question_answer')
    response = client.post(url, data=data, content_type='application/json')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status'] == 'error'
    assert response_data['message'] == 'Ошибка при разборе данных JSON.'


@pytest.mark.django_db
def test_submit_t_question_answer_success(client, user, olympiad):

    client.force_login(user)
    question = olympiad.truefalsequestion_set.first()

    data = {
        'olympiad_id': olympiad.id,
        'question_id': question.id,
        'answer': '2'
    }

    url = reverse_lazy('olympiads:submit_t_question_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Данные успешно обработаны.'

    submission = TrueFalseSubmission.objects.get(student=user, question=question)
    assert submission.answer == question.answer
    assert submission.students_mark == question.mark


@pytest.mark.django_db
def test_submit_t_question_answer_failure(client, user, olympiad):

    client.force_login(user)
    question = olympiad.truefalsequestion_set.first()

    data = {
        'olympiad_id': olympiad.id,
        'question_id': question.id,
        'answer': '1'
    }

    url = reverse_lazy('olympiads:submit_t_question_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Данные успешно обработаны.'

    submission = TrueFalseSubmission.objects.get(student=user, question=question)
    assert submission.answer != question.answer
    assert submission.students_mark == 0


@pytest.mark.django_db
def test_submit_t_question_answer_question_not_found(client, user, olympiad):

    client.force_login(user)

    data = {
        'olympiad_id': olympiad.id,
        'question_id': 9999,
        'answer': '1'
    }

    url = reverse_lazy('olympiads:submit_t_question_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status'] == 'error'
    assert response_data['message'] == 'вопрос не найден'


@pytest.mark.django_db
def test_submit_t_question_answer_invalid_json(client, user):

    client.force_login(user)
    data = 'invalid json'

    url = reverse_lazy('olympiads:submit_t_question_answer')
    response = client.post(url, data=data, content_type='application/json')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status'] == 'error'
    assert response_data['message'] == 'Ошибка при разборе данных JSON'


@pytest.mark.django_db
def test_submit_olympiad_answer_success(client, user, olympiad):

    client.force_login(user)
    question = olympiad.multiplechoicequestion_set.first()
    data = {
        'olympiad_id': olympiad.id,
        'student_id': user.id,
        'user_answers': {
            question.id: ['A', 'C', 'E']
        }
    }
    url = reverse_lazy('olympiads:submit_olympiad_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Данные успешно обработаны'

    submission = MultipleChoiceSubmission.objects.get(student=user, question=question)
    assert submission.students_mark == question.mark
    assert submission.a is True
    assert submission.b is False

    olympiad_user = OlympiadUser.objects.get(olympiad=olympiad, user=user)
    assert olympiad_user.is_finished is True


@pytest.mark.django_db
def test_submit_olympiad_answer_failure(client, user, olympiad):

    client.force_login(user)
    question = olympiad.multiplechoicequestion_set.first()
    data = {
        'olympiad_id': olympiad.id,
        'student_id': user.id,
        'user_answers': {
            question.id: ['A', 'C']
        }
    }
    url = reverse_lazy('olympiads:submit_olympiad_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    submission = MultipleChoiceSubmission.objects.get(student=user, question=question)
    assert submission.students_mark == 0

    olympiad_user = OlympiadUser.objects.get(olympiad=olympiad, user=user)
    assert olympiad_user.is_finished is True


@pytest.mark.django_db
def test_submit_olympiad_answer_question_not_found(client, user, olympiad):

    client.force_login(user)
    data = {
        'olympiad_id': olympiad.id,
        'student_id': user.id,
        'user_answers': {
            9999: ['A', 'B'],
        }
    }

    url = reverse_lazy('olympiads:submit_olympiad_answer')
    response = client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status'] == 'error'
    assert response_data['message'] == 'Ошибка при разборе данных JSON.'


@pytest.mark.django_db
def test_compute_score(client, user, olympiad):

    client.force_login(user)
    one_choice_question = olympiad.onechoicequestion_set.first()
    OneChoiceSubmission.objects.create(student=user, question=one_choice_question, students_mark=1)

    multiple_choice_question = olympiad.multiplechoicequestion_set.first()
    MultipleChoiceSubmission.objects.create(student=user, question=multiple_choice_question, students_mark=2)

    try_false_question = olympiad.truefalsequestion_set.first()
    TrueFalseSubmission.objects.create(student=user, question=try_false_question, students_mark=2)

    olympiad_user = OlympiadUser.objects.create(user=user, olympiad=olympiad)
    compute_score(user, olympiad, olympiad_user)
    assert olympiad_user.earned_mark == 5


@pytest.mark.django_db
def test_update_olympiad_user_ranking(user, olympiad):

    user2 = UserFactory()
    user3 = UserFactory()

    submission1 = OlympiadUserFactory(user=user, olympiad=olympiad, earned_mark=90, is_finished=True)
    submission2 = OlympiadUserFactory(user=user2, olympiad=olympiad, earned_mark=80, is_finished=True)
    submission3 = OlympiadUserFactory(user=user3, olympiad=olympiad, earned_mark=95, is_finished=True)

    update_olympiad_user_ranking(olympiad)

    submission1.refresh_from_db()
    submission2.refresh_from_db()
    submission3.refresh_from_db()

    user_ranking = submission1.ranking_place
    user2_ranking = submission2.ranking_place
    user3_ranking = submission3.ranking_place

    assert user3_ranking == 1
    assert user_ranking == 2
    assert user2_ranking == 3


@pytest.mark.django_db
def test_olympiad_registration_success(client, olympiad):

    user = UserFactory()
    client.force_login(user)

    assert not OlympiadUser.objects.filter(user=user, olympiad=olympiad).exists()

    url = reverse_lazy('olympiads:olympiad_registration', kwargs={'olympiad_id': olympiad.id})
    response = client.get(url)
    assert response.status_code == 200
    assert OlympiadUser.objects.filter(user=user, olympiad=olympiad).exists()
    assert response.context['allow_register'] is True


@pytest.mark.django_db
def test_olympiad_registration_already_registered(client, user, olympiad):

    client.force_login(user)
    OlympiadUserFactory(user=user, olympiad=olympiad)
    assert OlympiadUser.objects.filter(user=user, olympiad=olympiad).exists()

    url = reverse_lazy('olympiads:olympiad_registration', kwargs={'olympiad_id': olympiad.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['allow_register'] is False


@pytest.mark.django_db
def test_olympiad_registration_closed(client, olympiad):

    olympiad.registration_dedline = timezone.now() - timezone.timedelta(days=1)
    olympiad.save()

    user = UserFactory()
    client.force_login(user)
    url = reverse_lazy('olympiads:olympiad_registration', kwargs={'olympiad_id': olympiad.id})
    response = client.get(url)

    assert response.status_code == 200

    assert response.context['allow_register'] is True
    assert response.context['result'] is False
    assert not OlympiadUser.objects.filter(user=user, olympiad=olympiad).exists()
