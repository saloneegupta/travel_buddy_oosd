from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import User_details, Cab, Passengers
from .forms import SignUpForm

# Create your views here.
def view_cabs(request):
    cabs = Cab.objects.all()
    return render(request, 'view_cabs.html', {'cabs': cabs})

@login_required(login_url='/login')
def cab_info(request, pk):
    cab = get_object_or_404(Cab, id=pk)
    passengers = list(Passengers.objects.filter(of_cab=pk))
    if request.method == 'POST':
        username = request.user.username
        user = get_object_or_404(User, username=username) # checked that user exists
        if (Passengers.objects.filter(user=user, of_cab=cab).count()) > 0:
            return redirect('cab_info', pk=pk)
        else:
            passengers = Passengers.objects.create(
                user = user,
                of_cab = cab,
                is_cab_admin = 0,
                approval_status = 'r',
            )
        return redirect('cab_info', pk=pk)
    try:
        current_user = Passengers.objects.get(user = request.user, of_cab = cab)
    except Passengers.DoesNotExist:
        current_user = None
    if current_user != None:
        if current_user.approval_status == 'a':
            contact_access=True
        else:
            contact_access=False
    else:
        contact_access=False
    
    return render(request, 'cab_info.html', {'cab': cab, 'passengers': passengers, 'contact_access': contact_access})

@login_required(login_url='/login')
def contact_details(request, pk):
    current_user = Passengers.objects.get(user = request.user, of_cab = pk)
    if current_user.approval_status == 'a':
        cab = get_object_or_404(Cab, id=pk)
        passengers = list(Passengers.objects.filter(of_cab=pk, approval_status='a'))
        for passenger in passengers:
            passenger_contact_details = list(User_details.objects.filter(user = passenger.user))
        
        return render(request, 'contact_details.html', {'cab': cab, 'passengers': passengers, 'passenger_contact_details': passenger_contact_details})
    
    return render(request, 'not_authorized.html')

@login_required(login_url='/login')
def approve_cab(request, pk_cab, pk_user):
    cab = get_object_or_404(Cab, id=pk_cab)
    user = get_object_or_404(User, username=pk_user)
    passenger = Passengers.objects.get(of_cab=pk_cab, user=user)
    #if request.method == 'POST':
    passenger.approval_status = 'a'
    passenger.save()

    passengers = list(Passengers.objects.filter(of_cab=pk_cab))
    return render(request, 'manage_cab.html', {'cab': cab, 'passengers': passengers})


@login_required(login_url='/login')
def decline_cab(request, pk_cab, pk_user):
    cab = get_object_or_404(Cab, id=pk_cab)
    user = get_object_or_404(User, username=pk_user)
    passenger = Passengers.objects.get(of_cab=pk_cab, user=user)
    #if request.method == 'POST':
    passenger.approval_status = 'd'
    passenger.save()

    passengers = list(Passengers.objects.filter(of_cab=pk_cab))
    return render(request, 'manage_cab.html', {'cab': cab, 'passengers': passengers})


def user_info_for_request_cab(request, pk):
    cab = get_object_or_404(Cab, id=pk) # checked that cab exists
    if request.method == 'POST':
        username = request.POST['username']
        user = get_object_or_404(User, username=username) # checked that user exists
        passengers = Passengers.objects.create(
            user = user,
            of_cab = cab,
            is_cab_admin = 0,
            approval_status = 'r',
        )

        return redirect('cab_info', pk=pk)

    return render(request, 'user_info_for_request_cab.html')

def user_info_for_user_details(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = get_object_or_404(User, username=username)
        return redirect('user_details', username=user)

    return render(request, 'user_info_for_user_details.html')

def user_info_for_new_cab(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = get_object_or_404(User, username=username)
        return redirect('new_cab', username=user)

    return render(request, 'user_info_for_new_cab.html')

@login_required(login_url='/login')
def user_details(request, username):
    user = get_object_or_404(User, username=username) # TODO: get the currently logged in user
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        contact_no = request.POST['contact_no']
        contact_sharing = request.POST['contact_sharing']

        current_user = User.objects.get(username=username)

        user_details = User_details.objects.create(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        dob = dob,
        contact_no = contact_no,
        contact_sharing = contact_sharing,
        user = current_user,
        )

        return redirect('view_cabs')  # TODO: redirect to the created topic page

    return render(request, 'user_details.html',{'User': user})

@login_required(login_url='/login')
def new_cab(request, username):
    user = get_object_or_404(User, username=username) # TODO: get the currently logged in user
    if request.method == 'POST':
        destination = request.POST['destination']
        source = request.POST['source']
        dep_date = request.POST['dep_date']
        dep_time = request.POST['dep_time']
        dep_date_time = dep_date + ' ' + dep_time
        size = request.POST['size']

        current_user = User.objects.get(username=username)

        cab = Cab.objects.create(
        source = source,
        destination = destination,
        dep_date_time = dep_date_time,
        size = size,
        cab_admin = current_user,
        )

        created_cab = Cab.objects.get(
            source = source,
            destination = destination,
            dep_date_time = dep_date_time,
            size = size,
            cab_admin = current_user,
            )

        passengers = Passengers.objects.create(
            user = current_user,
            of_cab = created_cab,
            is_cab_admin = 1,
            approval_status = 'a',
        )

        return redirect('view_cabs')  # TODO: redirect to the created cab page
    
    return render(request, 'new_cab.html',{'User': user})

def user_info_for_admin_panel(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = get_object_or_404(User, username=username)
        return redirect('cab_admin_panel', username=user)
    return render(request, 'user_info_for_admin_panel.html')

@login_required(login_url='/login')
def cab_admin_panel(request, username):
    user = get_object_or_404(User, username=username)
    cabs = list(Cab.objects.filter(cab_admin=user))

    return render(request, 'cab_admin_panel.html', {'User': user,'cabs': cabs})

@login_required(login_url='/login')
def manage_cab(request, username, pk):
    cab = get_object_or_404(Cab, id=pk)
    user = get_object_or_404(User, username=username) 
    passengers = list(Passengers.objects.filter(of_cab=pk))

    return render(request, 'manage_cab.html', {'cab': cab, 'passengers': passengers})

def signup(request):
    # TODO: If user is already logged in, redirect him/her to the view_cabs page
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('view_cabs')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})