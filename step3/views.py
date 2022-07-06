from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from step3.models import FirstGuarantor, SecondGuarantor

# Create your views here.
@login_required
def personal_info_step3(request):
    context = {}

    if FirstGuarantor.objects.filter(user=request.user).exists():
        data = FirstGuarantor.objects.get(user=request.user)
        context['guarantor'] = data

    if SecondGuarantor.objects.filter(user=request.user).exists():
        data = SecondGuarantor.objects.get(user=request.user)
        context['guarantor1'] = data

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone_number = request.POST['phone_number']
        relationship = request.POST['relationship']

        firstname1 = request.POST['firstname1']
        lastname1 = request.POST['lastname1']
        phone_number1 = request.POST['phone_number1']
        relationship1 = request.POST['relationship1']

        if firstname == '' or lastname == '' or phone_number == '':
            context['errors'] = 'Please fill in all fields of guartor(1)'
            return render(request, 'step3/step3.html', context)

        if firstname1 == '' or lastname1 == '' or phone_number1 == '':
            context['errors'] = 'Please fill in all fields of guartor(2)'
            return render(request, 'step3/step3.html', context)
        
        if phone_number == request.user.phone_number or phone_number1 == request.user.phone_number:
            context['errors'] = 'You cannot appoint yourself as your guarantor'
            return render(request, 'step3/step3.html', context)
        
        if phone_number == phone_number1:
            context['errors'] = 'You cannot appoint one guarantor twice'
            return render(request, 'step3/step3.html', context)

        if FirstGuarantor.objects.filter(user=request.user).exists() and SecondGuarantor.objects.filter(user=request.user).exists():
            # update data
            data = FirstGuarantor.objects.get(user=request.user)
            data.firstname = firstname
            data.lastname = lastname
            data.phone_number = phone_number
            data.save()

            data = SecondGuarantor.objects.get(user=request.user)
            data.firstname = firstname1
            data.lastname = lastname1
            data.phone_number = phone_number1
            data.save()
            
            return redirect('frequency')

        guarantor1 = FirstGuarantor.objects.create(
            user=request.user,
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
            relationship=relationship,
        )

        guarantor1.save()

        guarantor2 = SecondGuarantor.objects.create(
            user=request.user,
            firstname=firstname1,
            lastname=lastname1,
            phone_number=phone_number1,
            relationship=relationship1,
        )

        guarantor2.save()

        context['success'] = 'Guarantor(s) information saved successfully'
        return redirect('frequency')
    
    return render(request, 'step3/step3.html', context)
