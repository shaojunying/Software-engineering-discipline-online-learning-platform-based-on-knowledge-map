from django.shortcuts import render_to_response,render
from django.contrib.auth.decorators import login_required
def home(request): 
    context={}
    return render_to_response('index.html',context)