# --------- Form.py ---------
from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm,
UserChangeForm,PasswordResetForm,SetPasswordForm,PasswordChangeForm)
from django.contrib.auth.models import User
from django import forms

# User Signup
class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            # 'first_name':forms.TextInput(attrs={'class':'form-control'}),
            # 'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     ok = self.cleaned_data['email']
    #     if ok == '':
    #         raise forms.ValidationError('Required')
    #     else:
    #         ok

# User Signin
class SigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','password']

# User Profile
class UserProfileChangeForm(UserChangeForm):
    password =None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {

        'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),

        'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),

        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),

        'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter E-Mail'}),

    }

# User Change Password with Old Password
class PassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Old Password'}))
    new_password1 =forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 =forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Re-New Password'}))

# Password Reset TextBox With Registred E-Mail
class PassResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Registered E-Mail'}))
    
# New Password Set Registred E-Mail Link
class SetNewPassForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}))




# --------- View.py ---------
from django.shortcuts import render,redirect
from .form import CutomerRegistrationForm,UserLoginForm,UserProfileChangeForm,PassChangeForm,PassResetForm,SetNewPassForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# User Signup
def RegisterView(request):
    if request.method == 'POST':
        form = CutomerRegistrationForm(request.POST)
        if form.is_valid():
            usrname= form.cleaned_data['username']
            print(usrname)
            form.save() 
            messages.success(request,f'{usrname} Successfully Registred')
            form = CutomerRegistrationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        form = CutomerRegistrationForm()
        context = {'form': form, }
    return render(request, 'signup.html', context)



# User Signin
def SigninView(request):
    form = UserLoginForm()
    if request.method == 'POST':
        uname = request.POST['username']
        upass = request.POST['password']
        user = authenticate(username=uname,password=upass)
        if user is None:
            messages.error(request,'Please Enter Correct Credinatial')
            return redirect('/signin/')
        else:
            login(request,user)
            messages.success(request,'Login Successful')
        return redirect('/shop/')
    else:
        if request.user.is_authenticated:
            return redirect('/shop/')
        else:
            return render(request,'signin.html',{'form':form})
    return render(request,'signin.html',{'form':form})

# User Logout
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You are Successfully Logged Out !')
        return redirect('/signin')
    else:
        messages.info(request, 'Please Login First')
    return redirect('/signin')


# User Profile Update
def ProfileView(request):
    if request.user.is_authenticated:
        form =UserProfileChangeForm(instance=request.user)
        context = {'form':form}
        if request.method == 'POST':
            form =UserProfileChangeForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.info(request,'Profile Successfully Updated')
                return redirect('/profile/')
            else:
                form =UserProfileChangeForm(instance=request.user)
                user_data = request.user
                context = {'form':form,'user_data':user_data}
                return render(request,'profile.html',context)
        
        return render(request,'profile.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/signin')



# User Password Change
def ChangePassView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PassChangeForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password Successfully Changed')
        else:
            form = PassChangeForm(user =request.user)
            
        context= {'form':form,}
        return render(request,'passchange.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/signin/')


# --------- Url.py ---------
from django.urls import path
from .views import *
from .form import PassResetForm,SetNewPassForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',RegisterView),
    path('signin/',SigninView),
    path('logout/',logoutView),
    path('profile/',ProfileView),
    path('pass_change/',ChangePassView),

    #Password Reset
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=PassResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=SetNewPassForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),

]