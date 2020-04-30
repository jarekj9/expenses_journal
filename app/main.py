#!/usr/bin/python3
from .models import *


def main():
    # Create a new record using the model's constructor.
    
    if not Categories.objects.filter(category='inne').count():
        record = Categories(category='inne')
        record.save()
    
    all_records = Categories.objects.all()
    print('categories:')
    for line in all_records:
        print(line)
    
    record = Journal(login='Jarek', value=100, category=Categories.objects.get(category='inne'), description='Test')
    record.save()
    
    
    all_records = Journal.objects.all()
    print('all records:')
    print(all_records)
    print('end')
    
    return 'Jarek'
    

if __name__ == '__main__':
    
    main()
  










