from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def check(request):
    return redirect("Login")


def user_login(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        return redirect("Details")
    context = {"error_msgs": []}
    if request.method == "POST":
        if check_values(request.POST, context):
            try:
                student = Student.objects.get(username=request.POST["rollno"])
            except:
                context["error_msgs"].append("User does not exist")
            student = authenticate(request, username=request.POST["rollno"], password=request.POST["pwd"])
            if student is not None:
                if not student.is_staff:
                    login(request, student)
                    return redirect("Details")
                else:
                    context["error_msgs"].append("staff cant login here")

            else:
                context["error_msgs"].append("check your username or password")
    return render(request, "User/login.html", context)


@login_required(login_url="/login")
def details(request):
    return render(request, "User/Details.html")


def user_logout(request):
    logout(request)
    return redirect("Login")


# functions

def check_values(user, context):
    crt = True
    if user["rollno"] == "":
        crt = False
        msg = "UserName should not be empty"
        context["error_msgs"].append(msg)
    if user["pwd"] == "":
        crt = False
        msg = "Password should not be empty"
        context["error_msgs"].append(msg)
    return crt
