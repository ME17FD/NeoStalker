from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import person

import hashlib
logged = False
# Create your views here.
def addscrn(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
    done=''
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        if request.POST['ismale']==0:
            ismale = False
        else:
            ismale = True
        email = request.POST['email']
        phone = request.POST['pnumber']
        cin = request.POST['cin']
        cen = request.POST['cen']
        info = request.POST['info']
        bday = request.POST.get('bday',"")
        new = person(fname= fname,lname=lname,ismale=ismale,email=email,phone=phone,cin=cin,cen=cen,info=info,bday=bday)
        if new.cin == "":
            print("no primary key")
            done="failed adding"
        else:
            new.save()
            print(f'{fname} saved')
            done = "added successfully"
            all_person = len(person.objects.all())


    all_person = len(person.objects.all())
    """for i in all_person:
        print(i.fname)"""
    return render(request,'inputs.html',{
        'done':done,
        'total':all_person
    })



def displayscrn(request):
    model_fields = ["fname", "lname", "email","phone",'cin','cen']
    if not request.user.is_authenticated:
        return redirect('login')
    
    

    query = request.GET.get('q','')
    if ' ' in query and query != " ":
        subq = []
        for i in query.split(' '):
            q_filter = Q()
            for field in model_fields:
                q_filter |= Q(**{f"{field}__icontains": i})
            subq.append(q_filter)
        
        
        for q in subq:
            q_filter &= q
        
    else:
        q_filter = Q()
        for field in model_fields:
            q_filter |= Q(**{f"{field}__icontains": query})
    
    all_person = person.objects.filter(q_filter).order_by("?")
    total = len(all_person)


    return render(request,'display.html',
                  {
                      "all_todos":all_person,
                      'total': total,
                      'query' : query
                  })
    
def Login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = str(request.POST['password'])
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("display")
    return render(request,'login.html')


def logoutview(request):
    logout(request)
    return redirect('login')