from apps.olympiads.models import MultipleChoiceQuestion, OneChoiceQuestion, TrueFalseQuestion
from apps.olympiads.tests.factories import OlympiadFactory, OlympiadUserFactory, SubjectFactory, UserFactory

import pytest


@pytest.fixture(scope='function')
def subjects():
    subjects_list = ['Биология', 'Математика', 'Химия', 'Информатика']
    return [SubjectFactory(name=name) for name in subjects_list]


@pytest.fixture(scope='function')
def olympiad(subjects):
    olympiad = OlympiadFactory(subject=subjects[0], stage='Областной')

    OneChoiceQuestion.objects.create(
        olympiad=olympiad,
        question_num=1,
        a="Красный", a_is_correct=True,
        b="Синий", b_is_correct=False,
        c="Зеленый", c_is_correct=False,
        d="Черный", d_is_correct=False,
        mark=1
    )

    MultipleChoiceQuestion.objects.create(
        olympiad=olympiad,
        question_num=1,
        a="Кит", a_is_correct=True,
        b="Дельфин", b_is_correct=False,
        c="Акула", c_is_correct=True,
        d="Скат", d_is_correct=False,
        e="Слон", e_is_correct=True,
        f="Крокодил", f_is_correct=False,
        mark=2
    )

    TrueFalseQuestion.objects.create(
        olympiad=olympiad,
        question_num=1,
        first_statement="Солнце вращается вокруг Земли",
        second_statement="Земля вращается вокруг Солнца",
        answer='2',
        mark=2
    )

    return olympiad


@pytest.fixture(scope='function')
def user():
    return UserFactory()


@pytest.fixture(scope='function')
def user_olympiad(user, olympiad):
    OlympiadUserFactory(user=user, olympiad=olympiad)
    return user, olympiad
