from django.shortcuts import render,HttpResponse
import datetime
import requests
from django.contrib import messages
import os

# Create your views here.

def home(request):
    
    if 'city' in request.POST:
        city=request.POST['city']
    else:
        city='Munnar'    
        
    url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=976c9a28685bfee2be7b6eac54f1e7b5'
    PARAMS={'units':'metric'}
    
        
    
    #API_KEY='GOOGLE_API_KEY'
    #SECRET_ENGINE_ID='GOOGLE_SEARCH_ENGINE_ID'
    
    API_KEY = os.getenv('GOOGLE_API_KEY')
    SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    
    query=city + "1920x1080"
    page=1
    start=(page-1) * 10 + 1
    searchType='image'
    city_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={API_KEY}&searchType={searchType}&start={start}"
    
    data=requests.get(city_url).json()
    count=1
    search_items=data.get("items")
       
    default_image="https://images.pexels.com/photos/457882/pexels-photo-457882.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"    
    
    if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
    else:
            image_url =default_image

    
    
    try:
        data=requests.get(url,PARAMS).json()
        description=data['weather'][0]['description']
        icon=data['weather'][0]['icon']
        temp=data['main']['temp']
        
        day=datetime.date.today()
        
        return render(request,'weatherapp/index.html',{'description':description,'icon':icon,'temp':temp,'day':day,"city":city,'exception_occured':False,'image_url':image_url})

    except:
        exception_occured=True
        messages.error(request,'Entered data is not avilable')
        day=datetime.date.today()
        
        return render(request,'weatherapp/index.html',{'description':'clear sky','icon':'01d','temp':22,'day':day,"city":'Munnar','exception_occured':True,'image_url':default_image})
