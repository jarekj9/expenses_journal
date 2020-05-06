#!/usr/bin/python3
from .models import *
from django.contrib.auth.models import User

def main():

    output=[]
    if not Categories.objects.filter(category='inne').count():
        record = Categories(category='inne', login=User.objects.get(username='jarek').login_id)
        Categories.objects.get(category=category)
        record.save()
        
    #record = Journal(login='Jarek', value=100, category=Categories.objects.get(category='inne'), description='Test')
    #record.save()
    
    
    all_records = Journal.objects.all()
    for item in all_records:
        output.append({'id':item.id,
                       'login':item.login.username,  #related object
                       'date':item.date.strftime("%d-%m-%Y"),
                       'value':item.value,
                       'category':item.category.category,  #related object
                       'description':item.description})
    
    return output
    

if __name__ == '__main__':
    
    main()
  










