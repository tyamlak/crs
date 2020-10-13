from django.shortcuts import render, redirect
from UserProfile.models import Criminal, Person
from UserProfile.forms import PersonForm
from case.form_tools import get_criminal_form_data


#@login_required # requires(police/data_encoder)decorators
def create_case(request):
	error = ''
	if request.POST:
		error = ''
		return render(
			request,'case/index.html',{
				'error':error
			}
		)
	return render(
		request,'case/create_case.html',{
			'error': error
		}
	)


def edit_case(request,pk):
	if request.POST:
		pass
	return render(request,'case/edit_case.html')
	

def edit_criminal_info(request,pk):
	criminal_ob = Person.objects.get(pk=pk)
	if request.POST:
		form_data = get_criminal_form_data(request)
		print(form_data)
		return redirect('edit-info',pk)
	form = PersonForm(instance=criminal_ob)
	return render(request,'case/edit_info.html',{'form':form})
