from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def home(request):
    return render(request,"authentication/index.html")


from django.db import IntegrityError

def signup(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging statement to print POST data
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Rest of your code

        if User.objects.filter(username=username):
            messages.error(request, "Username already Exists! Please try another username")
            return redirect(home)
        
        if User.objects.filter(email = email):
            messages.error(request, "Email already registered!")
            return redirect(home)
        
        if len(username)>10:
            messages.error(request, "Username must be 10 Characters")
        if pass1 != pass2 :
            messages.error(request, "Password didn't Matched !")
        if not username.isalnum():
            messages.error(request, "Username is AlphaNumerical!!")
        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been successfully created.")
            return redirect('/signin')
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('/signup')
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)
        if user is not None:
            login(request, user)
            fname=user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully !")
    return redirect('home')