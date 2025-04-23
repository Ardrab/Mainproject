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
from django.views.decorators.cache import never_cache

from django.contrib.auth.decorators import login_required

import cv2
import numpy as np
import base64
from django.core.files.base import ContentFile

def index_view(request):
    return render(request, 'index.html')

import base64
import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        face_image = request.POST.get('face_image')

        try:
            # Get the user from the database based on the email
            user = User.objects.get(email=email)

            if face_image:  # If a face image is provided for login
                try:
                    # Convert base64 to image
                    format, imgstr = face_image.split(';base64,')
                    image_data = base64.b64decode(imgstr)
                    
                    # Convert to numpy array
                    nparr = np.frombuffer(image_data, np.uint8)
                    live_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    # Convert live image to grayscale
                    live_gray = cv2.cvtColor(live_img, cv2.COLOR_BGR2GRAY)
                    
                    # Detect faces in the live image
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    faces = face_cascade.detectMultiScale(live_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    if len(faces) == 0:
                        messages.error(request, 'No face detected. Please try again.')
                        return render(request, 'login.html')

                    if len(faces) > 1:
                        messages.error(request, 'Multiple faces detected. Please ensure only your face is visible.')
                        return render(request, 'login.html')

                    # Extract the first face found (face ROI)
                    (x, y, w, h) = faces[0]
                    live_face = live_gray[y:y+h, x:x+w]
                    live_face_resized = cv2.resize(live_face, (128, 128))

                    # Check if the user has a registered face image
                    if not user.face_image:
                        messages.error(request, 'No face image registered for this user. Please use password login.')
                        return render(request, 'login.html')

                    # Load the stored face image
                    stored_img = cv2.imread(user.face_image.path)
                    stored_gray = cv2.cvtColor(stored_img, cv2.COLOR_BGR2GRAY)

                    # Detect faces in the stored image
                    stored_faces = face_cascade.detectMultiScale(stored_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    if len(stored_faces) == 0:
                        messages.error(request, 'Error with stored face image. Please use password login.')
                        return render(request, 'login.html')

                    # Extract the first face from stored image
                    (sx, sy, sw, sh) = stored_faces[0]
                    stored_face = stored_gray[sy:sy+sh, sx:sx+sw]
                    stored_face_resized = cv2.resize(stored_face, (128, 128))

                    # Compute similarity between live and stored faces
                    similarity = cv2.matchTemplate(live_face_resized, stored_face_resized, cv2.TM_CCOEFF_NORMED)[0][0]

                    if similarity > 0.3:  # Adjust threshold based on your needs
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        messages.success(request, 'Face login successful!')
                        return redirect('user_index')  # Redirect to user homepage after successful login
                    else:
                        messages.error(request, f'Face verification failed. Similarity: {similarity}. Please try again or use password login.')
                        return render(request, 'login.html')

                except Exception as e:
                    print(f"Face detection error: {str(e)}")
                    messages.error(request, 'Face detection failed. Please try again or use password login.')
                    return render(request, 'login.html')

            else:  # If no face image, authenticate with password
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('adminindex')
                    elif user.role == 3:
                        return redirect('labtechindex')
                    elif user.role == 2:
                        return redirect('labindex')
                    else:
                        return redirect('user_index')
                else:
                    messages.error(request, 'Invalid email or password')

        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')

        except Exception as e:
            print(f"Login error: {str(e)}")
            messages.error(request, 'Login failed')

    return render(request, 'login.html')





def register_view(request):
    if request.method == 'POST':
        try:
            # Get form data
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            phone = request.POST.get('phone')
            role = request.POST.get('role', 0)
            face_image = request.POST.get('face_image')

            # Create user
            user = User(
                first_name=fname,
                last_name=lname,
                username=email,
                email=email,
                password=make_password(password),
                gender=gender,
                dob=dob,
                phone=phone,
                role=role
            )

            # Process face image if provided
            if face_image and face_image.startswith('data:image'):
                format, imgstr = face_image.split(';base64,')
                image_data = base64.b64decode(imgstr)
                
                # Save the image
                user.face_image.save(f'face_{email}.jpg', ContentFile(image_data), save=False)

            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')

        except Exception as e:
            print(f"Registration error: {str(e)}")
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register.html')

@never_cache
@login_required
def user_index(request):
    return render(request, 'user/userindex.html')

@never_cache
@login_required
def lab_index(request):
    return render(request, 'lab/labindex.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification
@never_cache
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
@never_cache
@login_required
def medicalhistory_view(request):
    return render(request, 'user/medicalhistory.html')
@never_cache
@login_required
def adminindex_view(request):
    return render(request, 'admins/adminindex.html') 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import User
@never_cache
@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can access this view
def user_list_view(request):
    # Filter users with role=0 and is_staff=False
    users = User.objects.filter(role=0, is_staff=False)
    return render(request, 'admins/user_list.html', {'users': users})
@never_cache
@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {'activated' if user.is_active else 'deactivated'} successfully.")
    return redirect('user_list')
@never_cache
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('user_list')
@never_cache
@login_required
def bloodtest_view(request):
    return render(request, 'user/blood.html')
@never_cache
@login_required
def urinetest_view(request):
    return render(request, 'user/urine.html')
@never_cache
@login_required
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
@never_cache
@login_required
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
@never_cache
@login_required
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
import string
import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)

# ✅ Password generator function without 'request'
def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.SystemRandom().choice(characters) for _ in range(length))

@never_cache
@login_required
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

        # ✅ Generate a secure random password
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

        # ✅ Send autogenerated password via email
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

@never_cache
@login_required
def profile_view(request):
    return render(request, 'user/profile_view.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@never_cache
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
@never_cache
@login_required
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

@never_cache
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

@never_cache
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
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LabTechnician

@never_cache
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
@never_cache
@login_required
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
@never_cache
@login_required
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
@never_cache
@login_required
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
@never_cache
@login_required
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
@never_cache
@login_required
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
@never_cache
@login_required
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

@never_cache
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
@never_cache
@login_required
def booking_list_view(request):
    bookings = Booking.objects.all()
    return render(request, 'lab/booking_detail.html', {'bookings': bookings})
from django.shortcuts import render, get_object_or_404
from .models import Booking, Payment  # Ensure Payment is imported

# myproject/myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import Booking, Payment, CollectionStatus  # Ensure CollectionStatus is imported
@never_cache
@login_required
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

@never_cache
@login_required
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
@never_cache
@login_required
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

from django.shortcuts import render, get_object_or_404
from .models import LabTechnicianSchedule, CollectionStatus, LabTechnician, Booking, Notification  # Ensure all models are imported

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import LabTechnicianSchedule, CollectionStatus, LabTechnician, Booking, Notification

# @never_cache
# @login_required
# def view_scheduled_requests(request):
#     technician = get_object_or_404(LabTechnician, user=request.user)
#     scheduled_requests = LabTechnicianSchedule.objects.filter(technician=technician)

#     detailed_requests = []
#     for schedule in scheduled_requests:
#         booking = schedule.booking
#         test_types = booking.test_types.all()

#         test_type_names = ", ".join([test_type.tests_names for test_type in test_types]) if test_types else "No test types available"

#         # Get or create the collection status
#         collection_status, created = CollectionStatus.objects.get_or_create(booking=booking)

#         # Determine type of booking and fetch location if it's home collection
#         if booking.home_collection and booking.home_collection.location:
#             type_of_booking = 'Home Collection'
#             location = booking.home_collection.location  # Fetch location from home_collection table
#         else:
#             type_of_booking = 'Lab Visit'
#             location = None  # No location for Lab Visit

#         detailed_requests.append({
#             'appointment_date': booking.appointment_date,
#             'appointment_time': booking.appointment_time,
#             'user_name': f"{booking.user.first_name} {booking.user.last_name}",
#             'test_types': test_type_names,
#             'booking_id': booking.id,
#             'is_collected': collection_status.is_collected,  # Collection status
#             'technician_id': collection_status.technician.labtech_id if collection_status.technician else None,
#             'type_of_booking': type_of_booking,  # Booking type
#             'location': location,  # Store location for home collection
#         })

#     # Calculate the count of unread notifications for the current lab technician
#     unviewed_count = Notification.objects.filter(is_read=False, lab_technician=technician).count()

#     return render(request, 'labtech/view_scheduled_request.html', {
#         'scheduled_requests': detailed_requests,
#         'unviewed_count': unviewed_count,
#     })

 # Redirect back to the scheduled requests view  # Ensure you have the correct imports
# myproject/myapp/views.py
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import LabTechnician, LabTechnicianSchedule, CollectionStatus, Notification

@never_cache
@login_required
def view_scheduled_requests(request):
    technician = get_object_or_404(LabTechnician, user=request.user)
    scheduled_requests = LabTechnicianSchedule.objects.filter(technician=technician)

    # Get search and sort parameters from the request
    search_booking_id = request.GET.get('search_booking_id', '').strip()
    sort_by = request.GET.get('sort_by', '')

    detailed_requests = []
    for schedule in scheduled_requests:
        booking = schedule.booking
        test_types = booking.test_types.all()
        test_type_names = ", ".join([test_type.tests_names for test_type in test_types]) if test_types else "No test types available"

        # Collection status
        collection_status, _ = CollectionStatus.objects.get_or_create(booking=booking)

        # Booking type and location
        if booking.home_collection and booking.home_collection.location:
            type_of_booking = 'Home Collection'
            location = booking.home_collection.location
        else:
            type_of_booking = 'Lab Visit'
            location = None

        detailed_requests.append({
            'appointment_date': booking.appointment_date,
            'appointment_time': booking.appointment_time,
            'user_name': f"{booking.user.first_name} {booking.user.last_name}",
            'test_types': test_type_names,
            'booking_id': booking.id,
            'status': booking.status,
            'is_collected': collection_status.is_collected,
            'technician_id': collection_status.technician.labtech_id if collection_status.technician else None,
            'type_of_booking': type_of_booking,
            'location': location,
        })

    # Apply search filter
    if search_booking_id:
        detailed_requests = [req for req in detailed_requests if search_booking_id.lower() in str(req['booking_id']).lower()]

    # Apply sorting
    if sort_by == 'asc':
        detailed_requests.sort(key=lambda x: x['appointment_date'])
    elif sort_by == 'desc':
        detailed_requests.sort(key=lambda x: x['appointment_date'], reverse=True)

    # Unread notifications
    unviewed_count = Notification.objects.filter(is_read=False, lab_technician=technician).count()

    return render(request, 'labtech/view_scheduled_request.html', {
        'scheduled_requests': detailed_requests,
        'unviewed_count': unviewed_count,
        'request': request  # So we can access GET params in the template
    })


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
from .models import LabTechnician, LabTechnicianSchedule, Booking
from django.utils import timezone
from django.db.models import Max

@never_cache
@login_required
def unscheduled_lab_technicians(request):
    # Get today's date
    today = timezone.now().date()

    # Get all bookings that are scheduled before today
    past_bookings = Booking.objects.filter(appointment_date__lt=today)

    # Get the technicians associated with those bookings
    technicians_with_past_bookings = LabTechnicianSchedule.objects.filter(booking__in=past_bookings).values_list('technician', flat=True)

    # Retrieve the technician objects with past bookings
    technicians_with_past = LabTechnician.objects.filter(labtech_id__in=technicians_with_past_bookings)

    # Get the last appointment date for each technician with past bookings
    last_appointment_dates = LabTechnicianSchedule.objects.filter(technician__in=technicians_with_past).annotate(last_appointment=Max('booking__appointment_date'))

    # Create a dictionary to map technician IDs to their last appointment dates
    last_appointment_dict = {tech.technician.labtech_id: tech.last_appointment for tech in last_appointment_dates}

    # Get all lab technicians
    all_technicians = LabTechnician.objects.all()

    # Get scheduled technicians
    scheduled_technicians = LabTechnicianSchedule.objects.values_list('technician', flat=True)

    # Filter out scheduled technicians to find unscheduled ones
    unscheduled_technicians = all_technicians.exclude(labtech_id__in=scheduled_technicians)

    # Combine both lists
    combined_technicians = []
    for technician in technicians_with_past:
        combined_technicians.append({
            'technician': technician,
            'last_appointment': last_appointment_dict.get(technician.labtech_id, None)  # Use labtech_id
        })

    for technician in unscheduled_technicians:
        combined_technicians.append({
            'technician': technician,
            'last_appointment': None  # No appointment date for unscheduled technicians
        })

    return render(request, 'lab/unscheduled_lab_technicians.html', {
        'technicians': combined_technicians,
        'today': today,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Booking  # Ensure you have the correct import
@never_cache
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
@login_required
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
@never_cache
@login_required
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
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from .models import Booking, CollectionStatus, TestResult, TestValue, LabTechnician, TestType,Amount

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

from .models import Booking, CollectionStatus, TestResult, TestType, Amount

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
from .models import Booking, CollectionStatus, TestResult, TestType, Amount

def download_test_report_by_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    collection_status = get_object_or_404(CollectionStatus, booking=booking)
    lab_technician = collection_status.technician

    testing_date = "2023-01-15"
    collection_date = "2023-01-20"
    doctor_name = "Dr. John Doe"
    report_done_by = "Lab Technician: Jane Smith"
    report_id = f"{booking.id:03d}/medlab"

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=36)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='TitleStyle', fontSize=24, fontName='Helvetica-Bold', alignment=1, textColor=colors.darkblue, spaceAfter=14)
    subtitle_style = ParagraphStyle(name='SubtitleStyle', fontSize=12, fontName='Helvetica-Bold', alignment=1, spaceAfter=8)
    header_style = styles['Heading2']
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14
    bold_style = ParagraphStyle(name='BoldStyle', fontName='Helvetica-Bold', fontSize=11)

    elements = []

    # Report Header
    elements.append(Paragraph("MedLab Diagnostic Center", title_style))
    elements.append(Paragraph("123 Health Street, City, Country", subtitle_style))
    elements.append(Paragraph("Phone: +1 234 567 890 | Email: contact@medlab.com", subtitle_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"<b>Test Report ID:</b> {report_id}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Patient & Booking Info
    elements.append(Paragraph(f"<b>Patient:</b> {booking.user.first_name} {booking.user.last_name}", normal_style))
    elements.append(Paragraph(f"<b>Date of Appointment:</b> {booking.appointment_date}", normal_style))
    elements.append(Paragraph(f"<b>Testing Date:</b> {testing_date}", normal_style))
    elements.append(Paragraph(f"<b>Collection Date:</b> {collection_date}", normal_style))
    elements.append(Paragraph(f"<b>Doctor:</b> {doctor_name}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Technician Info
    elements.append(Paragraph("<b>Test Conducted By:</b>", header_style))
    elements.append(Paragraph(f"{lab_technician.user.first_name} {lab_technician.user.last_name}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("<b>Report Done By:</b>", header_style))
    elements.append(Paragraph(report_done_by, normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Test Results Table
    table_data = [
        [Paragraph("<b>Test Name</b>", bold_style), Paragraph("<b>Result</b>", bold_style), Paragraph("<b>Normal Range</b>", bold_style)]
    ]

    test_results = TestResult.objects.filter(collection_status=collection_status).prefetch_related('values', 'test_types')
    total_amount = 0

    for result in test_results:
        test_types = result.test_types.all()
        result_values = result.values.all()

        for test_type, value in zip(test_types, result_values):
            normal_range = get_object_or_404(TestType, testtype_id=test_type.testtype_id).normal_range
            split_values = value.result_value.split(",")

            try:
                amount_obj = Amount.objects.get(test_type=test_type)
                price = amount_obj.amount
            except Amount.DoesNotExist:
                price = 0

            for single_value in split_values:
                table_data.append([
                    Paragraph(test_type.tests_names, normal_style),
                    Paragraph(single_value.strip(), normal_style),
                    Paragraph(normal_range, normal_style)
                ])
                total_amount += float(price)

    # Total Row
    table_data.append([
        "",
        Paragraph("<b>Total Amount:</b>", bold_style),
        Paragraph(f"<b>INR {total_amount:.2f}</b>", bold_style)
    ])

    # Build Table
    table = Table(table_data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("<b>Thank you for choosing MedLab!</b>", normal_style))
    elements.append(Paragraph("For any inquiries, please contact us at: contact@medlab.com or +1 234 567 890.", normal_style))

    pdf.build(elements)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="test_report_booking_{report_id}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TestName, TestType, Booking
from datetime import datetime


from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import TestName, TestType, Booking, HomeCollection

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import make_aware
from .models import HomeCollection, Booking, TestName, TestType
from datetime import datetime

from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Booking, TestName, TestType, HomeCollection

@never_cache
@login_required
def home_collection(request):
    if request.method == 'POST':
        test_name_id = request.POST.get('name_id')
        selected_test_types = request.POST.getlist('selected_test_types')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        location = request.POST.get('location', '').strip()  # Ensure location is a valid string

        print(f"Received location: {location}")  # Debugging

        # Validate input
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
            return render(request, 'user/home_collection.html', {
                'test_names': TestName.objects.all(),
                'tests': TestType.objects.all(),
                'error': 'Please correct the following errors.'
            })

        # Process TestName
        try:
            test_name = TestName.objects.get(pk=test_name_id)
        except TestName.DoesNotExist:
            messages.error(request, 'Test Name not found.')
            return redirect('home_collection')

        # Convert date and time
        try:
            appointment_datetime = datetime.combine(
                datetime.strptime(appointment_date, '%Y-%m-%d').date(),
                datetime.strptime(appointment_time, '%I:%M %p').time()  # Fix: 12-hour format with AM/PM
            )
            appointment_datetime = make_aware(appointment_datetime)  # Convert to timezone-aware datetime
        except ValueError as e:
            messages.error(request, f"Invalid date or time format: {str(e)}")
            return redirect('home_collection')

        # Check for existing booking at the same time
        if Booking.objects.filter(
            appointment_date=appointment_datetime.date(),
            appointment_time=appointment_datetime.time()
        ).exists():
            messages.error(request, 'This time slot is already booked.')
            return render(request, 'user/home_collection.html', {
                'test_names': TestName.objects.all(),
                'tests': TestType.objects.all(),
                'error': 'The selected time slot is unavailable.'
            })

        # Ensure HomeCollection entry is created if location is provided
        home_collection_entry = None
        if location:
            home_collection_entry, created = HomeCollection.objects.get_or_create(location=location)
            print(f"HomeCollection Created: {created}, ID: {home_collection_entry.id}")  # Debugging

        # Create Booking instance and assign HomeCollection
        booking = Booking(
            user=request.user,
            appointment_date=appointment_datetime.date(),
            appointment_time=appointment_datetime.time(),
            status='pending',
            test=test_name,
            home_collection=home_collection_entry  # Ensure this is assigned correctly
        )
        booking.save()

        # Assign TestTypes
        valid_test_types = TestType.objects.filter(testtype_id__in=selected_test_types)
        booking.test_types.set(valid_test_types)

        messages.success(request, 'Appointment booked successfully.')
        return redirect('payment', booking_id=booking.id)

    else:
        context = {
            'test_names': TestName.objects.all(),
            'tests': TestType.objects.all(),
        }
        return render(request, 'user/home_collection.html', context)
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, redirect
from .models import Booking, CollectionStatus, LabTechnician

@never_cache
@login_required
def mark_test_done(request, booking_id):
    # Get the booking object
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Update status to "Test Done"
    booking.status = "test done"
    booking.save()
    
    return redirect('view_scheduled_requests')  # Redirect back to the scheduled requests view

