from django.shortcuts import render, redirect
from .forms import RecruiterProfileForm
from django.contrib import messages
from .models import RecruitingCompany as R
from industries.models import Industries



# Create your views here.
def view_recruiter_profile(request):
    if request.user.is_authenticated:
        if request.user.is_company:
            if not R.objects.filter(user=request.user).exists():
                messages.warning(request, 'You need to Update/Create your company profile')
                return redirect('home')
            recruiter = R.objects.filter(user=request.user)
            return render(request, 'recruiter/recruiter_profile.html', {'recruiter': recruiter.first()})
        else:
            messages.warning(request, 'You are not a recruiter')
            return redirect('home')
    else:
        messages.warning(request, 'You need to login first')
        return redirect('login')
        

def update_recruiter_profile(request):
    if request.user.is_authenticated: 
        if request.user.is_company:
            if request.method == 'POST':
                company = R.objects.filter(user=request.user)
                form = RecruiterProfileForm(request.POST)
                if form.is_valid():
                    if not company.exists():
                        company:R = form.save(commit=False)
                        company.user = request.user
                        company.save()
                        return redirect('recruiter_profile')
                    else:
                        company_instance = company.first()
                        company_instance.company_name = form.cleaned_data['company_name']
                        company_instance.company_description = form.cleaned_data['company_description']
                        company_instance.industry = form.cleaned_data['industry']
                        company_instance.save()
                        return redirect('recruiter_profile')
            else:
                form = RecruiterProfileForm()
            industries = Industries.objects.all()
            return render(request, 'recruiter/update_recruiter_profile.html', {'form': form, 'industries': industries})
        else:
            messages.warning(request, 'You are not a recruiter')
            return redirect('home')
    else:
        messages.warning(request, 'You need to login first')
        return redirect('login')

