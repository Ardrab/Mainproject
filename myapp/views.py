# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import RegistrationForm  # Import your RegistrationForm here
from .models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'index.html')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LabTechnician
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            print(f"User {user.email} authenticated successfully.")
            
            # Check if user is a lab technician and if their profile is completed
            if user.role == 3:  # Lab Technician
                if hasattr(user, 'lab_technicians'):
                    lab_technician = user.lab_technicians.first()
                    if lab_technician and lab_technician.profile_completed:
                        print("Redirecting completed lab tech profile to labtechindex.")
                        return redirect('labtechindex')
                    else:
                        print("Redirecting incomplete lab tech profile to labtechprofile.")
                        return redirect('labtechprofile')
            
            # Check if user is of role 2 and handle profile completion
            elif user.role == 2:  # Role 2 user
                if hasattr(user, 'profiles'):
                    user_profile = user.profiles.first()
                    if user_profile and user_profile.profile_completed:
                        print("Redirecting user with role 2 to lab index.")
                        return redirect('labindex')
                    else:
                        print("Redirecting incomplete profile user with role 2 to labprofile.")
                        return redirect('labprofile')

            # Check user role and redirect accordingly
            if user.is_superuser:
                print("Redirecting superuser to admin index.")
                return redirect('adminindex')  # Redirect to the admin index page if superuser
            elif hasattr(user, 'role'):
                if user.role == 0:
                    print("Redirecting user with role 0 to user index.")
                    return redirect('user_index')  # Redirect to the user index page if role is 0
            else:
                print("Redirecting normal user to user index.")
                return redirect('userindex')  # Redirect to the user index page if no specific role
        else:
            print("Invalid login credentials.")
            error = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')




def register_view(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 0)  # Default role to 0 if not provided

        hashed_password = make_password(password)

        user = User(
            first_name=fname,
            last_name=lname,
            username=email,
            email=email,
            password=hashed_password,
            gender=gender,
            dob=dob,
            phone=phone,
            role=role
        )
        user.save()

        # Example: Store user_id in session after registration
        request.session['user_id'] = user.id

        return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_index(request):
    return render(request, 'user/userindex.html')
def lab_index(request):
    return render(request, 'lab/labindex.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def labtechindex(request):
    # Fetch notifications for the logged-in lab technician
    notifications = Notification.objects.filter(lab_technician__user=request.user).order_by('-created_at')

    # Count unviewed notifications
    unviewed_count = notifications.filter(is_read=False).count()

    return render(request, 'labtech/labtechindex.html', {
        'notifications': notifications,
        'unviewed_count': unviewed_count  # Pass the count to the template
    })

from django.shortcuts import redirect

def logout_view(request):
    # Clear session data
    request.session.flush()

    # Perform logout action

    # Redirect to the index page
    return redirect('index')

def medicalhistory_view(request):
    return render(request, 'user/medicalhistory.html')
def adminindex_view(request):
    return render(request, 'admins/adminindex.html') 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import User

@user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can access this view
def user_list_view(request):
    # Filter users with role=0 and is_staff=False
    users = User.objects.filter(role=0, is_staff=False)
    return render(request, 'admins/user_list.html', {'users': users})
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {'activated' if user.is_active else 'deactivated'} successfully.")
    return redirect('user_list')

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('user_list')
def bloodtest_view(request):
    return render(request, 'user/blood.html')
def urinetest_view(request):
    return render(request, 'user/urine.html')
def swabtest_view(request):
    return render(request, 'user/swab.html')
import secrets
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

def addlab_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        role = request.POST.get('role')  # Get role value from hidden input

        User = get_user_model()
        if User.objects.filter(username=email).exists():
            messages.error(request, "Username (email) already exists.")
            return render(request, 'admins/addlab.html')

        # Generate a random password
        random_password = generate_random_password()

        # Create a new user
        user = User(
            first_name=first_name,
            username=email,  # Use username field for email
            email=email,
            role=role,
            password=make_password(random_password)
        )

        # Save the user
        user.save()

        # Send email with the autogenerated password
        subject = 'Your Account Details for MEDLAB'
        message = f'Hello {first_name},\n\nYour account has been created successfully. Here are your login details:\n\nEmail: {email}\nPassword: {random_password}\n\nPlease change your password after logging in.\n\nBest regards,\nMEDLAB Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            messages.error(request, "Failed to send email with the autogenerated password.")

        messages.success(request, "User added successfully. The autogenerated password has been sent to the provided email address.")
        return redirect('adminindex')

    return render(request, 'admins/addlab.html')




import time
import sqlite3
from django.db import transaction

def addlabtech_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        role = request.POST.get('role')  # Get role value from hidden input

        User = get_user_model()
        if User.objects.filter(username=email).exists():
            messages.error(request, "Username (email) already exists.")
            return render(request, 'lab/addlabtech.html')

        # Generate a random password
        random_password = generate_random_password()

        retries = 5
        while retries > 0:
            try:
                with transaction.atomic():
                    # Create a new user
                    user = User(
                        first_name=first_name,
                        last_name=lname,
                        username=email,  # Use username field for email
                        email=email,
                        role=role,
                        password=make_password(random_password)
                    )
                    # Save the user
                    user.save()
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retries -= 1
                    time.sleep(1)  # Wait for a second before retrying
                else:
                    raise

        if retries == 0:
            messages.error(request, "Failed to add user due to a database lock.")
            return render(request, 'lab/addlabtech.html')

        # Send email with the autogenerated password
        subject = 'Your Account Details for MEDLAB'
        message = f'Hello {first_name},\n\nYour account has been created successfully. Here are your login details:\n\nEmail: {email}\nPassword: {random_password}\n\nPlease change your password after logging in.\n\nBest regards,\nMEDLAB Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            messages.error(request, "Failed to send email with the autogenerated password.")

        messages.success(request, "User added successfully. The autogenerated password has been sent to the provided email address.")
        return redirect('labindex')

    return render(request, 'lab/addlabtech.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

@login_required
def profile_view(request):
    return render(request, 'user/profile_view.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        # Get updated data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')

        # Update the user object
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.gender = gender
        user.dob = dob
        user.phone = phone

        # Save the updated user object
        user.save()

        # Redirect to the profile view or another page
        return redirect('profile')  # Adjust this redirect as needed

    return render(request, 'user/edit_profile.html', {'user': user})
from django.shortcuts import render
from .models import User, UserProfile  # Adjust the import based on your project structure

def labtech_list_view(request):
    # Filter users by role=2 and prefetch related UserProfile data
    users = User.objects.filter(role=2).prefetch_related('profiles')
    return render(request, 'admins/labtech.html', {'users': users})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserProfileForm
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from .models import UserProfile
from .forms import UserProfileForm

User = get_user_model()

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
def labprofile_view(request):
    if request.method == 'POST':
        # Extract form data from POST request
        license_number = request.POST.get('license_number')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Get the currently logged-in user
        user = request.user

        if not user.is_authenticated:
            messages.error(request, 'User is not authenticated')
            return redirect('login')  # Redirect to login if user is not authenticated

        # Check if passwords match and update the password if provided
        if password:
            if password == confirm_password:
                user.set_password(password)  # Use set_password to hash the password
                user.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('labprofile')  # Redirect back to the form

        # Update or create the UserProfile
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'city': city,
                'phone_no': phone,
                'license_no': license_number,
                'profile_completed': True
            }
        )

        messages.success(request, 'User profile updated successfully')
        return redirect('labindex')  # Redirect to labindex after saving profile

    else:
        # Try to get the user's UserProfile or initialize an empty form
        try:
            profile = request.user.profiles.first()  # Changed to access UserProfile via profiles
            form = UserProfileForm(instance=profile)
        except UserProfile.DoesNotExist:
            form = UserProfileForm()

    return render(request, 'lab/labprofile.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from .models import LabTechnician
from .forms import LabTechnicianForm

@login_required
def labtechprofile_view(request):
    user = request.user

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        specialization = request.POST.get('specialization')
        certificate = request.FILES.get('certificate')  # Get the uploaded file

        # Update the user's password if provided
        if password:
            if password == confirm_password:
                user.set_password(password)
                update_session_auth_hash(request, user)  # Update session hash to prevent logout
                user.save()  # Save user with updated password
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('labtechprofile')

        # Update user's dob, gender, and phone
        user.dob = dob if dob else user.dob
        user.gender = gender if gender else user.gender
        user.phone = phone if phone else user.phone
        user.save()

        # Update or create LabTechnician profile
        lab_technician, created = LabTechnician.objects.update_or_create(
            user=user,
            defaults={
                'specialization': specialization,
                'profile_completed': True,
                'certificate': certificate  # Save the uploaded certificate
            }
        )

        messages.success(request, 'User profile updated successfully')
        return redirect('labtechindex')

    else:
        # Try to get the user's LabTechnician profile or initialize an empty form
        try:
            lab_technician = user.lab_technicians.first()
            form = LabTechnicianForm(instance=lab_technician)
        except LabTechnician.DoesNotExist:
            form = LabTechnicianForm()

    return render(request, 'labtech/labtechprofile.html', {'form': form})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LabTechnician

@login_required
def labtech_view(request):
    # Get the currently logged-in user's lab technician profile
    lab_technician = get_object_or_404(LabTechnician, user=request.user)

    return render(request, 'labtech/labtechpro.html', {
        'lab_technician': lab_technician
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestName, UserProfile  # Ensure your models are imported

def addtest_view(request):
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        if test_name:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                new_test_name = TestName(test_name=test_name, lad_id=user_profile)
                new_test_name.save()
                messages.success(request, 'Test name added successfully!')
                return redirect('labindex')  # Redirect to the lab index page after saving
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
                return redirect('addtest')  # Redirect to the lab index page
        else:
            messages.error(request, 'Please enter a test name.')
    
    return render(request, 'lab/addtest.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestName, Tests

def addtestname_view(request):
    if request.method == 'POST':
        test_type_names = request.POST.get('test_type_names')
        name_id = request.POST.get('name_id')
        
        if test_type_names and name_id:
            try:
                test_name = TestName.objects.get(pk=name_id)
                new_test = Tests(name_id=test_name, test_type_names=test_type_names)
                new_test.save()
                messages.success(request, 'Test added successfully!')
                return redirect('labindex')  # Redirect to the lab index page after saving
            except TestName.DoesNotExist:
                messages.error(request, 'Invalid Test Name ID.')
        else:
            messages.error(request, 'All fields are required.')
    
    test_names = TestName.objects.all()
    return render(request, 'lab/addtestname.html', {'test_names': test_names})

from django.shortcuts import render, redirect
from .models import Tests, TestType

# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestType, Tests

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestType, Tests, Amount  # Ensure Amount is imported

def add_test_types(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        tests_names = request.POST.get('tests_names')
        normal_range = request.POST.get('normal_range')
        amount_value = request.POST.get('amount')  # Get the amount from the form

        if test_id and tests_names and normal_range and amount_value:
            try:
                test = Tests.objects.get(test_id=test_id)
                
                # Create and save the TestType
                test_type = TestType(test_id=test, tests_names=tests_names, normal_range=normal_range)
                test_type.save()

                # Create and save the Amount
                amount = Amount(test_type=test_type, amount=float(amount_value))  # Ensure amount is a float
                amount.save()

                messages.success(request, 'Test type and amount added successfully')
                return redirect('labindex')  # Adjust this redirect URL as needed
            except Tests.DoesNotExist:
                messages.error(request, 'Selected test does not exist.')
        else:
            messages.error(request, 'All fields are required.')

    test_names = Tests.objects.all()
    return render(request, 'lab/addtesttypes.html', {'test_names': test_names})

   # myapp/views.py



from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.http import HttpResponse
from django.urls import reverse

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the uidb64 and get the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Invalid password reset link')

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Extract new password and confirm password from POST data
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            print(f"New password: {new_password}")
            print(f"Confirm password: {confirm_password}")

            if new_password and new_password == confirm_password:
                # Set the new password directly
                user.set_password(new_password)
                user.save()

                print("Password updated successfully")

                # Important to update session auth hash after password change
                update_session_auth_hash(request, user)

                return redirect('password_reset_complete')
            else:
                return render(request, 'password_reset_confirm.html', {'error': 'Passwords do not match.'})
        else:
            # Display the form to enter new password
            return render(request, 'password_reset_confirm.html')
    else:
        return HttpResponse('Invalid password reset link')




from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_body = render_to_string(email_template_name, c)
                    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return redirect('password_reset_done')
    else:
        # Display the password reset request form
        return render(request, 'password_reset.html', {'password_reset': True})
def password_reset_complete(request):
    return render(request, 'password_reset_complete.html', {'reset_complete': True})
def password_reset_done(request):
    return render(request, 'password_reset_done.html', {'reset_done': True})
    
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TestName, Tests, TestType
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TestName, Tests, TestType
from django.views.decorators.csrf import csrf_exempt

# View to render the form
def add_test_type_view(request):
    test_names = TestName.objects.all()
    return render(request, 'add_test_type.html', {'test_names': test_names})

# View to handle fetching test types by TestName ID
def get_test_types_by_name(request, name_id):
    tests = Tests.objects.filter(name_id=name_id)
    data = {'test_types': [{'test_id': test.test_id, 'test_type_names': test.test_type_names} for test in tests]}
    return JsonResponse(data)

# View to handle fetching tests by TestType ID
from django.http import JsonResponse

def get_tests_by_type(request, test_id):
    tests = TestType.objects.filter(test_id=test_id).values('testtype_id', 'tests_names')
    return JsonResponse({'tests': list(tests)})
# View to handle form submission
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TestName, TestType, Booking
from datetime import datetime

@login_required
def add_test_type(request):
    if request.method == 'POST':
        # Extract data from the POST request
        test_name_id = request.POST.get('name_id')
        selected_test_types = request.POST.getlist('selected_test_types')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Detailed validation
        errors = []
        if not test_name_id:
            errors.append('Please select a Test Name.')
        if not selected_test_types:
            errors.append('Please select at least one Test Type.')
        if not appointment_date:
            errors.append('Please select an Appointment Date.')
        if not appointment_time:
            errors.append('Please select an Appointment Time.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'user/add_test_type.html', {
                'test_names': TestName.objects.all(),
                'tests': TestType.objects.all(),
                'error': 'Please correct the following errors:'
            })

        try:
            test_name = TestName.objects.get(pk=test_name_id)
        except TestName.DoesNotExist:
            messages.error(request, 'Test Name not found.')
            return redirect('add_test_type')

        try:
            # Convert 12-hour time format to 24-hour time format
            appointment_time_24 = datetime.strptime(appointment_time, '%I:%M %p').strftime('%H:%M')

            # Combine date and time into a single datetime
            appointment_datetime = datetime.combine(
                datetime.strptime(appointment_date, '%Y-%m-%d').date(),
                datetime.strptime(appointment_time_24, '%H:%M').time()
            )
        except ValueError as e:
            messages.error(request, f"Invalid date or time format: {str(e)}")
            return redirect('add_test_type')

        # Check if the time slot is already booked by another user on the same date
        if Booking.objects.filter(appointment_date=appointment_datetime.date(), appointment_time=appointment_datetime.time()).exists():
            messages.error(request, 'This time slot is already booked. Please choose a different time.')
            return render(request, 'user/add_test_type.html', {
                'test_names': TestName.objects.all(),
                'tests': TestType.objects.all(),
                'error': 'The selected time slot is unavailable.'
            })

        # Create and save a new Booking
        booking = Booking(
            user=request.user,
            appointment_date=appointment_datetime.date(),
            appointment_time=appointment_datetime.time(),
            status='pending',  # Default status
            test=test_name,
        )
        booking.save()

        # Ensure selected_test_types are valid testtype_ids
        valid_test_types = [test_type for test_type in selected_test_types if test_type.isdigit()]
        
        if valid_test_types:
            # Set the many-to-many relationship using the TestType objects
            test_types = TestType.objects.filter(testtype_id__in=valid_test_types)
            booking.test_types.set(test_types)
        else:
            messages.warning(request, 'No valid test types were selected.')

        messages.success(request, 'Appointment booked successfully.')
        return redirect('payment', booking_id=booking.id)
    else:
        context = {
            'test_names': TestName.objects.all(),
            'tests': TestType.objects.all(),
        }
        return render(request, 'user/add_test_type.html', context)



from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import Booking

def update_booking_status(request, booking_id, new_status):
    # Fetch the booking object by ID
    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure the new_status is valid by checking against STATUS_CHOICES
    if new_status in dict(Booking._meta.get_field('status').choices):
        booking.status = new_status
        booking.save()  # Save the updated status to the database
        return redirect('booking_list_view')  # Redirect to the booking list view after success
    else:
        return HttpResponse("Invalid status.", status=400)  # Return an error response if the status is invalid



from django.shortcuts import render, get_object_or_404
from .models import Booking, TestType

def booking_list_view(request):
    bookings = Booking.objects.all()
    return render(request, 'lab/booking_detail.html', {'bookings': bookings})
from django.shortcuts import render, get_object_or_404
from .models import Booking, Payment  # Ensure Payment is imported

# myproject/myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import Booking, Payment, CollectionStatus  # Ensure CollectionStatus is imported

def view_booking_details(request, booking_id):
    # Fetch the booking instance
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Fetch the payment status for the booking
    payment = Payment.objects.filter(booking=booking).first()  # Get the first payment related to the booking
    payment_status = payment.status if payment else 'Not Paid'  # Default to 'Not Paid' if no payment exists

    # Fetch test types related to the booking
    test_types = booking.test_types.all()

    # Fetch the collection status for the booking
    collection_status = CollectionStatus.objects.filter(booking=booking).first()  # Get the collection status
    is_collected = collection_status.is_collected if collection_status else False  # Default to False if no status exists

    # Prepare context to pass to the template
    context = {
        'booking': booking,
        'test_types': test_types,
        'payment_status': payment_status,  # Include payment status in the context
        'is_collected': is_collected,  # Include collection status in the context
    }
    
    return render(request, 'lab/view_booking_details.html', context)
from django.shortcuts import get_object_or_404


def user_details_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'lab/user_details.html', {'user': user})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Amount, Payment
from datetime import datetime
import razorpay
from django.conf import settings
import hashlib
import json

import razorpay
from django.conf import settings  # To access Razorpay API keys
from django.http import HttpResponseBadRequest

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def payment_view(request, booking_id):
    try:
        # Fetch the booking instance
        booking = Booking.objects.get(id=booking_id)
        
        # Get all amounts related to the test types in the booking
        amounts = Amount.objects.filter(test_type__in=booking.test_types.all())

        # Calculate the total amount
        total_amount = sum(amount.amount for amount in amounts)
        total_amount_in_paise = int(total_amount * 100)  # Razorpay uses paisa

        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': total_amount_in_paise,  # Amount in paisa
            'currency': 'INR',
            'payment_capture': '1'  # Auto-capture payment
        })

        # Render the payment page with Razorpay order details
        return render(request, 'user/payment.html', {
            'booking': booking,
            'total_amount': total_amount,
            'razorpay_order_id': razorpay_order['id'],  # Pass the order ID to the template
            'razorpay_key': settings.RAZORPAY_KEY_ID,  # Pass the public key to the template
        })

    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('user_index')


@login_required
def process_payment(request, booking_id):
    if request.method == 'POST':
        # Get Razorpay payment details from the form
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        try:
            # Fetch the booking instance
            booking = Booking.objects.get(id=booking_id)
            
            # Get the amount associated with the booking's test types
            amount = Amount.objects.filter(test_type__in=booking.test_types.all()).first()

            if not amount:
                messages.error(request, 'No amount found for the selected tests.')
                return redirect('user_index')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                messages.error(request, 'Payment signature verification failed.')
                return HttpResponseBadRequest()

            # Create a new payment record
            payment = Payment(
                booking=booking,
                amount=amount,
                payment_date=datetime.now().date(),
                status='completed'  # Set status to completed after successful payment
            )
            payment.save()

            # Update the booking status
            booking.status = 'scheduled'
            booking.save()

            messages.success(request, 'Payment successful! Your appointment is confirmed.')
            return redirect('user_index')

        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
            return redirect('user_index')

    # If not a POST request, redirect to the user index
    return redirect('user_index')



@login_required
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        # Create a signature hash
        params = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated_signature = hashlib.sha256((params + settings.RAZORPAY_API_SECRET).encode('utf-8')).hexdigest()

        if generated_signature == razorpay_signature:
            try:
                # Fetch the payment instance for the given order ID
                payment = Payment.objects.get(booking__id=razorpay_order_id)

                # Update payment status
                payment.status = 'completed'
                payment.save()

                messages.success(request, 'Payment verified successfully!')
                return JsonResponse({'success': True})
            except Payment.DoesNotExist:
                messages.error(request, 'Payment record not found.')
                return JsonResponse({'success': False})
        else:
            messages.error(request, 'Payment verification failed.')
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})

from django.shortcuts import render, redirect, get_object_or_404
from .models import LabTechnicianSchedule, LabTechnician, Booking, Notification
from .forms import LabTechnicianScheduleForm

def schedule_lab_technician_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        technician_id = request.POST.get('technician')
        technician = get_object_or_404(LabTechnician, labtech_id=technician_id)

        # Check if the technician is already scheduled for the same booking_id
        if LabTechnicianSchedule.objects.filter(technician=technician, booking=booking).exists():
            error_message = 'This technician is already scheduled for this booking.'
            return render(request, 'lab/schedule_labtech.html', {
                'form': LabTechnicianScheduleForm(),
                'booking': booking,
                'error_message': error_message
            })

        # Create a new schedule entry
        schedule = LabTechnicianSchedule(technician=technician, booking=booking)
        schedule.save()

        # Create a notification for the technician
        Notification.objects.create(
            lab_technician=technician,
            message=f'You have been scheduled for a booking on {booking.appointment_date}.'
        )

        return redirect('labindex')
    else:
        form = LabTechnicianScheduleForm()

    return render(request, 'lab/schedule_labtech.html', {'form': form, 'booking': booking})


def get_technicians(request):
    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        specialization = request.GET.get('specialization')
        
        # Debugging: Print the specialization received
        print(f"Requested specialization: {specialization}")
        
        technicians = LabTechnician.objects.filter(specialization=specialization)
        
        # Debugging: Print the number of technicians found
        print(f"Found {technicians.count()} technicians with specialization '{specialization}'")
        
        # Create a list of technicians to return as JSON, fetching first name and last name from the User model
        technician_list = [
            {
                'id': technician.labtech_id,
                'name': f"{technician.user.first_name} {technician.user.last_name}"  # Concatenate first and last name
            } for technician in technicians
        ]
        
        return JsonResponse(technician_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
# myproject/myapp/views.py
# myproject/myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import LabTechnicianSchedule, CollectionStatus, LabTechnician, Booking, Notification  # Ensure Notification is imported

def view_scheduled_requests(request):
    technician = get_object_or_404(LabTechnician, user=request.user)
    scheduled_requests = LabTechnicianSchedule.objects.filter(technician=technician)

    detailed_requests = []
    for schedule in scheduled_requests:
        booking = schedule.booking
        test_types = booking.test_types.all()

        test_type_names = ", ".join([test_type.tests_names for test_type in test_types]) if test_types else "No test types available"

        # Get or create the collection status
        collection_status, created = CollectionStatus.objects.get_or_create(booking=booking)

        detailed_requests.append({
            'appointment_date': booking.appointment_date,
            'appointment_time': booking.appointment_time,
            'user_name': f"{booking.user.first_name} {booking.user.last_name}",
            'test_types': test_type_names,
            'booking_id': booking.id,
            'is_collected': collection_status.is_collected,  # Include collection status
            'technician_id': collection_status.technician.labtech_id if collection_status.technician else None,  # Use labtech_id
        })

    # Calculate the count of unread notifications for the current lab technician
    unviewed_count = Notification.objects.filter(is_read=False, lab_technician=technician).count()

    return render(request, 'labtech/view_scheduled_request.html', {
        'scheduled_requests': detailed_requests,
        'unviewed_count': unviewed_count,  # Pass the count to the template
    })
 # Redirect back to the scheduled requests view  # Ensure you have the correct imports
# myproject/myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import LabTechnicianSchedule, CollectionStatus, LabTechnician
from django.views.decorators.cache import never_cache


def toggle_collection_status(request, booking_id):
    # Get the collection status for the specified booking
    collection_status = get_object_or_404(CollectionStatus, booking__id=booking_id)
    
    # Toggle the collection status
    collection_status.is_collected = not collection_status.is_collected
    
    # Set the technician who collected the sample
    if collection_status.is_collected:
        collection_status.technician = get_object_or_404(LabTechnician, user=request.user)  # Set technician who collected
    else:
        collection_status.technician = None  # Clear technician if not collected
    
    # Save the updated collection status
    collection_status.save()
    
    # Redirect back to the scheduled requests view
    return redirect('view_scheduled_requests')

@login_required
@never_cache
def view_notifications(request):
    # Fetch notifications for the logged-in lab technician
    notifications = Notification.objects.filter(lab_technician__user=request.user).order_by('-created_at')

    # Mark notifications as read
    notifications.update(is_read=True)

    # Count unviewed notifications
    unviewed_count = notifications.filter(is_read=False).count()

    return render(request, 'labtech/view_notifications.html', {
        'notifications': notifications,
        'unviewed_count': unviewed_count  # Pass the count to the template
    })
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LabTechnician, LabTechnicianSchedule

@login_required
def unscheduled_lab_technicians(request):
    # Get all lab technicians
    all_technicians = LabTechnician.objects.all()
    
    # Get scheduled technicians
    scheduled_technicians = LabTechnicianSchedule.objects.values_list('technician', flat=True)
    
    # Filter out scheduled technicians
    unscheduled_technicians = all_technicians.exclude(labtech_id__in=scheduled_technicians)

    return render(request, 'lab/unscheduled_lab_technicians.html', {
        'unscheduled_technicians': unscheduled_technicians,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Booking  # Ensure you have the correct import

@login_required
def user_bookings(request):
    # Fetch all bookings for the logged-in user, prefetching related test types
    bookings = Booking.objects.filter(user=request.user).prefetch_related('test_types').order_by('-appointment_date')

    return render(request, 'user/user_bookings.html', {
        'bookings': bookings
    })
# myproject/myapp/views.py
# myproject/myapp/views.py
# myproject/myapp/views.py
# myproject/myapp/views.py
# myproject/myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, CollectionStatus, TestResult, TestValue, Notification, LabTechnician, TestType  # Ensure all models are imported

@never_cache
@never_cache
def create_test_result(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    collection_status = get_object_or_404(CollectionStatus, booking=booking)

    # Fetch available test types for the booking
    test_types = booking.test_types.all()

    # Get the LabTechnician instance for the current user
    lab_technician = get_object_or_404(LabTechnician, user=request.user)

    # Calculate the count of unread notifications for the current lab technician
    unviewed_count = Notification.objects.filter(is_read=False, lab_technician=lab_technician).count()

    if request.method == 'POST':
        test_type_ids = request.POST.getlist('test_types')  # Get the selected test type IDs
        result_values = request.POST.get('result_value')  # Get the result values as a string

        # Split the result values by the delimiter (assuming comma here)
        result_values_list = result_values.split(',')

        if test_type_ids and len(test_type_ids) == len(result_values_list):  # Ensure both fields are filled and match in length
            test_result = TestResult.objects.create(collection_status=collection_status)

            # Associate each test type with its corresponding result value
            for test_type_id, result_value in zip(test_type_ids, result_values_list):
                test_type = get_object_or_404(TestType, testtype_id=test_type_id)
                test_result.test_types.add(test_type)  # Add the test type to the many-to-many field
                
                # Create a TestValue entry for each test type and result value
                TestValue.objects.create(test_result=test_result, result_value=result_value.strip())  # Store the trimmed result value

            return redirect('view_scheduled_requests')  # Redirect to the booking details page

    return render(request, 'labtech/add_test_result.html', {
        'booking': booking,
        'test_types': test_types,
        'unviewed_count': unviewed_count,  # Pass the count to the template
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, CollectionStatus, TestResult

def view_test_results(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    # Check booking status first
    if booking.status == 'complete':
        booking.status = 'scheduled'  # Change status to 'scheduled' if it's complete
    elif booking.status == 'pending':
        booking.status = 'pending'  # Keep status as 'pending' if it was pending

    # Attempt to get the collection status for the booking
    try:
        collection_status = CollectionStatus.objects.get(booking=booking)

        # Update booking status based on collection status
        if collection_status.is_collected:  # Assuming `is_collected` is a boolean field in CollectionStatus
            booking.status = 'collected'  # Change booking status to 'collected'
        else:
            booking.status = 'pending'  # If not collected, set status to 'pending'

        booking.save()  # Save the updated booking status

    except CollectionStatus.DoesNotExist:
        # Redirect to a page that informs the user that the sample collection is not done
        return render(request, 'user/sample_collection_not_done.html', {
            'booking': booking,
        })

    # Fetch test results associated with the collection status
    test_results = TestResult.objects.filter(collection_status=collection_status).prefetch_related('values', 'test_types')

    # Fetch the test types associated with the booking
    test_types = booking.test_types.all()

    return render(request, 'user/view_test_results.html', {
        'booking': booking,
        'test_results': test_results,  # Pass the test results to the template
        'test_types': test_types,  # Pass the test types to the template
    })

# myproject/myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import Booking, CollectionStatus, TestResult, TestValue, Notification, LabTechnician, TestType  # Ensure all models are imported

# def view_test_results(request, booking_id):
#     booking = get_object_or_404(Booking, pk=booking_id)
#     collection_status = get_object_or_404(CollectionStatus, booking=booking)

#     # Fetch test results associated with the collection status
#     test_results = TestResult.objects.filter(collection_status=collection_status).prefetch_related('values')

    

#     # Calculate the count of unread notifications for the current lab technicianunviewed_count = Notification.objects.filter(is_read=False, lab_technician=lab_technician).count()

#     # Fetch the test types associated with the booking
#     test_types = booking.test_types.all()

#     return render(request, 'user/view_test_results.html', {
#         'booking': booking,
#         'test_results': test_results,  # Pass the test results to the template
#         'test_types': test_types,  # Pass the test types to the template
#           # Pass the count to the template
#     })
# myproject/myapp/views.py
# myproject/myapp/views.py
# myproject/myapp/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from .models import Booking, CollectionStatus, TestResult, TestValue, LabTechnician

def download_test_report_by_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    collection_status = get_object_or_404(CollectionStatus, booking=booking)
    
    # Fetch the lab technician using the correct field "technician" in CollectionStatus
    lab_technician = collection_status.technician

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="test_report_booking_{booking_id}.pdf"'

    # Create a PDF document with ReportLab's SimpleDocTemplate
    buffer = response
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles for the PDF
    styles = getSampleStyleSheet()

    # Custom styles for lab name and titles
    large_bold_style = ParagraphStyle(
        name='LargeBold',
        fontSize=18,
        leading=22,
        fontName='Helvetica-Bold',
        alignment=1,  # Center alignment
    )
    normal_bold_style = ParagraphStyle(
        name='NormalBold',
        fontSize=12,
        fontName='Helvetica-Bold',
        alignment=0,  # Left alignment
    )

    elements = []

    # Lab name and booking details in bold and large font
    elements.append(Paragraph("MedLab Diagnostic Center", large_bold_style))
    elements.append(Spacer(1, 0.2 * inch))  # Spacer to add space between elements
    elements.append(Paragraph(f"Test Report for Booking ID: {booking_id}", normal_bold_style))
    elements.append(Paragraph(f"Patient: {booking.user.first_name} {booking.user.last_name}", styles['Normal']))
    elements.append(Paragraph(f"Date of Appointment: {booking.appointment_date}", styles['Normal']))
    
    if lab_technician:
        elements.append(Paragraph(f"Test conducted by: {lab_technician.user.first_name} {lab_technician.user.last_name}", styles['Normal']))
    else:
        elements.append(Paragraph("Test conducted by: N/A", styles['Normal']))
    
    elements.append(Spacer(1, 0.3 * inch))  # Add more space before showing test results

    # Fetch test results associated with the collection status
    test_results = TestResult.objects.filter(collection_status=collection_status).prefetch_related('values', 'test_types')

    # Create a table with headers
    table_data = [["Test Name", "Result"]]  # Two columns: Test Name and Result

    # Loop through each test result and split result values by commas into separate rows
    for result in test_results:
        test_types = result.test_types.all()  # Get all test types related to this result
        result_values = result.values.all()  # Get all result values related to this result

        # Process each test type and corresponding result values
        for test_type, value in zip(test_types, result_values):
            # Split the result value by commas and create a row for each result
            split_values = value.result_value.split(",")  # Split result value by commas
            for single_value in split_values:
                row = [test_type.tests_names, single_value]  # Each result in a new row under the test name
                table_data.append(row)

        # Handle cases where the number of test types and result values do not match
        for test_type in test_types[len(result_values):]:
            table_data.append([test_type.tests_names, "N/A"])

        for value in result_values[len(test_types):]:
            table_data.append(["N/A", value.result_value])

    # Create the table with separated test names and result values into different rows
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    return response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.contrib import messages

@login_required
def generate_bill(request, booking_id):
    try:
        # Fetch the booking and payment details
        booking = Booking.objects.get(id=booking_id)
        payment = Payment.objects.get(booking=booking)

        # Fetch related test types through the booking
        test_types = booking.test_types.all()

        # Fetch the corresponding amount for each test type and calculate the total amount
        total_amount = 0
        test_details = []  # To store the test types and their amounts

        for test_type in test_types:
            amount_obj = get_object_or_404(Amount, test_type=test_type)  # Get the related amount
            test_details.append({
                'test_type': test_type,
                'amount': amount_obj.amount  # Store the amount for this test type
            })
            total_amount += amount_obj.amount  # Sum the amount for each test type

        # Load the HTML template
        template = get_template('user/bill_template.html')
        html = template.render({
            'booking': booking,
            'payment': payment,
            'test_details': test_details,  # Pass test details (test type and amount) to the template
            'total_amount': total_amount,  # Pass the calculated total amount
            'request': request,  # Pass request to get user info
        })

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bill_{booking.id}.pdf"'

        # Generate the PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating bill', status=400)
        return response

    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('user_index')
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found.')
        return redirect('user_index')

