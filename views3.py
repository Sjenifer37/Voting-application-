04.18 11:58 AM


from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Questions, Voted, UserProfile
from django.contrib import messages
# Create your views here.
def Index(request):
    return render(request, "app/login.html")

def register(request):
    return render(request, "app/registration.html")

@login_required(login_url="login")
def successfully(request):
    return render(request, "app/successfully_voted.html")

@login_required(login_url="login")
def already(request):
    return render(request, "app/already_voted.html")


def Registration(request):
    if request.method == "POST":
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['passw']
        cpassword = request.POST['cpass']
        age = int(request.POST['age'])  # Convert age to an integer

        if password == cpassword:
            new_user = User.objects.create(
                username=username,
                email=email,
            )
            new_user.set_password(password)
            new_user.save()

            # Save the age information in the UserProfile model
            UserProfile.objects.create(user=new_user, age=age)

            return redirect("index")
        return render(request, "app/registration.html")
   
def Loginview(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("show")
        else:
            return HttpResponse("invalid credentials")
   
@login_required(login_url="login")
def home(request):
    return render(request, "app/votingpage.html")

@login_required(login_url="login")
def Voting(request, pk):
    user = request.user
    ques = get_object_or_404(Questions, pk=pk)
   
    # Check if the user is below 18 years old
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.age < 18:
        messages.warning(request, "Voters below 18 years of age are not allowed to vote.")
        return render(request, "app/votingpage.html")

    # Check if the user has already voted for this question
    if Voted.objects.filter(user=user, voted_question=ques).exists():
        return redirect("successfully")
    else:
        ques.vote += 1
        ques.save()
        Voted.objects.create(user=user, voted_question=ques)
        return redirect('already')

@login_required(login_url="login")
def show(request):
    new_ques = Questions.objects.all()
   

    # Check if the user's age is less than 18 and show a warning message
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.age < 18:
        messages.warning(request, "Voter below 18 age group is not allowed.")

    return render(request, "app/votingpage.html", {"new_ques": new_ques, "user_profile": user_profile})

def signout(request):
    logout(request)
    return redirect("index")
