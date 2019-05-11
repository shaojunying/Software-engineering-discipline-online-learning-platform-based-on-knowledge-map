import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import SearchForm
from .models import Course


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def start(request):
    return render(request, 'app/start.html')


@login_required
def graph(request):
    return render(request, 'app/graph.html')


@login_required
def others(request):
    return render(request, 'app/others.html')


@login_required
def search(request):
    result = ""
    if request.method == "POST":
        question_form = SearchForm(request.POST)
        if question_form.is_valid():
            data = question_form.cleaned_data  # 键值对
            result = requests.get('http://127.0.0.1:5000/query/' + data['question']).text
    else:
        question_form = SearchForm()
    return render(request, 'app/search.html', {"question_form": question_form, "result": result})


