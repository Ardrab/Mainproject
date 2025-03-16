from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('user/userindex/', views.user_index, name='user_index'),
    path('logout/', views.logout_view, name='logout'),
    path('user/medicalhistory/', views.medicalhistory_view, name='medicalhistory'),
    path('user/blood/', views.bloodtest_view, name='blood'),
    path('user/urine/', views.urinetest_view, name='urine'),
    path('user/swab/', views.swabtest_view, name='swab'),
    path('admins/addlab/', views.addlab_view, name='addlab'),
    path('user/profile/', views.profile_view, name='profile'),
    path('user/profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('admins/adminindex/', views.adminindex_view, name='adminindex'),
    path('admins/user_list', views.user_list_view, name='user_list'),
    path('lab/labindex/', views.lab_index, name='labindex'),
    path('lab/addlabtech/', views.addlabtech_view, name='addlabtech'),
    path('labtech/labtechindex/', views.labtechindex, name='labtechindex'),
    path('labtech/labtechprofile/', views.labtechprofile_view, name='labtechprofile'),
    path('lab/labprofile/', views.labprofile_view, name='labprofile'),
    path('labtechs/', views.labtech_list_view, name='labtech_list'),
    path('lab/addtest/', views.addtest_view, name='addtest'),
    path('lab/addtestname/', views.addtestname_view, name='addtestname'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('lab/addtesttypes/', views.add_test_types, name='addtesttypes'),

    # URL for password reset done page
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),

    # URL for password reset confirm page
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # URL for password reset complete page
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    
   
    path('add_test_type/', views.add_test_type_view, name='add_test_type_view'),
    path('get_test_types_by_name/<int:name_id>/', views.get_test_types_by_name, name='get_test_types_by_name'),
    path('get_tests_by_type/<int:test_id>/', views.get_tests_by_type, name='get_tests_by_type'),
    path('add_test_type/submit/', views.add_test_type, name='add_test_type'),
    path('bookings/', views.booking_list_view, name='booking_list_view'),
     path('update_booking_status/<int:booking_id>/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
    path('view_booking_details/<int:booking_id>/', views.view_booking_details, name='view_booking_details'),
     path('user/<int:user_id>/', views.user_details_view, name='user_details'),
        path('payment/<int:booking_id>/', views.payment_view, name='payment'),  # Payment initiation
     path('verify_payment/', views.verify_payment, name='verify_payment'),
       path('process_payment/<int:booking_id>/', views.process_payment, name='process_payment'), 
       path('labtech/profile/', views.labtech_view, name='labtech_profile'),# URL for processing payment
path('labtech/schedule/<int:booking_id>/', views.schedule_lab_technician_view, name='schedule_lab_technician'),
    path('get-technicians/', views.get_technicians, name='get_technicians'),
    path('labtech/scheduled_requests/', views.view_scheduled_requests, name='view_scheduled_requests'),# Add this line
    path('labtech/notifications/', views.view_notifications, name='view_notifications'),
    path('unscheduled-lab-technicians/', views.unscheduled_lab_technicians, name='unscheduled_lab_technicians'),
    path('user-bookings/', views.user_bookings, name='user_bookings'), 
     path('toggle-collection-status/<int:booking_id>/', views.toggle_collection_status, name='toggle_collection_status'),
     path('booking/<int:booking_id>/add-test-result/', views.create_test_result, name='create_test_result'), 
    path('view-test-results/<int:booking_id>/', views.view_test_results, name='view_test_results'), 
    path('booking/<int:booking_id>/download-test-report/', views.download_test_report_by_booking, name='download_test_report_by_booking'), 
    path('generate_bill/<int:booking_id>/', views.generate_bill, name='generate_bill'),# New URL pattern
      # Updated to include booking_id# URL for viewing user bookings
     path('user/home_collection/', views.home_collection, name='home_collection'),
     path('mark-test-done/<int:booking_id>/', views.mark_test_done, name='mark_test_done'),
]
    


if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

     



