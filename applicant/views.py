from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Skills, Applicant
from django.contrib import messages
from .forms import ApplicantProfileForm, ResumeForm
from users.models import CustomUser

# Create your views here.

def applicant_profile_view(request):
    if request.user.is_authenticated:
        applicant = Applicant.objects.filter(user=request.user)
        if not applicant.exists():
            messages.warning(request, 'Applicant profile not found')
            return redirect('update_applicant')
        applicant = applicant.first()
        skills = applicant.skills.all()
        # print("Here", applicant.resume.resume.url)
        return render(request, 'applicant/applicant_profile.html', {'applicant': applicant, 'skills': skills, 'resume': applicant.resume})

    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login/Signup first')
        return redirect('home')
        
    
    
def update_applicant_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        applicant = Applicant.objects.filter(user=user_id)

        if request.method == 'POST':
            form = ApplicantProfileForm(request.POST)

            # get skills from the form
            skills = request.POST.get('skills')
            print("skills", skills)

            if form.is_valid():
                if not applicant.exists():  # Check if applicant exists
                    applicant_instance = form.save(commit=False)
                    applicant_instance.user = request.user
                    print("skills", form.cleaned_data['skills'])
                    applicant_instance.save()
                
                    form.save_m2m()  # Save many-to-many field (skills)
                    resume_ins = upload_resume(request)
                    if resume_ins is None:
                        print(form.errors)
                        return render(request, 'applicant/update_applicant.html', {'form': form, 'skills': Skills.objects.all()})
                    applicant_instance.resume = resume_ins
                    applicant_instance.save()

                else:
                    applicant_instance = applicant.first()
                    applicant_instance.location = form.cleaned_data['location']
                    applicant_instance.phone_number = form.cleaned_data['phone_number']

                    # Clear old skills
                    applicant_instance.skills.clear()

                    # Add new skills
                    print("skills", form.cleaned_data['skills'])
                    applicant_instance.skills.set(form.cleaned_data['skills'])
                    resume_ins = upload_resume(request)
                    if resume_ins is None:
                        print(form.errors)
                        return render(request, 'applicant/update_applicant.html', {'form': form, 'skills': Skills.objects.all()})


                    applicant_instance.resume = resume_ins

                    applicant_instance.save()  # Save the updated object
                    print("THis isss: ", applicant_instance.resume.resume.url)

                return redirect('applicant_profile')

            else:
                print(form.errors)
                messages.warning(request, 'Please enter valid data')
                return render(request, 'applicant/update_applicant.html', {'form': form, 'skills': Skills.objects.all()})

        form = ApplicantProfileForm()
        return render(request, 'applicant/update_applicant.html', {'form': form, 'skills': Skills.objects.all()})

    else:
        messages.warning(request, 'Please Login/Signup first')
        return redirect('home')
    
def upload_resume(request):
    if request.user.is_authenticated:
        # applicant = Applicant.objects.filter(user=request.user).first()  

        # if not applicant:
        #     messages.warning(request, "Applicant profile not found.")
        #     return redirect("create_applicant_profile")  

        if request.method == "POST":
            form = ResumeForm(request.POST, request.FILES)
            if form.is_valid():
                
                resume_instance = form.save(commit=False)
                resume_instance.user = request.user  # Assuming Resume has a user field
                resume_instance.save()

                # add a debugging statement to check for applicant.resume
                
                # applicant.save()  # Save the applicant with the resume
                # print("THis isss: ", applicant.resume.resume.url)
                messages.success(request, "Resume uploaded successfully!")
                return resume_instance
            else:
                messages.warning(request, "Please enter valid data")
                return None
        else:
            messages.warning(request, "Please upload a resume")
            return None


    else:
        messages.warning(request, 'Please Login/Signup first')
        return redirect('home')



def veiw_applicant(request, applicant_id):
    applicant = Applicant.objects.filter(id=applicant_id)
    if not applicant.exists():
        messages.warning(request, 'Applicant not found')
        return redirect('home')
    applicant = applicant.first()
    return render(request, 'applicant/view_applicant.html', {'applicant': applicant})


def view_applicants(request):
    if request.user.is_superuser:
        applicants = Applicant.objects.all()
        return render(request, 'applicant/view_applicants.html', {'applicants': applicants})
    else:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('home')
    
def delete_applicant(request, applicant_id):
    if request.user.is_superuser:
        applicant = Applicant.objects.filter(id=applicant_id)
        if not applicant.exists():
            messages.warning(request, 'Applicant not found')
            return redirect('view_applicants')
        applicant = applicant.first()
        applicant.delete()
        return redirect('view_applicants')
    else:
        messages.error(request, 'You are not authorized to delete this applicant')
        return redirect('home')
            
def applicant_view_by_email(request, email):
    user = CustomUser.objects.get(email=email)
    applicant = Applicant.objects.filter(user=user)
    if not applicant.exists():
        messages.warning(request, 'Applicant not found')
        return redirect('home')
    applicant = applicant.first()
    return render(request, 'applicant/view_applicant.html', {'applicant': applicant})
    


