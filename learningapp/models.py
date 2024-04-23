from django.db import models
from django.contrib.auth.models import User

from autoslug import AutoSlugField


# Create your models here.

class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)




class Course(models.Model):
    course_name = models.CharField(max_length=250, unique=True)
    slug = AutoSlugField(populate_from='course_name', unique=True, null=True)
    course_price = models.CharField(max_length=10, default=None)
    course_offer_price = models.CharField(max_length=10, default=None)
    course_description = models.TextField()
    course_type = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('free', 'Free')])  # True for Paid, False for Unpaid
    course_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    thumbnail = models.ImageField(
        upload_to='course_thumbnails',
        blank=True,
        null=True, 
        default='course/default.png'
    )
    
    create_at = models.DateField(null=True, blank=True, auto_now=True)
    update_at = models.DateField(null=True, blank=True, auto_now=True)
    delete_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.course_name}"
    










class Quiz(models.Model):
        course = models.ForeignKey(Course, on_delete=models.CASCADE)
        quiz_title = models.CharField(max_length=50)
        description = models.TextField()
        time_limit = models.IntegerField()
        randomize_questions = models.BooleanField(default=False)
        attempts_allowed = models.IntegerField()

        def __str__(self):
            return self.quiz_title
        






class QuizQuestion(models.Model):
        QUIZ_QUESTION_TYPES = (
            ('multiple_choice', 'Multiple Choice'),
            ('true_false', 'True/False'),
            ('short_answer', 'Short Answer'),
        )

        quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
        question_text = models.TextField()
        question_type = models.CharField(max_length=20, choices=QUIZ_QUESTION_TYPES)
        points = models.IntegerField()

        def __str__(self):
            return self.question_text  
          
class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
            return self.choice_text 
    












    