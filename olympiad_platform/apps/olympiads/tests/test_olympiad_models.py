from abc import ABC, abstractmethod
from datetime import timedelta

from apps.olympiads.models import MultipleChoiceQuestion, MultipleChoiceSubmission, Olympiad, OlympiadUser, \
    OneChoiceQuestion, OneChoiceSubmission, Subject, TrueFalseQuestion, TrueFalseSubmission
from apps.students.models import User

from django.core.exceptions import ValidationError
from django.utils import timezone

import pytest


@pytest.fixture
def olympiad():
    subject = Subject.objects.create(name='Биология')
    return Olympiad.objects.create(
            title='Олимпиада Ломоносова',
            subject=subject,
            description='Тестовое описание',
            stage='Школьный',
            degree=9,
            date_of_start=timezone.now(),
            registration_dedline=timezone.now() + timedelta(days=2),
            total_mark=100,
    )


@pytest.fixture
def user():
    return User.objects.create_user(
        email='ivanov@.com',
        password='password123',
        first_name='Иван',
        last_name='Иванов',
        status='s',
        degree=10,
        degree_id='a'
    )


@pytest.mark.django_db
class TestSubjectModel:
    def setup_method(self):
        self.subject = Subject.objects.create(name='Математика')

    def test_str_method(self):
        assert str(self.subject) == 'Математика'

    def test_unique_name(self):
        with pytest.raises(ValidationError):
            duplicate_subject = Subject(name='Математика')
            duplicate_subject.full_clean()
            duplicate_subject.save()

    def test_name_max_length(self):
        long_name = 'a' * 51
        subject = Subject(name=long_name)
        with pytest.raises(ValidationError):
            subject.full_clean()


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad')
class TestOlympiadModel:
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad):
        self.olympiad = olympiad

    def test_str_method(self):
        assert str(self.olympiad) == 'Олимпиада Ломоносова'

    def test_is_registration_open(self):
        assert self.olympiad.is_registrations_open() is True

        self.olympiad.registration_dedline = timezone.now() - timedelta(days=1)
        self.olympiad.save()
        assert self.olympiad.is_registrations_open() is False

    def test_unique_title(self):
        with pytest.raises(ValidationError):
            duplicate_olympiad = Olympiad(
                title='Олимпиада Ломоносова',
                subject=Subject(name='Биология'),
                degree=9,
                date_of_start=timezone.now(),
                registration_dedline=timezone.now() + timedelta(days=2),
                total_mark=100,
            )
            duplicate_olympiad.full_clean()


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad')
class TestOlympiadUserModel:
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad):
        self.user = User.objects.create(email='ivanov@gmail.com', password="testpassword")
        self.olympiad = olympiad
        self.olympiad_user = OlympiadUser.objects.create(
            user=self.user,
            olympiad=self.olympiad,
            registration_date=timezone.now()
        )

    def test_default_values(self):
        assert self.olympiad_user.is_finished is False
        assert self.olympiad_user.earned_mark is None
        assert self.olympiad_user.ranking_place is None


@pytest.mark.django_db
class BaseTestQuestionModel(ABC):
    @pytest.fixture(autouse=True)
    @abstractmethod
    def setup_method(self):
        pass

    def test_str_method(self):
        assert str(self.question) == f'{self.question.description}'

    def test_question_wrong_data(self):
        with pytest.raises(ValidationError):
            self.question.question_num = -1
            self.question.full_clean()

        with pytest.raises(ValidationError):
            self.question.mark = -1
            self.question.full_clean()


@pytest.mark.django_db
class BaseTestSubmissionModel(ABC):
    @pytest.fixture(autouse=True)
    @abstractmethod
    def setup_method(self):
        pass

    def test_str_method(self):
        assert str(self.submission) == f'{self.submission.student} : {self.submission.question}'

    def test_negative_mark(self):
        with pytest.raises(ValidationError):
            self.submission.students_mark = -1
            self.submission.full_clean()


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad')
class TestMultipleChoiceQuestionModel(BaseTestQuestionModel):
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad):
        self.olympiad = olympiad
        self.question = MultipleChoiceQuestion.objects.create(
            question_num=1,
            title='Вопрос 1',
            description='Перечислите нуклеотиды ДНК?',
            a='A',
            a_is_correct=True,
            b='G',
            b_is_correct=True,
            c='C',
            c_is_correct=True,
            d='K',
            d_is_correct=False,
            mark=10,
            olympiad=self.olympiad
        )


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad', 'user')
class TestMultipleChoiceSubmissionModel(BaseTestSubmissionModel):
    @pytest.fixture(autouse=True)
    def setup_method(self, user, olympiad):
        self.question = MultipleChoiceQuestion.objects.create(
            question_num=1,
            title='Вопрос 1',
            description='Перечислите нуклеотиды ДНК?',
            a='A',
            a_is_correct=True,
            b='G',
            b_is_correct=True,
            c='C',
            c_is_correct=True,
            d='K',
            d_is_correct=False,
            mark=10,
            olympiad=olympiad
        )

        self.submission = MultipleChoiceSubmission.objects.create(
            a=True,
            b=True,
            c=True,
            student=user,
            question=self.question,
            students_mark=10
        )

    def test_default_values(self):
        assert self.submission.a is True
        assert self.submission.b is True
        assert self.submission.c is True
        assert self.submission.d is False
        assert self.submission.e is False
        assert self.submission.f is False


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad')
class TestOneChoiceQuestionModel(BaseTestQuestionModel):
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad):
        self.question = OneChoiceQuestion.objects.create(
            question_num=1,
            title='Вопрос 1',
            description='Бактерии это:',
            a='прокариоты',
            a_is_correct=True,
            b='эукариоты',
            b_is_correct=False,
            c='сумчатые',
            c_is_correct=False,
            d='вирусы',
            d_is_correct=False,
            mark=5,
            olympiad=olympiad
        )


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad', 'user')
class TestOneChoiceSubmissionModel(BaseTestSubmissionModel):
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad, user):
        self.question = OneChoiceQuestion.objects.create(
            question_num=1,
            title='Вопрос 1',
            description='Бактерии это:',
            a='прокариоты',
            a_is_correct=True,
            b='эукариоты',
            b_is_correct=False,
            c='сумчатые',
            c_is_correct=False,
            d='вирусы',
            d_is_correct=False,
            mark=5,
            olympiad=olympiad
        )

        self.submission = OneChoiceSubmission.objects.create(
            a=True,
            student=user,
            question=self.question,
            students_mark=5
        )

    def test_default_values(self):
        assert self.submission.a is True
        assert self.submission.b is False
        assert self.submission.c is False
        assert self.submission.d is False


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad', 'user')
class TestTrueFalseQuestionModel(BaseTestQuestionModel):
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad):
        self.question = TrueFalseQuestion.objects.create(
            question_num=1,
            title='Вопрос 1',
            description='Выберите верное утверждение:',
            first_statement='Кислород переносится гемоглобином',
            second_statement='Кислород переносится миоглобином',
            answer='1',
            mark=10,
            olympiad=olympiad
        )


@pytest.mark.django_db
@pytest.mark.usefixtures('olympiad', 'user')
class TestTrueFalseSubmissionModel(BaseTestSubmissionModel):
    @pytest.fixture(autouse=True)
    def setup_method(self, olympiad, user):
        self.question = TrueFalseQuestion.objects.create(
            question_num=1,
            title='Вопрос 1',
            description='Выберите верное утверждение:',
            first_statement='Кислород переносится гемоглобином',
            second_statement='Кислород переносится миоглобином',
            answer='1',
            mark=10,
            olympiad=olympiad
        )

        self.submission = TrueFalseSubmission.objects.create(
            answer='1',
            students_mark=5,
            student=user,
            question=self.question
        )
