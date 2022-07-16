import datetime
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from step1.models import PersonalInfoStepOne
from authentication.models import User


@login_required
def personal_info_step1(request):
    context = {}
    if PersonalInfoStepOne.objects.filter(user=request.user).exists():
        data = PersonalInfoStepOne.objects.get(user=request.user)
        if data is not None:
            context['personal'] = data
    userBasicInfo = User.objects.get(id=request.user.id) 
    context['basic'] = userBasicInfo      

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        middlename = request.POST['middlename']
        dateofbirth = request.POST['dateofbirth']
        idnumber = request.POST['idnumber']
        education = request.POST['education']
        status = request.POST['status']
        gender = request.POST['gender']
        resident = request.POST['resident']

        if dateofbirth == '' or idnumber == '' or status == '' or resident == '' or firstname == '' or lastname == '':
            context['errors'] = 'Please fill in all fields'
            return render(request, 'step1/step1.html', context)

        if not idnumber.isdigit():
            context['errors'] = 'ID number can only contain digits'
            return render(request, 'step1/step1.html', context)
        
        if any(letter.isdigit() for letter in firstname) or any(letter.isdigit() for letter in firstname):
            context['errors'] = 'Names can only contain alpha values (a-z)'
            return render(request, 'step1/step1.html', context)
        
        
        if PersonalInfoStepOne.objects.filter(user=request.user).exists():
            # update data
            data = PersonalInfoStepOne.objects.get(user=request.user)
            data.firstname = firstname
            data.lastname = lastname
            data.middlename = middlename
            data.idnumber = idnumber
            data.save()

            
            return redirect('step2')

        dateofbirth = datetime.datetime.strptime(dateofbirth, '%m/%d/%Y').strftime('%Y-%m-%d')

        personal = PersonalInfoStepOne.objects.create(
            user=request.user,
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            idnumber=idnumber,
            status=status,
            resident=resident,
            dateofbirth=dateofbirth,
            gender=gender,
            education=education,
            is_complete=True
        )
        personal.save()         

        return redirect('step2')

    return render(request, 'step1/step1.html', context)
