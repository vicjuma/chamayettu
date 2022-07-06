from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .forms import RegisterForm
from verify_email.email_handler import send_verification_email

User = get_user_model()

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'authentication/index.html')

def register(request):
    context = {}
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            context['success'] = 'User created successfully, Login to continue'
            return render(request, 'authentication/confirm_email.html')
        return render(request, 'authentication/register.html', {'form': form})
    return render(request, 'authentication/register.html', {'form': form})
    # return render(request, 'authentication/login.html', context)

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
            if user.is_active:
                login(request, user)
                return redirect('home')
            context['errors'] = 'You have not verified your email. Kindly check your inbox or spam for activation the link'
            return render(request, 'authentication/login.html', context)

        context['errors'] = 'Wrong phone number or password'
        return render(request, 'authentication/login.html', context)

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

def logout_user(request):
    logout(request)
    return redirect('/')

def activate(request, uidb64, token):
    context = {}
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return render(request, 'authentication/message.html', context)
    else:
        return render(request, 'authentication/invalid.html', context)
    

def forgetPass(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'This Email does not exists')
            return render(request, 'authentication/forget_pass_fail.html')
        else:
            user = User.objects.get(email=email)
            message = render_to_string('authentication/password_reset_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user),
            })
            mail = EmailMessage(
                'Password Reset',  # subject
                message,
                to=[email],  # to
            )
            mail.send()
            messages.success(request, 'The email has been sent successfully')
            return render(request, 'authentication/forget_pass_success.html')
    if request.method == 'GET':
        return render(request, 'authentication/password_reset.html')

def CompletePasswordReset(request, uidb64, token):
  if request.method == 'GET':
    try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = User.objects.get(id=uid)

      if not default_token_generator.check_token(user, token):
        return render(request, 'authentication/password_reset_fail.html')
    except Exception as identifier:
      pass
    return render(request, 'authentication/new_password.html')

  if request.method == 'POST':
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    if password1 != password2:
        messages.error(request, 'Passwords do not match')
        return render(request, 'authentication/new_password.html')
    else:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
            user.set_password(password1)
            user.save()
            messages.success(
                request, 'The password has been reset successfully')
        except Exception as identifier:
            messages.error(request, 'Something went wrong, try again')
            return render(request, 'authentication/password_reset_fail.html')
        return render(request, 'authentication/password_reset_success.html')