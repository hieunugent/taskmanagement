# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm


# Create your views here.
def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request,user)
            messages.success(request,'Your account has been created successfully!')
            return redirect('home')
    else:
        form =UserRegisterForm()
    return render(request,'users/register.html', {'form':form})