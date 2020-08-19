from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import render, redirect


def sign_in(request):
	if request.POST:
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			redirect_to = request.GET.get('next','index')
			return redirect(redirect_to)
		else:
			return render(request,'UserProfile/login.html',
				{'error':'Wrong Username or Password'})
	else:
		if get_user(request):
			return redirect('index')
		return render(request,'UserProfile/login.html',
			{'login_required':True})

def sign_out(request):
    logout(request)
    return redirect('index')