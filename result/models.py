from django.db import models
from django.contrib.postgres.indexes import BrinIndex

from exam.models import ExamQuestion, Exam
from questions.models import Subject, Question
from result.utils import data_parser


class UserManager(models.Manager):

    def get_or_create_user(self, name, email):
        try:
            obj, created = User.objects.get_or_create(name=name, email=email)
            return obj
        except Exception as e:
            return False


class User(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=256)

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]

    def __str__(self):
        return "Username: {}".format(self.name)


class UserAnswerManager(models.Manager):

    def store_user_answer(self, session_data, requested_data):
        try:
            user = User.objects.get(id=session_data['user_id'])
            exam = Exam.objects.get(id=session_data['exam_id'])

            time_spent = data_parser.get_spent_time(requested_data['total_time'], exam, requested_data['question'])
            print(time_spent)
            answered_object = self.create(user=user, exam=exam, question=requested_data['question'],
                                          answer=requested_data.get('user_answer', ''), time_spent=time_spent)
            if answered_object:
                question_object = Question.objects.get(question=requested_data['question'])
                user_result, created = UserResult.objects.get_or_create(user=user, exam=exam)
                if requested_data.get('user_answer', '') == question_object.answer:
                    user_result.score += 1
                    user_result.total_time_spent += time_spent
                    user_result.save()
                else:
                    user_result.total_time_spent += time_spent
                    user_result.save()
            return answered_object
        except Exception as e:
            print(e)
            return False

    def get_user_answer(self, session_data):
        return self.filter(user=session_data['user_id'], exam=session_data['exam_id'])


class UserAnswer(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, default="")
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=100, default="")
    time_spent = models.IntegerField()

    objects = UserAnswerManager()

    class Meta:
        indexes = [
            BrinIndex(fields=['id'])
        ]

    def __str__(self):
        return "{} || Answer: {}".format(self.user, self.answer)


class UserResultManager(models.Manager):

    def get_user_result(self, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
            return self.filter(exam=exam).order_by('-score', 'total_time_spent')
        except Exception as e:
            return False


class UserResult(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, default="")
    score = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)

    objects = UserResultManager()

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]

    def __str__(self):
        return "{} || score: {}".format(self.user, self.score)
