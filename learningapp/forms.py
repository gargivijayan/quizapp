
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PhoneNumber
from django.contrib.auth.models import  User

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.save()
        phone_number = self.cleaned_data['phone_number']
        PhoneNumber.objects.create(user=user, phone_number=phone_number)
        return user
    


from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_price', 'course_offer_price', 'course_description', 'course_type', 'course_status', 'thumbnail']








from .models import Quiz
from .models import QuizQuestion, QuizChoice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'quiz_title', 'description', 'time_limit', 'randomize_questions', 'attempts_allowed']







class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['quiz','question_text', 'question_type', 'points']

class QuizChoiceForm(forms.ModelForm):
    class Meta:
        model = QuizChoice
        fields = ['question','choice_text', 'is_correct']        


