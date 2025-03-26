from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Skills, Applicant
from django.contrib import messages
from .forms import ApplicantProfileForm

# Create your views here.

def applicant_profile_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        applicant = Applicant.objects.get(user=user_id)
        skills = applicant.skills.all()
        return render(request, 'applicant/applicant_profile.html', {'applicant': applicant, 'skills': skills})

    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login/Signup first')
        return redirect('home')
        
    
    
def update_applicant_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        applicant = Applicant.objects.filter(user=user_id)
        if request.method == 'POST':
            form = ApplicantProfileForm(request.POST)
            if form.is_valid():
                if applicant is None or len(applicant) == 0:
                    applicant = form.save(commit=False)
                    applicant.user = request.user
                    applicant.save()
                    return render(request, 'applicant/applicant_profile.html', {'applicant': applicant})
                else:
                    applicant.location = form.cleaned_data['location']
                    applicant.phone_number = form.cleaned_data['phone_number']
                    applicant_instance = applicant.first()
                    applicant_skills = applicant_instance.skills.all() if applicant_instance else []
                    for skill in applicant_skills:
                        applicant.skills.remove(skill)
                    skills = form.cleaned_data['skills']
                    for skill in skills:
                        applicant.skills.add(skill)
                    applicant.update()
                    return render(request, 'applicant/applicant_profile.html', {'applicant': applicant})
            else:
                print(form.errors)
                messages.warning(request, 'Please enter valid data')

                return render(request, 'applicant/update_applicant.html', {'form': form, 'skills': Skills.objects.all()})
        form = ApplicantProfileForm()
        return render(request, 'applicant/update_applicant.html', {'form': form, 'skills': Skills.objects.all()})
    else:
        messages.warning(request, 'Please Login/Signup first')
        return redirect('home')
                
            




    