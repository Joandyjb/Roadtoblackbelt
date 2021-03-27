
from django.shortcuts import render, redirect

from BlackApp.models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request,'LoginRegister.html')


def create(request):
    if request.method =='POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['Userpass']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            New_User = User.objects.create(
                First_Name = request.POST['UserFname'],
                Last_Name = request.POST['UserLname'],
                Email = request.POST['UserMail'],
                Password =pw_hash)
            request.session['User_id'] = New_User.id
            return redirect('/user/quotes')
    return redirect('/')






def login(request):
    if request.method =='POST':
        User_with_email= User.objects.filter(Email = request.POST['UserMail'])
        if User_with_email:
            user = User_with_email[0]
            if bcrypt.checkpw(request.POST['Userpass'].encode(), user.Password.encode()):
                request.session['User_id'] = user.id
                return redirect('/user/quotes')
        messages.error(request, "Email or Password are incorrect!")
    return redirect('/')

def Dashboard(request):
    if 'User_id' not in request.session:
        return redirect('/')
    context = {
        'current_user':User.objects.get(id=request.session['User_id']),
        'all_Quotes': Quotes.objects.all()
        }
    
    return render(request,'dashboard.html', context)

def create_quotes(request):
    if request.method =='POST':
        errors = Quotes.objects.Quote_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/user/quotes')
        else:
            New_User = Quotes.objects.create(
                Author_name = request.POST['Post_Author'],
                desc = request.POST['Post_Quote'],
                User_postingQuotes = User.objects.get(id=request.session['User_id']))
            return redirect('/user/quotes')
    return redirect('/')



def UserPosterProfile(request, Userposter_id ):
    # if 'User_id' not in request.session:
    #     return redirect('/')
    userposter = User.objects.get(id=Userposter_id)
    context ={
        'theUser': userposter
    }
    return render(request, "profile.html", context)


def editprofile(request, current_user_id):
    if 'User_id' not in request.session:
        return redirect('/')
    profile_to_edit= User.objects.get(id=current_user_id)
    context= {
        'UserEditobject': profile_to_edit
    }

    return render(request, 'editProfile.html', context)

def updatedprofile(request, UserUptade_id):
    if request.method =='POST':
        errors = User.objects.Edit_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/myaccount/{UserUptade_id}')
        else:
            # User_with_email= User.objects.filter(Email = request.POST['EUserMail'])
            User_with_email= User.objects.get(id =UserUptade_id)
            # if User_with_email:
            userlog = User_with_email
            userlog.First_Name= request.POST['EUserFname']
            userlog.Last_Name = request.POST['EUserLname']
            userlog.Email= request.POST['EUserMail']
            userlog.save()
            messages.success(request, 'Profile has been Succesfully Updated!')
            
            # return redirect (f'/user/{UserUptade_id}')
            return redirect(f'/myaccount/{UserUptade_id}')
    return redirect('/user/quotes')
    



def logout(request):
    request.session.flush()
    return redirect('/')

def returnp(request):

    return redirect ('/user/quotes')

def delete(request, quote_id ):
    if request.method =='POST':
        quote_to_delete =  Quotes.objects.get(id=quote_id)
        quote_to_delete.delete()
        return redirect('/user/quotes')
    return redirect('/user/quotes')

def like_quote (request, quote_id ):
    if  'user_id' not in request.session:
        quote_message = Quotes.objects.get(id=quote_id)
        quote_message.USers_who_liked_Quotes.add(User.objects.get(id=request.session['User_id']))
        quote_message.save()
        return redirect('/user/quotes')
    return redirect('/')




