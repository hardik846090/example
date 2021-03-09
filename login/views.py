from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
import phonenumbers
from validate_email import validate_email
from django.contrib import messages
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.base_user import BaseUserManager
from twilio.rest import Client
from .models import Login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth


# Create your views here.


def validation(email, mobile):
    validateDict = {}

    is_valid = validate_email(email)
    if is_valid == True:
        validateDict['email'] = True
    else:
        validateDict['email'] = False

    phone_number = phonenumbers.parse(mobile, "IN")
    if phonenumbers.is_valid_number(phone_number) == True:
        validateDict['mobile'] = True
    else:
        validateDict['mobile'] = False

    return validateDict


def generateOTP(email, mobile):
    OTPDict = {}
    mobileOTP = str(random.randint(100000, 999999))
    account_sid = "ACca19d237b26c0855a40a626df88e008d"
    auth_token = "c98b8e9973c5ed9c722c0dfa13fee259"
    client = Client(account_sid, auth_token)
    client.messages.create(to="+91" + str(mobile), from_="+13344686786",
                           body="This is example OTP" + str(mobileOTP))
    OTPDict['mobileOTP'] = mobileOTP

    emailOTP = str(random.randint(100000, 999999))
    sender = "hardik249312@gmail.com"
    receiver = email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "example password"
    msg.attach(MIMEText(emailOTP, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "hardik846090")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    OTPDict['emailOTP'] = emailOTP

    return OTPDict


def loadLogin(request):
    return render(request, 'loginSystem/login.html')


def insertLogin(request):
    mobileAndEmail = request.POST['mobileAndEmail']
    password = request.POST['password']

    if str(mobileAndEmail).isdigit() == True:
        verify = Login.objects.filter(mobile=mobileAndEmail, password=password)
    else:
        verify = Login.objects.filter(email=mobileAndEmail, password=password)

    if len(verify) != 0:
        request.session['login_Id'] = verify[0].id
        request.session['login_UserName'] = str(verify[0].email).split("@")[0]
        request.session['login_Email'] = verify[0].email
        request.session['login_Role'] = verify[0].role
        request.session['login_Mobile'] = verify[0].mobile
        return redirect('/loadDashbord')
    else:
        messages.success(request, 'please enter correct username and password')
        return redirect('/loadLogin')


def loadRegister(request):
    return render(request, 'loginSystem/register.html')


def insertRegister(request):
    renderDict = {}
    mobile = request.POST['mobile']
    email = request.POST['email']
    password = request.POST['password']

    validationUser = Login.objects.filter(Q(mobile=mobile) | Q(email=email))
    if len(validationUser) == 0:
        validateDict = validation(email, mobile)
        if validateDict['email'] == True and validateDict['mobile'] == True:
            renderDict['mobile'] = mobile
            renderDict['email'] = email
            renderDict['password'] = password

            OTPDict = generateOTP(email, mobile)
            renderDict['emailOTP'] = OTPDict['emailOTP']
            renderDict['mobileOTP'] = OTPDict['mobileOTP']

            request.session['register'] = renderDict
            print(">>>>>>>>>>>>>>", renderDict)
            return render(request, 'loginSystem/otp.html')
        else:
            messages.success(request, 'please enter correct email or mobile number')
            return redirect('/loadRegister')
    else:
        messages.success(request, 'This Email or Mobile number already use.')
        return redirect('/loadLogin')


def loadOTP(request):
    return render(request, 'loginSystem/otp.html')


def insertOTP(request):
    emailOTP = request.POST['emailOTP']
    mobileOTP = request.POST['mobileOTP']

    validationDict = request.session['register']
    if emailOTP == validationDict['emailOTP'] and mobileOTP == validationDict['mobileOTP']:
        Login(email=validationDict['email'], mobile=validationDict['mobile'], password=validationDict['password'],
              role='user', loginStatus='active').save()
        request.session.clear()
        return render(request, 'loginSystem/login.html')
    else:
        messages.success(request, 'Please enter correct OTP.')
        return redirect('/loadOTP')


def logout(request):
    request.session.clear()
    return redirect("/loadLogin")


def loadDashbord(request):
    return HttpResponse("you are in user")
