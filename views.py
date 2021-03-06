from django.shortcuts import render,redirect
from django.views.generic import (
    CreateView,ListView,
    DetailView,UpdateView,
    DeleteView)
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from .models import create_events,Post,profile
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class EventListView(ListView):
    model = create_events
    template_name = 'home/active_event.html'
    context_object_name = 'events'
    ordering = ['-date_posted']

class EventCreateView(LoginRequiredMixin,CreateView):
    model = create_events
    success_url = '/'
    template_name = 'home/create_event.html'
    fields = ['title','content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(EventCreateView, self).form_valid(form)

class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user==post.author:
            return True
        return False


def team(request):
    return render(request,'home/team.html')


def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'home/register.html',{'form':form})


class create_event(CreateView):
    template_name = 'create_event.html'
    model=create_events
    fields = ['title','content','author']
    def get_form(self, form_class=None):
        form=super().get_form()
        
        return form

    def get_success_url(self):
        return reverse('home', )




@login_required
def profile(request):
    if request.method=='POST':
        u_form=UserUpdateForm( request.POST, instance=request.user)
        p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
             u_form.save()
             p_form.save()
        messages.success(request, f'Your account has been updated !')
        return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'home/profile.html',context)

