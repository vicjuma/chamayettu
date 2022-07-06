from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from step2.models import PersonalInfoStepTwo
from authentication.models import User

# Create your views here.
@login_required
def personal_info_step2(request):
    context = {}
    if PersonalInfoStepTwo.objects.filter(user=request.user).exists():
        data = PersonalInfoStepTwo.objects.get(user=request.user)
        context['personal'] = data
    
    userBasicInfo = User.objects.get(id=request.user.id) 
    context['basic'] = userBasicInfo 


    if request.method == 'POST':
        email = userBasicInfo.email
        employment = request.POST['employment']
        income = request.POST['income']

        if email == '':
            context['errors'] = 'Please fill in all fields'
            return render(request, 'step2/step2.html', context)

        if PersonalInfoStepTwo.objects.filter(user=request.user).exists():
            # update data
            data = PersonalInfoStepTwo.objects.get(user=request.user)
            data.email = email
            data.save()
            return redirect('step3')

        personal = PersonalInfoStepTwo.objects.create(
            user=request.user,
            email=email,
            employment=employment,
            income=income,
        )

        personal.save()
        return redirect('step3')

    return render(request, 'step2/step2.html', context)