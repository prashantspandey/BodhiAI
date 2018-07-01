from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import (authenticate, 
                                 login,
                                logout,
                                 update_session_auth_hash)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.forms import PasswordChangeForm

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

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

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            try:
                course = request.POST['course']
                if course == None or course == '':
                    print('I am here')
                    new_user = form.save()
                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:home'))
 
                elif str(course.lower()) == 'jito':
                    new_user = form.save(course = course)

                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:jitoHome'))
                elif str(course).lower() == 'siel':
                    new_user = form.save(course = course)

                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:studentInfo'))

                else:
                    new_user = form.save()
                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:home'))
 

            

            except Exception as e:
               print(str(e)) 
            new_user = form.save()
            
            new_user = authenticate(username=form.cleaned_data['username'],
                                                                        password=form.cleaned_data['password1'],
                                                                        )
            login(request, new_user)
            return HttpResponseRedirect(reverse('basic:home'))
        else:
            context = {'form':form}
            return render(request,'membership/register.html', context)
    else:
        form = RegisterForm()
        context = {'form':form}
        return render(request,'membership/register.html',context)



def user_changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST,user = request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'Password successfully changed !!')
            update_session_auth_hash(request,form.user)
            return HttpResponseRedirect(reverse('basic:home'))
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form':form}
    return render(request,'membership/change_password.html',context)

#--------------------------------------------------------------------------------------------------
# client user logins

def siel_user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))


    return render(request, 'membership/siel_login.html', context)









