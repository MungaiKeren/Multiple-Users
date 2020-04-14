from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.views.generic import CreateView, FormView

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()

    return render(request, "accounts/register.html", context)