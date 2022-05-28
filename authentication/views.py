from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, logout

from authentication.verify import send, check

User = get_user_model()

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'authentication/index.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'authentication/register.html')

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        middlename = request.POST['middlename']
        phone_number = request.POST['phone_number']
        phone_number1 = request.POST['phone_number1']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        
        context = {}

        if firstname == '' or lastname == '' or phone_number == '' or password == '' or confirm_password == '':
            context['errors'] = 'Please fill in all fields'
            return render(request, 'authentication/register.html', context)

        if password != confirm_password:
            context['errors'] = 'Passwords do not match'
            return render(request, 'authentication/register.html', context)

        if phone_number != phone_number1:
            context['errors'] = 'Phone numbers do not match'
            return render(request, 'authentication/register.html', context)
        
        # Check if the phone number already exists
        if User.objects.filter(phone_number=phone_number).exists():
            context['errors'] = 'Phone number already exists'
            return render(request, 'authentication/register.html', context)

        # Create the user
        user = User.objects.create_user(
            phone_number=phone_number,
            firstname=firstname,
            lastname=lastname,
            middlename=middlename,
            password=password   
        )

        user.save()
        # redirect to login page
        context['success'] = 'User created successfully, Login to continue'

        return render(request, 'authentication/login.html', context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')

    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        context = {}

        if phone_number == '' or password == '':
            context['errors'] = 'Please fill in all fields'
            return render(request, 'authentication/login.html', context)

        if not User.objects.filter(phone_number=phone_number).exists():
            context['errors'] =  'Wrong phone number or password'
            return render(request, 'authentication/login.html', context)

        user = User.objects.get(phone_number=phone_number)
        if user.check_password(password):
            login(request, user)
            if user.is_verified:
                return redirect('home')
            return redirect('verify')

        context['errors'] = 'Wrong phone number or password'
        return render(request, 'authentication/login.html', context)

def verify_phone_number(request):
    context = {}
    if request.method == 'GET':
        response = send(request.user.get_username())

        if response is None:
            context['errors'] = 'Error sending verification code'
            return render(request, 'authentication/verify.html', context)
        
        context['success'] = 'Verification code sent successfully'
        return render(request, 'authentication/verify.html')


    if request.method == 'POST':
        code = request.POST['code']

        if check(request.user.get_username(), code):
            request.user.is_verified = True
            request.user.save()

            context['success'] = 'Phone number verified successfully'

            return redirect('home')
        context['errors'] = 'Invalid verification code'
        return render(request, 'authentication/verify.html', context)

def new_password(request):
    context = {}

    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password != password1:
            context['errors'] = 'Passwords do not match'
            return render(request, 'authentication/new_password.html', context)

        user = User.objects.get(phone_number=phone_number)
        user.set_password(password)
        user.save()

        login(request, user)
        return redirect('home')

    return render(request, 'authentication/new_password.html')

def password_reset_confirm(request):
    context = {}

    if request.method == 'POST':
        code = request.POST['code']
        phone_number = request.POST['phone_number']
        if check(phone_number, code):
            context['phone_number'] = phone_number
            return render(request, 'authentication/new_password.html', context)
        
        context['errors'] = 'Invalid verification code'
        return render(request, 'authentication/verify_password_reset.html', context)

    return render(request, 'authentication/verify_password_reset.html')

def password_reset(request):
    context = {}

    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        response = send(phone_number)

        if response is None:
            context['errors'] = 'Error sending verification code'
            return render(request, 'authentication/verify_password_reset.html', context)        

        context['success'] = 'Verification code sent successfully'
        context['phone_number'] = phone_number
        return render(request, 'authentication/verify_password_reset.html', context)

    return render(request, 'authentication/password_reset.html')

def logout_user(request):
    logout(request)
    return redirect('/')