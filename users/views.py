from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser as Users
from .signupForm import NewUserForm
from django.contrib import messages
from applicant.models import Applicant

# Create your views here.
def signup_applicant_veiw(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already Logged In')
        applicant = Applicant.objects.filter(user=request.user)
        if applicant.exists():
            return redirect('applicant_profile')
        return redirect('update_applicant')
        
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.email)
            queryset = Users.objects.filter(email=user.email)
            print(queryset)
            if queryset.exists():
                messages.warning(request, "Email-id already exists")
                return redirect('signup_applicant')
            user.is_applicant = True
            user.is_company = False
            user.save()
            login(request, user)
            return redirect('update_applicant')
        else:
            messages.error(request, form.errors)
            form = NewUserForm()
            return render(request, 'users/signup_applicant.html', {'form': form})
    else:
        form = NewUserForm()
        return render(request, 'users/signup_applicant.html', {'form': form})
    
def signup_company_veiw(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already Logged In')
        return redirect('home')         
    
    #check if user already exist
    # @TODO: Check if user with email already exist
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_applicant = False
            user.is_company = True
            user.save()
            login(request, user)
            return redirect("update_recruiter")
        else:
            messages.error(request, form.errors)
            form = NewUserForm()
            return render(request, 'users/signup_company.html', {'form': form})
    else:
        form = NewUserForm()
        return render(request, 'users/signup_company.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already Logged In')
        if request.user.is_applicant:
            return redirect('applicant_profile')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_applicant:
            login(request, user)
            return redirect('applicant_profile')
        elif user is not None and user.is_company:
            login(request, user)
            return redirect('recruiter_profile')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Your session has ended')
        return redirect('login')
    else:
        messages.warning(request, 'Please Log In to continue')
        return redirect('login')



def _delete_user(user_id):
    user = Users.objects.get(id=user_id)
    user.delete()


def delete_user(request):
    if request.user.is_authenticated and request.user.is_verified:
        user = request.user
        logout(request)
        _delete_user(user.id)
        messages.warning(request, 'Your account has been deleted')
        return redirect('login')
    else:
        messages.info(request, 'Please Log In to continue')
        return redirect('login')