
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login

from .forms import CourseForm

from .models import Course



# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('admin_index')  # Redirect to admin_index if user is superuser
                else:
                    return redirect('index')  # Redirect to index if user is not superuser
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def admin_index(request):
    return render(request, 'admin_index.html')





def courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_index')  # Redirect to index page after successfully creating the course
    else:
        form = CourseForm()
    return render(request, 'courses.html', {'form': form})




def view(request):
    courses = Course.objects.all()  
    return render(request, 'view.html', {'courses': courses})




def delete(request,id):
    dlt=Course.objects.get(id=id)
    dlt.delete()
    return redirect('admin_index') 



def edit(request,id):
    data={
        "data":Course.objects.get(id=id)
        }
    return render(request,'edit.html',data)



def update(request, id):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_price = request.POST.get('course_price')
        course_offer_price = request.POST.get('course_offer_price')
        course_description = request.POST.get('course_description')
        course_type = request.POST.get('course_type')
        course_status = request.POST.get('course_status')
        
        # Fetch the Course object from the database
        edit = Course.objects.get(id=id)
        
        # Check if a new image file was uploaded and update the thumbnail accordingly
        if 'img' in request.FILES:
            edit.thumbnail = request.FILES['img']
        
        # Update other fields of the Course object
        edit.course_name = course_name
        edit.course_price = course_price
        edit.course_offer_price = course_offer_price
        edit.course_description = course_description
        edit.course_type = course_type
        edit.course_status = course_status
               
        # Save the updated Course object
        edit.save()
        
        # Redirect to a specific URL after updating (e.g., admin index)
        return redirect('admin_index')
    
    # If the request method is not POST, render the same page
    return render(request, 'edit.html')





from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Course

def course_fullview(request):
    # Retrieve all courses from the database
    all_courses = Course.objects.all()
    
    # Number of courses per page
    per_page = 10
    
    # Create a Paginator object
    paginator = Paginator(all_courses, per_page)
    
    # Get the current page number
    page_number = request.GET.get('page')
    
    try:
        # Get the courses for the requested page number
        courses = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        courses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        courses = paginator.page(paginator.num_pages)
    
    return render(request, 'course_fullview.html', {'courses': courses})







def add_to_cart(request, course_id):
    # Logic to add course to the cart goes here
    return redirect('course_fullview')  # Redirect to user_courses page after adding to cart











# from django.shortcuts import render, get_object_or_404
# from .models import Course, Quiz(ethu venam)

# def course_detail(request, course_id):
#     # Retrieve the course object using get_object_or_404
#     course = get_object_or_404(Course, id=course_id)
    
#     # Retrieve quizzes related to the current course
#     quizzes = Quiz.objects.filter(course=course)
    
#     # Pass the course and quizzes to the template
#     return render(request, 'course_detail.html', {'course': course, 'quizzes': quizzes})






from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Course, Quiz, QuizChoice

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizzes = Quiz.objects.filter(course=course)
    
    if request.method == 'POST':
        total_score = 0
        for question_id, choice_id in request.POST.items():
            if question_id.startswith('question'):
                try:
                    question_id = int(question_id.replace('question', ''))
                    choice_id = int(choice_id)  # Convert choice_id to int
                except ValueError:
                    # Handle invalid choice_id (e.g., '_12')
                    # You can skip this choice or handle it in another way
                    continue
                
                try:
                    selected_choice = QuizChoice.objects.get(pk=choice_id)
                    if selected_choice.is_correct:
                        total_score += selected_choice.question.points
                except QuizChoice.DoesNotExist:
                    # Handle case where choice_id does not exist in the database
                    continue
        
        return render(request, 'course_detail.html', {'course': course, 'quizzes': quizzes, 'total_score': total_score})
    
    return render(request, 'course_detail.html', {'course': course, 'quizzes': quizzes})





from .forms import QuizForm
def admin_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_index')  # Redirect to index page after successfully creating the course
    else:
        form = QuizForm()
    return render(request, 'admin_quiz.html', {'form': form})






from django.urls import reverse
from django.shortcuts import redirect
from .forms import QuizQuestionForm

def create_question(request):
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)  # Redirect back to the same page
    else:
        form = QuizQuestionForm()
    return render(request, 'create_question.html', {'form': form})




from .models import QuizQuestion
from .forms import QuizChoiceForm
def create_choice(request):
    if request.method == 'POST':
        form = QuizChoiceForm(request.POST)
        if form.is_valid():
            # Associate the QuizChoice with the selected QuizQuestion
            question_id = request.POST.get('question')  # Get the selected QuizQuestion ID from the form
            question = QuizQuestion.objects.get(pk=question_id)  # Retrieve the QuizQuestion object using the ID
            form.instance.question = question  # Associate the QuizChoice with the selected QuizQuestion
            form.save()
            return redirect('admin_index')  # Redirect to the view showing list of quiz choices
    else:
        form = QuizChoiceForm()
    return render(request, 'create_choice.html', {'form': form})





from django.shortcuts import render
from .models import QuizQuestion, QuizChoice

def quiz_view(request):
    questions = QuizQuestion.objects.all()
    context = {'questions': questions}
    return render(request, 'quiz_view.html', context)





from django.http import HttpResponse

def grade_quiz(request):
    if request.method == 'POST':
        total_score = 0
        for question_id, choice_id in request.POST.items():
            if question_id.startswith('question'):
                try:
                    question_id = int(question_id.replace('question', ''))
                    choice_id = int(choice_id)  # Convert choice_id to int
                except ValueError:
                    # Handle invalid choice_id (e.g., '_12')
                    # You can skip this choice or handle it in another way
                    continue
                
                try:
                    selected_choice = QuizChoice.objects.get(pk=choice_id)
                    print(f"Selected choice: {selected_choice}")  # Print the selected choice for debugging
                    if selected_choice.is_correct:
                        total_score += selected_choice.question.points
                except QuizChoice.DoesNotExist:
                    # Handle case where choice_id does not exist in the database
                    continue

        return HttpResponse(f"Your total score is: {total_score}")
    else:
        return HttpResponse("Method not allowed")
    



from django.shortcuts import render
from django.http import HttpResponse

def submit_quiz(request):
    if request.method == 'POST':
        score = calculate_score(request.POST)
        return HttpResponse(f'Your score: {score}')
    else:
        return HttpResponse('Method not allowed')

def calculate_score(submitted_answers):
    pass




