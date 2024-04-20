04.18 11:53 AM


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
