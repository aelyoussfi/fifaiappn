from django.shortcuts import render,redirect
from . import forms
# Create your views here.

def signup_page(request):
    message = ""
    form = forms.signupForm()
    if request.method == 'POST':
        form = forms.signupForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print('about to authenticate user')
            #login(request,user)
            return redirect('login')
        if not form.is_valid():
            message = form.errors #.as_text()
    return render(request,'accounts/signup.html',{'form':form,"message":message})
