from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecord
from .models import Record

def home(request):
    records = Record.objects.all()
    # check if user is logging in. If yes, then we want to grab their info
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate. check if the above info is correct
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #giving a message
            messages.success(request, "You've successfully logged in!!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in. Please try again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})
    
def logout_user(request):
    logout(request)
    messages.success(request, "You've successfully logged out!!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #checking if the form is valid
        if form.is_valid():
            form.save()
            #Lets Immediately Login & Authenticate the valid user
            username = form.cleaned_data['username'] #cleaned_data: to only pull username from whatever the user post in SignUpForm
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You've Successfully Registered!")
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})    
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    ## we want only authenticated users to see the records
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk) # .get() to get the specific record based on id  
        return render(request, 'record.html', {'customer_record':customer_record})
    else: 
        messages.success(request, "You Must Be Logged In To View Records!")
        return redirect('home')

def delete_record(request, pk):
        if request.user.is_authenticated:
            delete_record = Record.objects.get(id=pk)
            delete_record.delete()
            messages.success(request, "You've Deleted A Record!")
            return redirect('home')
        else: 
            return redirect('home') 

def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecord(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect('home')
        else:
            form = AddRecord()
            return render(request, 'add_record.html', {'form': form})
    else:  
        messages.success(request, 'You must be Logged in')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You must be Logged in')
        return redirect('home')
