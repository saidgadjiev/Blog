from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.template import RequestContext
from models import Question, Answer, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms
from django.db import models
import json

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=60)    
    password = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField()
     
    def clean_username(self):
        data = self.cleaned_data.get('username')
        try:
            User.objects.get(username=data)
        except (User.DoesNotExist):
           return data
        raise forms.ValidationError('This username is already taken. ')             
    
    def clean_email(self):
        data = self.cleaned_data.get('email')
        try:
            User.objects.get(email=data)
        except (User.DoesNotExist):
            return data
        raise forms.ValidationError('This email is already taken. ')             

class QuestionForm(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(QuestionForm, self).save(commit=False)
        instance.author = self.author
        if commit:
            instance.save()
        return instance    

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

def index(request, sort='new'):
    page = request.GET.get('page')
    order = sort == 'best' and '-author__profile__rating' or '-date_added'
    question_list = Question.objects.order_by(order)

    paginator = Paginator(question_list, 3)

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    
    isBest = sort == 'best' and True or False 
    return render_to_response('index.html', {'questions': questions, 'isBest': isBest}, context_instance=RequestContext(request))

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            Profile.objects.create(user_id=user.id, avatar_url=request.FILES['avatar'])
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect_to = request.GET.get('next')
            return HttpResponseRedirect(redirect_to)
    else:
        form = UserForm()
    
    return render(request, 'signup.html', {'form': form})

def answer(request):
    id_q = request.GET.get('id_q')
    question = Question.objects.get(id=id_q)
    
    if request.method == 'POST':
        if request.user.is_authenticated():
            author = request.user
            Answer.objects.create(author=author, question=question, text=request.POST['text'])
        else:
            return HttpResponseRedirect('/login/')
    
    answer_list = Answer.objects.filter(question_id=id_q)
    paginator = Paginator(answer_list, 3)

    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)
     
    return render_to_response('answer.html', {'answers': answers, 'question': question}, context_instance=RequestContext(request))

def ask(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            author = request.user
            form = QuestionForm(request.POST, author=author)
            if form.is_valid():
                form.save()
                redirect_to = request.GET.get('next')
                return HttpResponseRedirect(redirect_to) 
        else:
            form = QuestionForm()
        return render(request, 'ask.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def settings(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.profile.email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            Profile.objects.create(user_id=user.id, avatar_url=request.FILES['avatar'])
            user = authenticate(username=username, password=password)

def like(response):
    response_data = {}
    if request.user.is_authenticated():
        type = request.POST.get('type')
        id_user = request.POST.get('id')
        user = User.objects.get(id=id_user)
        if type == 'like':
            user.profile.rating = 10
            response_data['status'] = 'ok'
            response_data['new_rating'] = user.profile.rating 
        else:
            user.profile.raing = 13
            response_data['status'] = 'ok'
            response_data['new_rating'] = user.profile.rating
    else:
        response_data['status'] = 'error'
        responce_data['new_rating'] = 0;
    return HttpResponse(json.dumps(response_data), content_type="application/json")
