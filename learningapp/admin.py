from django.contrib import admin

# Register your models here.

from django.shortcuts import redirect
from .models import QuizChoice
from .models import QuizQuestion
from .models import Quiz


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('admin_index')  # Redirect superuser to admin_index page
        return super().index(request, extra_context)
    


admin.site.register(QuizChoice)
admin.site.register(QuizQuestion)
admin.site.register(Quiz)