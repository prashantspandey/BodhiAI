from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form}

    if request.POST:

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))

    return render(request, 'membership/login.html', context)



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Successfully Logged Out")
        return HttpResponseRedirect(reverse('basic:home'))
    else:
        messages.add_message(request, messages.INFO, "You were not logged in.")
        return HttpResponseRedirect(reverse('basic:home'))

