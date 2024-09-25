from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm,UserRegistrationForms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # Ensure you're associating the user with the tweet
            tweet.save()  # Save the tweet to the database
            return redirect('tweet_list')
    else:
        form = TweetForm()
    
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()  # Save the edited tweet
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()  # Delete the tweet
        return redirect('tweet_list')
    
    return render(request, 'tweet_confirm_delete.html', {"tweet": tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password correctly
            user.save()  # Save the user instance
            login(request, user)  # Log the user in after registration
            return redirect('tweet_list')  # Redirect to the tweet list page
    else:
        form = UserRegistrationForms()

    return render(request, 'registration/register.html', {'form': form})  # Pass form to template
