from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors ={}
        if len(reqPOST['UserFname']) < 2 :
            errors['UserFname'] ='First Name should at least be 2 characters'
        if len(reqPOST['UserLname']) < 2  :
            errors['UserLname'] ='Last Name should at least be 2 characters'
        
        EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['UserMail']):
            errors['UserMail']='Email in wrong format'
        
        User_with_email = User.objects.filter(Email=reqPOST['UserMail'])
        if len(User_with_email)>= 1:
            errors['Taken'] ='Email already taken'

        if len(reqPOST['Userpass']) < 8  :
            errors['Userpass'] ='Password should at least be 8 characters'
        if reqPOST['Userpass'] != reqPOST['UserconfirmPass']:
            errors['matching'] = 'Password must match'
        
        return errors
    
    def Edit_validator(self, reqPOST):
        errors={}
        if len(reqPOST['EUserFname']) < 2 :
            errors['EUserFname'] ='First Name should at least be 2 characters'
        if len(reqPOST['EUserLname']) < 2  :
            errors['EUserLname'] ='Last Name should at least be 2 characters'
        
        EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['EUserMail']):
            errors['UserMail']='Email in wrong format'
        
        User_with_email = User.objects.filter(Email=reqPOST['EUserMail'])
        if len(User_with_email)>= 1:
            errors['Taken'] ='Email already taken'

        return errors
    

class QuotesManager(models.Manager):
    def Quote_validator(self, reqPOST):
        errors ={}
        if len(reqPOST['Post_Author']) < 3 :
            errors['Post_Author'] ='Author Name should at least be 3 characters'
        if len(reqPOST['Post_Quote']) < 10  :
            errors['Post_Quote'] ='Quotes should at least be 10 characters'
        return errors

class User(models.Model):
    First_Name = models.CharField(max_length=45)
    Last_Name = models.CharField(max_length=45)
    Email = models.TextField()
    Password = models.TextField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quotes(models.Model):
    Author_name = models.CharField(max_length=45) 
    desc= models.CharField(max_length=445)
    User_postingQuotes= models.ForeignKey(User, related_name='Quotes_posted', on_delete=models.CASCADE)
    USers_who_liked_Quotes = models.ManyToManyField(User, related_name='Quotes_liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuotesManager()

