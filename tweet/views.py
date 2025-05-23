from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm, UserProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from rest_framework import viewsets, permissions
from .serializers import TweetSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, Http404
from .utils.ai_helper import generate_tweet_idea


# Create your views here.
def home(request):
    return render(request, 'home.html')
def index(request):
    return render(request, 'index.html')
@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_At')
    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'show_actions': False  # Don't show Edit/Delete here
    })

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form=TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form=TweetForm(request.POST, request.FILES, instance =tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
        return redirect('tweet_list')
    else:
        form =TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

@login_required
def my_tweets(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_At')
    return render(request, 'my_tweets.html', {
        'tweets': tweets,
        'show_actions': True  # Show Edit/Delete here
    })
#search view
@login_required
def tweet_search(request):
    query = request.GET.get('q')
    tweets = Tweet.objects.all().order_by('-created_At')

    if query:
        tweets = tweets.filter(Q(title__icontains=query) |Q(text__icontains=query) )

    return render(request, 'tweet_list.html', {'tweets': tweets, 'query': query})       

def tweet_detail(request, tweet_id):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            tweet = Tweet.objects.get(id=tweet_id)
            data = {
                'username': tweet.user.username,
                'title': tweet.title,
                'text': tweet.text,
                'photo': tweet.photo.url if tweet.photo else '',
                'created_At': tweet.created_At.strftime('%b %d, %Y'),
            }
            return JsonResponse(data)
        except Tweet.DoesNotExist:
            raise Http404("Tweet does not exist.")
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your account has been created successfully. You can now login.')
                return redirect('tweet_list')
            except IntegrityError:
                messages.error(request, 'This username already exists. Please try another one.')
        else:
            # Form is invalid, Django will automatically handle specific field errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

class TweetViewSet(viewsets.ModelViewSet):
    queryset=Tweet.objects.all().order_by('-created_At')
    serializer_class=TweetSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

# aiview
from .forms import AIPromptForm
from .utils.ai_helper import generate_tweet_idea
@login_required
def ai_tweet_idea_view(request):
    generated_idea = None

    if request.method == "POST":
        form = AIPromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            generated_idea = generate_tweet_idea(prompt)
    else:
        form = AIPromptForm()

    return render(request, "ai_tweet_idea.html", {
        'form': form,
        'generated_idea': generated_idea
    })
