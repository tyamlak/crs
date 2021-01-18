from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import render, redirect


def sign_in(request):
	if request.POST:
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username,password=password)
		if user:
			redirect_to = request.GET.get('next','case-list')
			login(request,user)
			print('Redirecting to ',redirect_to)
			return redirect(redirect_to)
		else:
			return render(request,'case/login.html',
				{'error':'Wrong Username or Password'})
	else:
		if not get_user(request).is_anonymous:
			redirect_to = request.GET.get('next','case-list')
			return redirect(redirect_to)
		return render(request,'case/login.html',
			{'login_required':True})

def sign_out(request):
    logout(request)
    return redirect('index')