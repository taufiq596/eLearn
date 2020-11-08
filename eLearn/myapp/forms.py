from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm,UserChangeForm, PasswordChangeForm
from .models import Contact, BlogPost, BlogComment

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(max_length=100, label = 'Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=100, label = 'Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name','email')
        labels = {'username':'Username', 'first_name':'First name', 'last_name':'Last name', 'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'}),
                    'first_name': forms.TextInput(attrs={'class':'form-control'}),
                    'last_name': forms.TextInput(attrs={'class':'form-control'}),
                    'email': forms.EmailInput(attrs={'class':'form-control'}) }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Username',widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(max_length=100, label='Password',widget=forms.PasswordInput(attrs={'autofocus':True, 'class':'form-control'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'description')
        labels = {'name':'Name', 'email':'Email', 'phone':'Phone Number', 'description': 'Your Message'}
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':'3'})
            }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'author', 'slug', 'image')
        labels = {'title':'Title', 'content':'Content', 'author':'Author', 'slug':'Slug', 'image':'Image'}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'})
        }


class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'username':'Username', 'first_name': 'First Name', 'last_name':'Last Name','email': 'Email'}
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))

