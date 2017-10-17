from django.shortcuts import render

def index(request):
    context = {'hello':'hello'}
    return render(request,'basicinformation/index.html',context)
