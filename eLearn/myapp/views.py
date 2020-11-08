from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, ContactForm, BlogPostForm, EditProfileForm, PasswordChangeCustomForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import BlogPost, Contact, BlogComment

# Home 
def home(request):
    form = LoginForm()
    allpost = BlogPost.objects.all().order_by('-date')
   
    context = {'home':'active',
                'form':form,
                'allpost':allpost}
    return render(request, 'myapp/home.html', context)

def about(request):
    users = User.objects.all()
    return render(request, 'myapp/about.html', {'about':'active', 'users':users})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            description = form.cleaned_data['description']
            contact = Contact(name=name, email=email, phone=phone, description=description)
            contact.save()
            messages.success(request, "Thankyou! We will contact you soon")
            form = ContactForm()
    else:    
        form = ContactForm()
    return render(request, 'myapp/contact.html', {'contact':'active','form':form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Account created successfully')  
            return HttpResponseRedirect('/login/')      
    else:    
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form':form})  

# user Authentication

def userlogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data = request.POST)
            if form.is_valid():
                usr = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=usr, password=pwd)
                if user is not None:
                    login(request, user)
                    messages.success(request,'You have loggedin Successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form}) 
    else:
        return HttpResponseRedirect('/dashboard/')

def dashboard(request):
    if request.user.is_authenticated:
        allpost = BlogPost.objects.all().order_by('-date')
        context = {'dashboard':'active',
                'allpost':allpost
                }
        return render(request, 'myapp/dashboard.html', context)
    else:
        return HttpResponseRedirect('/')            

def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/')  

#Blog post

def blog(request):
    allpost = BlogPost.objects.all().order_by('-date')
    return render(request, 'myapp/blog.html', {'blog':'active', 'allpost':allpost})    

def blogpost(request,slug):
    allpost = BlogPost.objects.filter(slug=slug).first()
    allpost.view+=1
    allpost.save()
    comments = BlogComment.objects.filter(post=allpost)
    # print(comments)
    return render(request, 'myapp/blogpost.html', {'allpost':allpost, 'comments':comments})  


def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post added successfully')
                return HttpResponseRedirect('/dashboard/')
        else:
            form = BlogPostForm()
        return render(request, 'myapp/addpost.html',{'form':form})    
    else:
        return HttpResponseRedirect('/login/')

def delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postid = BlogPost.objects.get(id=id)
            postid.delete()
            return HttpResponseRedirect('/dashboard/') 
    else:
        return HttpResponseRedirect('/login/')  

def update(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postid = BlogPost.objects.get(id=id)
            form = BlogPostForm(request.POST, request.FILES, instance=postid)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated successfully')
                return HttpResponseRedirect('/dashboard/')
        else:
            postid = BlogPost.objects.get(id=id)
            form = BlogPostForm(instance=postid)
        return render(request, 'myapp/update.html', {'form':form})    
    else:
        return HttpResponseRedirect('/login/')       

def comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
                comment = request.POST.get('comment')
                user = request.user
                postid = request.POST.get('id')
                post = BlogPost.objects.get(id=postid)
                comments = BlogComment(comment=comment, user=user, post=post)
                comments.save()
                # print(comments)
                messages.success(request, "Comment posted successfully")
                return HttpResponseRedirect(f'/blog/{post.slug}')              
        return render(request, 'myapp/blogpost.html', {'comments':comments})                 
    else:
        return HttpResponseRedirect('/login/')


#User Profile
def viewprofile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        return render(request, 'myapp/profile.html',{'user':user})        
    else:
        return HttpResponseRedirect('/login/')

def editProfile(request, id):
    if request.user.is_authenticated:
        print(request.user)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                messages.success(request, 'Profile Update Successfully!!')
                form.save()
                return render(request, 'myapp/profile.html')
        else:
            form = EditProfileForm(instance=request.user)
        return render(request, 'myapp/editprofile.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/',)


def changePassword(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeCustomForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password Changed Suceessfully!!')
                return render(request, 'myapp/profile.html')
        else:
            form = PasswordChangeCustomForm(request.user)
        return render(request, 'myapp/passwordchange.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# blog search
def search(request):
    if request.method == 'POST':
        searchquery = request.POST.get('search', '')
        searchcontent = BlogPost.objects.filter(content__icontains=searchquery)
        searchtitle = BlogPost.objects.filter(title__icontains=searchquery)
        allpost = searchcontent.union(searchtitle)
        if allpost.count()==0:
            norecord = "oops: No record faund"
            return render(request, 'myapp/blog.html', {'norecord':norecord})
        return render(request, 'myapp/blog.html', {'allpost':allpost})
    else:
        return render(request, 'myapp/blog.html')