from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from account.models import ContibutionFrequency, Points, Chama
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
            # check if chama with frequency and amount exists and add user to chama
            user = User.objects.get(id=request.user.id)
            if Chama.objects.filter(frequency=frequency, amount=amount).exists():
                chama = Chama.objects.filter(frequency=frequency, amount=amount).order_by('-created').first()
                members = User.objects.filter(chama_id=chama.id).count()
                if chama.group_complete == False:
                    user.chama = chama
                    user.save()
                    transaction.chama = chama
                    transaction.save()
                    context["chama"] = chama
                    members_count = User.objects.filter(chama_id=chama.id).count()
                    context["count"] = members_count
                    if members_count == 3:
                        chama.group_complete = True;
                        chama.save()
                        members_count = User.objects.filter(chama_id=chama.id).count()
                        context["count"] = members_count
                if chama.group_complete == True:
                    chama = Chama.objects.create(
                    frequency=frequency,
                    amount=amount
                )
                    user.chama_id = chama.id
                    transaction.chama = chama
                    transaction.save()
                    chama.save()
                    user.save()
                    context["chama"] = chama
                    members_count = User.objects.filter(chama_id=chama.id).count()
                    context["count"] = members_count
            else:
                # create chama with frequency and amount
                chama = Chama.objects.create(
                    frequency=frequency,
                    amount=amount
                )
                user.chama_id = chama.id
                transaction.chama = chama
                transaction.save()
                chama.save()
                user.save()
                context["chama"] = chama
                members_count = User.objects.filter(chama_id=chama.id).count()
                context["count"] = members_count

            return render(request, 'account/home.html', context)

    return render(request, 'account/home.html', context)


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


def reset_password(request):
    context = {}
    if request.method == 'POST':
        oldpassword = request.POST['oldpassword']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password1 = request.POST['password1']

        if oldpassword == '' or password == '' or password1 == '':
            context['errors'] = 'Please insert all fields'
            return render(request, 'account/password_reset.html', context)

        if password != password1:
            context['errors'] = 'Passwords do not match'
            return render(request, 'account/password_reset.html', context)
        
        user = User.objects.get(phone_number=phone_number)
        if user.check_password(oldpassword) == False:
            context['errors'] = 'Invalid password'
            return render(request, 'account/password_reset.html', context)

        user.set_password(password)
        user.save()
        login(request, user)
        context["success"] = "Password successfully updated"

    return render(request, 'account/password_reset.html', context)

