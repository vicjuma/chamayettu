import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from account.models import ContibutionFrequency, FirstGuarantor, PersonalInfoStepOne, PersonalInfoStepTwo, Points, SecondGuarantor, Chama
from authentication.verify import send, check
from daraja.models import Savings, Transaction, TotalAmount

User = get_user_model()

# Create your views here.
@login_required
def home(request):
    context = {}

    if not Points.objects.filter(user=request.user).exists():
        Points.objects.create(user=request.user, points=0)

    try:
        ContibutionFrequency.objects.get(user=request.user)
    except ContibutionFrequency.DoesNotExist:
            return render(request, 'account/home.html')

    contribution = ContibutionFrequency.objects.get(user=request.user)
    frequency = contribution.frequency
    amount = contribution.amount
    users = User.objects.all()
    context["users"] = users

    total_savings = 0
    
    # Get total savings
    if Savings.objects.filter(user=request.user).exists():
        if Savings.objects.filter(user=request.user, description="The service request is processed successfully.").exists():
            savings = Savings.objects.filter(user=request.user, description="The service request is processed successfully.")
            total, _ = TotalAmount.objects.get_or_create(
                user=request.user
            )

            for save in savings:
                total_savings += save.amount
            
            total.total = total_savings
            total.save()

            context["total_savings"] = total.value
    
    phone = request.user.get_username().replace('+', '')
    if Transaction.objects.filter(phone_number=phone).exists():
        transactions = Transaction.objects.filter(phone_number=phone)

        for transaction in transactions:
            if transaction.description == "The service request is processed successfully.":
                context["transaction"] = transaction

    # Get chama details
    if Transaction.objects.filter(phone_number=phone).exists():
        transaction = Transaction.objects.filter(phone_number=phone).latest('created')
        if transaction.description == "The service request is processed successfully.":
            if Chama.objects.filter(user=request.user).exists():
                chama = Chama.objects.get(user=request.user)
                context["chama"] = chama
            else:
                # check if chama with frequency and amount exists and add user to chama
                if Chama.objects.filter(frequency=frequency, amount=amount).exists():
                    chama = Chama.objects.get(frequency=frequency, amount=amount)
                    chama.user = request.user
                    context["chama"] = chama
                    chama.save()
                else:
                    # create chama with frequency and amount
                    chama = Chama.objects.create(
                        frequency=frequency,
                        amount=amount,
                        user=request.user
                    )
                    chama.save()
                    transaction.chama = chama
                    transaction.save()
                    context["chama"] = chama

            return render(request, 'account/home.html', context)

    return render(request, 'account/home.html', context)
    
@login_required
def personal_info_step1(request):
    context = {}
    if PersonalInfoStepOne.objects.filter(user=request.user).exists():
        data = PersonalInfoStepOne.objects.get(user=request.user)
        if data is not None:
            context['personal'] = data

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

        if firstname == '' or lastname == '' or middlename == '' or dateofbirth == '' or idnumber == '' or status == '' or resident == '':
            context['errors'] = 'Please fill in all fields'
            return render(request, 'account/step1.html', context)

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

    return render(request, 'account/step1.html', context)

@login_required
def personal_info_step2(request):
    context = {}
    if PersonalInfoStepTwo.objects.filter(user=request.user).exists():
        data = PersonalInfoStepTwo.objects.get(user=request.user)
        context['personal'] = data

    if request.method == 'POST':
        email = request.POST['email']
        employment = request.POST['employment']
        income = request.POST['income']

        if email == '':
            context['errors'] = 'Please fill in all fields'
            return render(request, 'account/step2.html', context)

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

    return render(request, 'account/step2.html', context)

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
            return render(request, 'account/step3.html', context)

        if firstname1 == '' or lastname1 == '' or phone_number1 == '':
            context['errors'] = 'Please fill in all fields of guartor(2)'
            return render(request, 'account/step3.html', context)

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

            response = send(phone_number)
            response2 = send(phone_number1)

            if response is None:
                context['errors'] = 'Fail to send verification code for guarantor(1)'
                return render(request, 'account/verify_guarantor.html', context)
            
            if response2 is None:
                context['errors'] = 'Fail to send verification code for guarantor(2)'
                return render(request, 'account/verify_guarantor.html', context)
            
            return redirect('verify_guarantor')

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

        response = send(phone_number)
        response2 = send(phone_number1)

        if response is None:
            context['errors'] = 'Fail to send verification code for guarantor(1)'
            return render(request, 'account/verify_guarantor.html', context)
        
        if response2 is None:
            context['errors'] = 'Fail to send verification code for guarantor(2)'
            return render(request, 'account/verify_guarantor.html', context)

        context['success'] = 'Verification code has been sent to guarantor(s)'
        return render(request, 'account/verify_guarantor.html', context)
    
    return render(request, 'account/step3.html', context)


@login_required
def verify_guarantor(request):
    context = {}

    if request.method == 'POST':
        code = request.POST['code']
        code1 = request.POST['code1']

        if code == '' or code1 == '':
            context['errors'] = 'Please fill in the code'
            return render(request, 'account/verify_guarantor.html', context)

        if FirstGuarantor.objects.filter(user=request.user).exists():
            data = FirstGuarantor.objects.get(user=request.user)
            phone_number = data.phone_number
            phone_number = str(phone_number)

            if check(phone_number, code):
                data.is_verified = True
                data.save()
            else:
                context['errors'] = 'Verification code is incorrect'
                return render(request, 'account/verify_guarantor.html', context)

        if SecondGuarantor.objects.filter(user=request.user).exists():
            guarantor = SecondGuarantor.objects.get(user=request.user)
            phone_number = guarantor.phone_number
            phone_number = str(phone_number)
            if check(phone_number, code1):
                guarantor.is_verified = True
                guarantor.save()

                context['success'] = 'Phone number verified successfully'
            else:
                context['errors'] = 'Verification code is incorrect (2)'
                return render(request, 'account/verify_guarantor.html', context)

        return redirect('frequency')

    return render(request, 'account/verify_guarantor.html', context)


@login_required
def contribution_frequency(request):
    context = {}
    if ContibutionFrequency.objects.filter(user=request.user).exists():
        data = ContibutionFrequency.objects.get(user=request.user)
        context['contribution'] = data

    if request.method == 'POST':
        frequency = request.POST['frequency']
        amount = request.POST['amount']

        contribution = ContibutionFrequency.objects.create(
            user=request.user,
            frequency=frequency,
            amount=amount,
            is_saved=True
        )

        contribution.save()

        context['contribution'] = contribution

        return render(request, 'account/contribution_frequency.html', context)

    return render(request, 'account/contribution_frequency.html', context)


@login_required
def account(request):
    context = {}
    user = User.objects.get(phone_number=request.user.phone_number)
    context['user'] = user

    if Points.objects.filter(user=request.user).exists():
        data = Points.objects.get(user=request.user)
        context['points'] = data

    if request.method == 'GET':
        return render(request, 'account/account.html', context)

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        middlename = request.POST['middlename']
        profile_image = ''
        if request.FILES.get('profile_image'):
            profile_image = request.FILES['profile_image']

        user = User.objects.get(id=request.user.id)
        if firstname != '':
            user.firstname = firstname
        if lastname != '':
            user.lastname = lastname
        if middlename != '':
            user.middlename = middlename
        if profile_image != '':
            user.profile_image = profile_image
        user.save()

        if user is not None:
            context['success'] = 'Account updated successfully'
            return redirect('account')
        else:
            context['errors'] = 'Error updating account'

        return render(request, 'account/account.html', context)

@login_required
def savings_contribute(request):
    context = {}
    total = TotalAmount.objects.get(user=request.user)
    contribution = ContibutionFrequency.objects.get(user=request.user)
    amount = contribution.amount

    if total.value < int(amount):
        context["errors"] = 'Request failed, insuffient savings'
        return redirect('home')

    total.deductions = amount
    total.save()
    context['success'] = 'Success, your contribution has been recorded'
    return redirect('home')
