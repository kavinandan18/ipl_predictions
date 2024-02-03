from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Match, Prediction
from .forms import PredictionForm, CustomUserCreationForm,EditMatchForm,CreateMatchForm
from django.contrib.auth import  login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone


def home(request):
    return render(request, 'predictions/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'predictions/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'predictions/login.html', {'form': form})

def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        messages.info(request, 'You have been logged out.')
        return render(request, 'predictions/logout.html')



@login_required
def index(request):
    matches = Match.objects.all()
    return render(request, 'predictions/index.html', {'matches': matches})

@login_required
def predictions_view(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'predictions/prediction_view.html', {'predictions': predictions})

@login_required
def edit_prediction(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PredictionForm(request.POST, instance=prediction)
        if form.is_valid():
            form.save()
            return redirect('predictions_view')
    else:
        form = PredictionForm(instance=prediction)

    return render(request, 'predictions/edit_prediction.html', {'form': form, 'prediction': prediction})

@login_required
def delete_prediction(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk, user=request.user)

    if request.method == 'POST':
        prediction.delete()
        return redirect('predictions_view')

    return render(request, 'predictions/delete_prediction.html', {'prediction': prediction})

@login_required
def create_match(request):
    if request.method == 'POST':
        form = CreateMatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.user = request.user
            match.save()
            return redirect('index')  # Redirect to the main page after creating match
    else:
        form = CreateMatchForm()

    return render(request, 'predictions/create_match.html', {'form': form})

@login_required
def make_prediction(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    # Check if the logged-in user is the owner of the match
    if match.user and request.user != match.user:
        return HttpResponseForbidden("You are not allowed to make predictions for this match.")

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.user = request.user
            prediction.match = match
            prediction.save()
            messages.success(request, 'Prediction successfully saved!')
            return redirect('prediction_success')
    else:
        # Pass the form instance to the template
        form = PredictionForm(initial={'match': match})

    return render(request, 'predictions/make_prediction.html', {'form': form, 'match': match})

def view_match(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'predictions/view_match.html', {'match': match})

@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    # Check if the logged-in user is the owner of the match
    if match.user and request.user != match.user:
        return HttpResponseForbidden("You are not allowed to make predictions for this match.")

    if request.method == 'POST':
        match.delete()
        return redirect('index')  # Redirect to the main page after deletion
    else:
        return render(request, 'predictions/delete_match.html', {'match': match})

@login_required
def edit_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    # Check if the logged-in user is the owner of the match
    if match.user and request.user != match.user:
        return HttpResponseForbidden("You are not allowed to make predictions for this match.")

    if request.method == 'POST':
        form = EditMatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the main page after editing
    else:
        form = EditMatchForm(instance=match)

    return render(request, 'predictions/edit_match.html', {'form': form, 'match': match})

@login_required
def prediction_success(request):
    return render(request, 'predictions/prediction_success.html')


