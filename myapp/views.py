from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import person
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
logger = logging.getLogger(__name__)



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
    empty_name_persons = person.objects.filter(Q(fname__isnull=True) | Q(fname__exact='') | Q(lname__isnull=True) | Q(lname__exact=''))
    # Get the count of objects to be deleted
    count = empty_name_persons.count()

    # Delete the objects
    empty_name_persons.delete()

    # Output the result
    print(f'Successfully deleted {count} person objects without a first name or last name.')
    model_fields = ["fname", "lname", "email", "phone", "cin", "cen","info"]
    
    # Redirect if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get the search query
    query = request.GET.get('q', '')
    
    # Build the filter query
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
    
    # Fetch filtered data
    all_person = person.objects.filter(q_filter).order_by("?")
    total = len(all_person)
    
    # Pagination
    number_per_page = 50
    paginator = Paginator(all_person, number_per_page)  
    page_number = request.GET.get('page')  # Get the current page number from the request
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, 'display2.html', {
        "page_obj": page_obj,  # Pass the paginated data
        'total': total,
        'query': query
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


def upload_excel(request):
    """
    Handles the upload of an Excel file, processes it, and updates the database.
    """
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Validate file type and size
        if not excel_file.name.endswith('.xlsx') and not excel_file.name.endswith('.xls'):
            messages.error(request, "Invalid file type. Please upload a .xlsx file.")
            return redirect('input')
        
        
        fs = FileSystemStorage()
        try:
            # Save the file temporarily
            filename = fs.save(excel_file.name, excel_file)
            file_path = fs.path(filename)
            
            # Process the Excel file
            process_excel_file(request, file_path, filename)
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            messages.error(request, f"An error occurred while processing the file: {e}")
        finally:
            # Clean up: Delete the temporary file
            if fs.exists(filename):
                fs.delete(filename)
        
        return redirect('input')  # Redirect to input page after upload
    
    return redirect('input')


def logoutview(request):
    logout(request)
    return redirect('login')