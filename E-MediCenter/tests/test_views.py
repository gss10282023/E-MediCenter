from django.test import TestCase, Client, RequestFactory
from EMediCenter import views
from EMediCenter.views import *
from datetime import datetime, timedelta
from EMediCenter.models import *
from django.utils import timezone
import unittest
import json
from unittest import mock
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser,User
from django.contrib.sessions.middleware import SessionMiddleware
from EMediCenter.models import GP, UserProfile, Caregiver, CaregiverOrder, GP, GPOrder
from django.contrib.messages import get_messages
import datetime


# class CaregiverAvailabilityTest(TestCase):
#     def setUp(self):
#         # Create a Caregiver instance
#         self.caregiver = Caregiver.objects.create(
#             Name="Sample Caregiver",
#             Gender="Male",
#             ServiceArea="Area1"
#         )
        
#         self.caregiver2 = Caregiver.objects.create(
#             Name="Sample Caregiver2",
#             Gender="Male",
#             ServiceArea="Area1"
#         )  
        
#         # create a user instance
#         user = User.objects.create_user(
#             username='john_doe', 
#             password='john_password',
#             email='john@example.com',
#             first_name='John',
#             last_name='Doe'
#         )

#         # Use the created Caregiver instance for CaregiverOrder
#         self.caregiver_id = self.caregiver.CaregiverID
#         self.caregiver2_id = self.caregiver2.CaregiverID
#         self.sample_start_time = timezone.make_aware(datetime(2023, 11, 1, 10, 0))  
#         self.sample_end_time = self.sample_start_time + timedelta(hours=2)
        
#         # no overlap 
#         CaregiverOrder.objects.create(
#             CaregiverID=self.caregiver,  # Updated this line
#             start_time=self.sample_start_time - timedelta(hours=4), #6:00
#             end_time=self.sample_start_time - timedelta(hours=2),#8:00
#             Cost=100,
#             UserID=user
#         )
                
#         # overlap
#         CaregiverOrder.objects.create(
#             CaregiverID=self.caregiver,  # Updated this line
#             start_time=self.sample_start_time + timedelta(minutes=30), #10:30
#             end_time=self.sample_end_time + timedelta(minutes=30), #12:30
#             Cost=100,
#             UserID=user
#         )
                
#         # Create a CaregiverOrder for a different caregiver
#         CaregiverOrder.objects.create(
#             CaregiverID=self.caregiver,  
#             start_time=self.sample_start_time, #8:00
#             end_time=self.sample_end_time, #10:00
#             Cost=100,
#             UserID=user
#         )

    
#     # available    
#     def test_caregiver_available(self):
#         is_available = is_caregiver_available(self.caregiver_id, self.sample_start_time - timedelta(hours=1), self.sample_start_time)
#         self.assertTrue(is_available, "The caregiver should be available")

#     # not available
#     def test_caregiver_not_available(self):
#         is_available = is_caregiver_available(self.caregiver_id, self.sample_start_time + timedelta(minutes=30), self.sample_end_time)
#         self.assertFalse(is_available, "The caregiver should not be available")
    
#     # available  
#     def test_caregiver_available_for_different_caregiver(self):
#         is_available = is_caregiver_available(self.caregiver2_id, self.sample_start_time, self.sample_end_time)
#         self.assertTrue(is_available, "The caregiver should be available")



# class TestIsValidAddress(unittest.TestCase):

#     @patch('requests.get')
#     def test_valid_address(self, mock_get):
#         # successful API response
#         mock_get.return_value.json.return_value = {
#             'status': 'OK',
#             'results': [{'formatted_address': 'Sample Address'}]
#         }
#         self.assertTrue(is_valid_address("a real St", "api_key"))

#     @patch('requests.get')
#     def test_invalid_address(self, mock_get):
#         # failed API response
#         mock_get.return_value.json.return_value = {
#             'status': 'ZERO_RESULTS',
#             'results': []
#         }
#         self.assertFalse(is_valid_address("Invalid Address", "api_key"))

#     @patch('requests.get')
#     def test_api_error(self, mock_get):
#         # Mock an error API response
#         mock_get.return_value.json.return_value = {
#             'status': 'ERROR',
#             'results': []
#         }
#         self.assertFalse(is_valid_address("a real St", "api_key"))



# class TestGetPlaceDetails(unittest.TestCase):

#     @patch('requests.get')
#     def test_get_place_details_successful(self, mock_get):
#         # successful API response
#         mock_response = {
#             'status': 'OK',
#             'address_components': [{'long_name': 'Sydney', 'short_name': 'SYD', 'types': ['locality', 'political']}]
#         }
#         mock_get.return_value.json.return_value = mock_response

#         result = get_place_details("valid_id", "api_key")
#         self.assertEqual(result, mock_response)

#     @patch('requests.get')
#     def test_get_place_details_failed(self, mock_get):
#         # failed API response
#         mock_response = {
#             'status': 'INVALID_REQUEST',
#         }
#         mock_get.return_value.json.return_value = mock_response

#         result = get_place_details("invalid_id", "api_key")
#         self.assertEqual(result, mock_response)

#     @patch('requests.get')
#     def test_get_place_details_error(self, mock_get):
#         # Mock an error from the requests module (e.g., timeout or connection error)
#         mock_get.side_effect = requests.RequestException("Error message")

#         with self.assertRaises(requests.RequestException):
#             get_place_details("valid_id", "api_key")


# class RenderingTest(TestCase):

#     def test_home_page(self):
#         response = self.client.get(reverse('HomePage'))  #
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'index.html')
        
#     def test_about_us_page(self):
#         response = self.client.get(reverse('AboutusPage'))  
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'AboutusPage.html')

#     def test_donation_page(self):
#         response = self.client.get(reverse('Donation'))  
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'DonationPage.html')
        
#     def test_caregiver_dashboard(self):
#         response = self.client.get(reverse('Caregiver'))  
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'caregiver_profile.html')

#     def test_admin_dashboard(self):
#         response = self.client.get(reverse('admin'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'Dashboard_Admin.html')

#     def test_customer_dashboard(self):
#         response = self.client.get(reverse('customer'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'customer_profile.html')

#     def test_customer_order(self):
#         response = self.client.get(reverse('customer_order'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'customer_order.html')

#     def test_doctor_dashboard(self):
#         response = self.client.get(reverse('doctor'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'doctor_profile.html')

#     def test_doctor_order(self):
#         response = self.client.get(reverse('doctor_order'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'doctor_order.html')


# class BookGPTest(TestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpass')
    
#     # unauthenticated user, go to login page
#     def test_unauthenticated_access(self):
#         response = self.client.get('/book_GP/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html') 
        
#     def test_GET_request(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/book_GP/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'BookGPPage.html')
    
#     # has matching GP
#     @mock.patch('EMediCenter.views.googlemaps.Client.distance_matrix')
#     def test_matching_GPs(self, mocked_distance_matrix):
#         data = {
#             'distance': '10',
#             'street': 'Sample Street',
#             'suburb': 'Sample Suburb',
#             'state': 'Sample State',
#             'postcode': '12345',
#             'cost': '50',
#             'date': '2022-01-01'
#         }
#         self.client.force_login(self.user)
#         mocked_distance_matrix.return_value = {
#             "status": "OK",
#             "rows": [{
#                 "elements": [{
#                     "status": "OK",
#                     "distance": {"value": 5000}
#                 }]
#             }]
#         }
#         response = self.client.post('/book_GP/', data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'selectGP.html')
    
#     # no matching GP
#     @mock.patch('EMediCenter.views.googlemaps.Client.distance_matrix')
#     def test_no_matching_GPs(self, mocked_distance_matrix):
#         data = {
#             'distance': '0',
#             'street': 'Sample Street',
#             'suburb': 'Sample Suburb',
#             'state': 'Sample State',
#             'postcode': '12345',
#             'cost': '0',
#             'date': '2022-01-01'
#         }
#         self.client.force_login(self.user)
#         mocked_distance_matrix.return_value = {
#             "status": "OK",
#             "rows": [{
#                 "elements": [{
#                     "status": "OK",
#                     "distance": {"value": 40000}
#                 }]
#             }]
#         }
#         response = self.client.post('/book_GP/', data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'selectGP.html')
    
#     # test session storage
#     @mock.patch('EMediCenter.views.googlemaps.Client.distance_matrix')
#     def test_session_storage(self, mocked_distance_matrix):
#         data = {
#             'distance': '10',
#             'street': 'Sample Street',
#             'suburb': 'Sample Suburb',
#             'state': 'Sample State',
#             'postcode': '12345',
#             'cost': '50',
#             'date': '2022-01-01'
#         }
#         self.client.force_login(self.user)
#         response = self.client.post('/book_GP/', data)
#         self.assertEqual(response.status_code, 200)
#         session = self.client.session
#         self.assertIn('GPs_matched_ids', session)

# class BookCaregiverTest(TestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpass')
    
#     # Unauthenticated user, go to login page
#     def test_unauthenticated_access(self):
#         response = self.client.get('/book_caregiver/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html') 
        
#     def test_GET_request(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/book_caregiver/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'BookCaregiverPage.html')
    
#     # Has matching caregiver
#     @mock.patch('EMediCenter.views.googlemaps.Client.distance_matrix')
#     def test_matching_caregivers(self, mocked_distance_matrix):
#         data = {
#             'distance': '10',
#             'street': 'Sample Street',
#             'suburb': 'Sample Suburb',
#             'state': 'Sample State',
#             'postcode': '12345',
#             'cost': '50',
#             'date': '2022-01-01'
#         }
#         self.client.force_login(self.user)
#         mocked_distance_matrix.return_value = {
#             "status": "OK",
#             "rows": [{
#                 "elements": [{
#                     "status": "OK",
#                     "distance": {"value": 5000}
#                 }]
#             }]
#         }
#         response = self.client.post('/book_caregiver/', data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'select.html')
    
#     # No matching caregiver
#     @mock.patch('EMediCenter.views.googlemaps.Client.distance_matrix')
#     def test_no_matching_caregivers(self, mocked_distance_matrix):
#         data = {
#             'distance': '0',
#             'street': 'Sample Street',
#             'suburb': 'Sample Suburb',
#             'state': 'Sample State',
#             'postcode': '12345',
#             'cost': '0',
#             'date': '2022-01-01'
#         }
#         self.client.force_login(self.user)
#         mocked_distance_matrix.return_value = {
#             "status": "OK",
#             "rows": [{
#                 "elements": [{
#                     "status": "OK",
#                     "distance": {"value": 40000}
#                 }]
#             }]
#         }
#         response = self.client.post('/book_caregiver/', data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'select.html')
    
#     # Test session storage
#     @mock.patch('EMediCenter.views.googlemaps.Client.distance_matrix')
#     def test_session_storage(self, mocked_distance_matrix):
#         data = {
#             'distance': '10',
#             'street': 'Sample Street',
#             'suburb': 'Sample Suburb',
#             'state': 'Sample State',
#             'postcode': '12345',
#             'cost': '50',
#             'date': '2022-01-01'
#         }
#         self.client.force_login(self.user)
#         response = self.client.post('/book_caregiver/', data)
#         self.assertEqual(response.status_code, 200)
#         session = self.client.session
#         self.assertIn('caregivers_matched_ids', session)


# class TestIsValidEmail(unittest.TestCase):
    
#     def test_valid_emails(self):
#         valid_emails = [
#             "test@example.com",
#             "test.a@example.com",
#             "test_a@example.co.au",
#             "test.a+123@example.com"
#         ]
#         for email in valid_emails:
#             with self.subTest(email=email):
#                 self.assertTrue(is_valid_email(email), f"{email} should be valid!")

#     def test_invalid_emails(self):
#         invalid_emails = [
#             "test@example",
#             "test.example.com",
#             "@example.com",
#             "test@.com",
#             "test@.com.",
#             "test@com",
#             "test@.com.au.",
#             "test user@example.com",
#             "test@user@example.com"
#         ]
#         for email in invalid_emails:
#             with self.subTest(email=email):
#                 self.assertFalse(is_valid_email(email), f"{email} should be invalid")

#     def test_edge_cases(self):
#         edge_cases = [
#             "", # empty string
#             None, # None value
#             "   ", # spaces only
#             "test@ex ample.com", # space within domain
#             " test@example.com", # space at the beginning
#             "test@example.com " # space at the end
#         ]
#         for email in edge_cases:
#             with self.subTest(email=email):
#                 self.assertFalse(is_valid_email(email), f"{email} should be invalid")




# class LoginViewTestCase(TestCase):
    
#     @staticmethod
#     def add_session_to_request(request):
#         middleware = SessionMiddleware()
#         middleware.process_request(request)
#         request.session.save()
#         return request
    # def add_session_to_request(self, request):
    #     middleware = SessionMiddleware(lambda req: None)  # 这里我们提供了一个lambda函数作为get_response
    #     middleware.process_request(request)
    #     request.session.save()
    #     return request

    
#     def setUp(self):
#         self.factory = RequestFactory()
#         # Create a user and profile
#         self.user = User.objects.create_user(username='test_user', password='test_password')
#         self.profile = UserProfile.objects.create(user=self.user)  

#     def test_non_existing_user(self):
#         request = self.factory.post('/login/', {'Username': 'non_existing_user', 'password': 'some_password'})
#         request = self.add_session_to_request(request)
#         response = login_view(request)

#         self.assertEqual(response.status_code, 200)  # render the login page again
#         self.assertIn("User doesn&#x27;t exist.", response.content.decode())

#     def test_wrong_password(self):
#         request = self.factory.post('/login/', {'Username': 'test_user', 'password': 'wrong_password'})
#         request = self.add_session_to_request(request)
#         response = login_view(request)

#         self.assertEqual(response.status_code, 200)  # render the login page again
#         self.assertIn("Incorrect password.", response.content.decode())

#     def test_inactive_user(self):
#         # Make the user inactive
#         self.user.is_active = False
#         self.user.save()

#         request = self.factory.post('/login/', {'Username': 'test_user', 'password': 'test_password'})
#         request = self.add_session_to_request(request)
#         response = login_view(request)
#         self.assertEqual(response.status_code, 200)  # render the login page again
#         self.assertIn("Your account is inactive.", response.content.decode()) # check error msg



#     def test_login_successful(self):
        
#         test_cases = [
#             {"is_staff": True, "is_doctor": False, "is_caregiver": False, "expected_url": "/admin_dashboard/"},
#             {"is_staff": False, "is_doctor": True, "is_caregiver": False, "expected_url": "/doctor_dashboard/"},
#             {"is_staff": False, "is_doctor": False, "is_caregiver": True, "expected_url": "/caregiver_dashboard/"},
#             {"is_staff": False, "is_doctor": False, "is_caregiver": False, "expected_url": "/user_dashboard/"}
#         ]

#         for test_case in test_cases:
#             with self.subTest(**test_case):
#                 # Setting the user profile attributes
#                 self.user.is_staff = test_case["is_staff"]
#                 self.user.save()
#                 self.profile.is_doctor = test_case["is_doctor"]
#                 self.profile.is_caregiver = test_case["is_caregiver"]
#                 self.profile.save()

#                 request = self.factory.post('/login/', {'Username': 'test_user', 'password': 'test_password'})
#                 request = self.add_session_to_request(request)
#                 request.user = self.user
#                 response = login_view(request)

#                 # Redirect
#                 self.assertEqual(response.status_code, 302)
#                 self.assertEqual(response.url, test_case["expected_url"])



# class AddDoctorTestCase(TestCase):
    
#     def setUp(self):
#         self.factory = RequestFactory()
# class DoctorProfileTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username="testdoctor", password="testpassword", 
#                                              first_name="Doctor", last_name="Test", email="test@example.com")
#         UserProfile.objects.create(user=self.user, address="123 Test Street, TestSuburb, TestState, 12345")
#         GP.objects.create(Name="testdoctor", Cost=100)  
        
#         self.client = Client()

#     def test_get_doctor(self):
#         self.client.login(username="testdoctor", password="testpassword")
#         response = self.client.get(reverse('Get_doctor'))
        
#         context_data = response.context[0] if isinstance(response.context, list) else response.context

#         self.assertIn('first_name', context_data)
#         self.assertEqual(context_data['first_name'], "Doctor")
        
#         self.assertIn('last_name', context_data)
#         self.assertEqual(context_data['last_name'], "Test")
        
#         self.assertIn('email', context_data)
#         self.assertEqual(context_data['email'], "test@example.com")
        
#         self.assertIn('street', context_data)
#         self.assertEqual(context_data['street'], "123 Test Street")
        
#         self.assertIn('suburb', context_data)
#         self.assertEqual(context_data['suburb'], "TestSuburb")
        
#         self.assertIn('state', context_data)
#         self.assertEqual(context_data['state'], "TestState")
        
#         self.assertIn('postcode', context_data)
#         self.assertEqual(context_data['postcode'], "12345")
        
#         self.assertTemplateUsed(response, 'doctor_profile.html')

#     def test_user_without_userprofile(self):
#         UserProfile.objects.filter(user=self.user).delete()
#         self.client.login(username="testdoctor", password="testpassword")
#         response = self.client.get(reverse('Get_doctor'))
#         self.assertIsInstance(response, HttpResponseBadRequest)


#     def test_wrong_request_method(self):
#         response = self.client.post(reverse('Get_doctor'))
#         self.assertIsInstance(response, HttpResponseBadRequest) 
    
#     def test_edit_doctor_post(self):
#         self.client.login(username="testdoctor", password="testpassword")

#         post_data = {
#             'fname': 'UpdatedDoctor',
#             'lname': 'UpdatedTest',
#             'email': 'updated@example.com',
#             'street': '456 Updated Street',
#             'suburb': 'UpdatedSuburb',
#             'state': 'UpdatedState',
#             'postcode': '67890',
#             'cost': '200'
#         }

#         response = self.client.post(reverse('Edit_doctor'), data=post_data)

#         updated_user = User.objects.get(username="testdoctor")
#         self.assertEqual(updated_user.first_name, 'UpdatedDoctor')
#         self.assertEqual(updated_user.last_name, 'UpdatedTest')
#         self.assertEqual(updated_user.email, 'updated@example.com')

#         updated_profile = updated_user.userprofile
#         self.assertEqual(updated_profile.address, '456 Updated Street, UpdatedSuburb, UpdatedState, 67890')

#         doctor = GP.objects.get(Name="testdoctor")
#         self.assertEqual(doctor.Cost, 200)

#     def test_edit_doctor_without_cost(self):
#         self.client.login(username="testdoctor", password="testpassword")

#         post_data = {
#             'fname': 'UpdatedDoctor',
#             'lname': 'UpdatedTest',
#             'email': 'updated@example.com',
#             'street': '456 Updated Street',
#             'suburb': 'UpdatedSuburb',
#             'state': 'UpdatedState',
#             'postcode': '67890',
#         }

#         response = self.client.post(reverse('Edit_doctor'), data=post_data)

#         updated_user = User.objects.get(username="testdoctor")
#         self.assertEqual(updated_user.first_name, 'UpdatedDoctor')

#         doctor = GP.objects.get(Name="testdoctor")
#         self.assertEqual(doctor.Cost, 100) 

# class TemplateRenderingTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_success_template(self):
#         response = self.client.get(reverse('success'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'success.html')

#     def test_admin_profile_template(self):
#         response = self.client.get(reverse('admin_profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'Dashboard_Admin_profile.html')

#     def test_caregiver_profile_template(self):
#         response = self.client.get(reverse('caregiver_profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'caregiver_profile.html')

#     def test_caregiver_order_template(self):
#         response = self.client.get(reverse('caregiver_order'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'caregiver_order.html')

#     def test_customer_profile_template(self):
#         response = self.client.get(reverse('customer_profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'customer_profile.html')

#     def test_customer_order_template(self):
#         response = self.client.get(reverse('customer_order'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'customer_order.html')

# class customerProfileTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username="testcustomer", password="testpassword", 
#                                              first_name="customer", last_name="Test", email="test@example.com")
#         UserProfile.objects.create(user=self.user, address="123 Test Street, TestSuburb, TestState, 12345")
        
#         self.client = Client()

#     def test_get_customer(self):
#         self.client.login(username="testcustomer", password="testpassword")
#         response = self.client.get(reverse('Get_customer'))
        
#         context_data = response.context[0] if isinstance(response.context, list) else response.context

#         self.assertIn('first_name', context_data)
#         self.assertEqual(context_data['first_name'], "customer")
        
#         self.assertIn('last_name', context_data)
#         self.assertEqual(context_data['last_name'], "Test")
        
#         self.assertIn('email', context_data)
#         self.assertEqual(context_data['email'], "test@example.com")
        
#         self.assertIn('street', context_data)
#         self.assertEqual(context_data['street'], "123 Test Street")
        
#         self.assertIn('suburb', context_data)
#         self.assertEqual(context_data['suburb'], "TestSuburb")
        
#         self.assertIn('state', context_data)
#         self.assertEqual(context_data['state'], "TestState")
        
#         self.assertIn('postcode', context_data)
#         self.assertEqual(context_data['postcode'], "12345")
        
#         self.assertTemplateUsed(response, 'customer_profile.html')

#     def test_user_without_userprofile(self):
#         UserProfile.objects.filter(user=self.user).delete()
#         self.client.login(username="testcustomer", password="testpassword")
#         response = self.client.get(reverse('Get_customer'))
#         self.assertIsInstance(response, HttpResponseBadRequest)


#     def test_wrong_request_method(self):
#         response = self.client.post(reverse('Get_customer'))
#         self.assertIsInstance(response, HttpResponseBadRequest) 
    
#     def test_edit_customer_post(self):
#         self.client.login(username="testcustomer", password="testpassword")

#         post_data = {
#             'fname': 'Updatedcustomer',
#             'lname': 'UpdatedTest',
#             'email': 'updated@example.com',
#             'street': '456 Updated Street',
#             'suburb': 'UpdatedSuburb',
#             'state': 'UpdatedState',
#             'postcode': '67890',
#         }

#         response = self.client.post(reverse('Edit_customer'), data=post_data)

#         updated_user = User.objects.get(username="testcustomer")
#         self.assertEqual(updated_user.first_name, 'Updatedcustomer')
#         self.assertEqual(updated_user.last_name, 'UpdatedTest')
#         self.assertEqual(updated_user.email, 'updated@example.com')

#         updated_profile = updated_user.userprofile
#         self.assertEqual(updated_profile.address, '456 Updated Street, UpdatedSuburb, UpdatedState, 67890')

#     def test_edit_customer_without_cost(self):
#         self.client.login(username="testcustomer", password="testpassword")

#         post_data = {
#             'fname': 'Updatedcustomer',
#             'lname': 'UpdatedTest',
#             'email': 'updated@example.com',
#             'street': '456 Updated Street',
#             'suburb': 'UpdatedSuburb',
#             'state': 'UpdatedState',
#             'postcode': '67890',
#         }

#         response = self.client.post(reverse('Edit_customer'), data=post_data)

#         updated_user = User.objects.get(username="testcustomer")
#         self.assertEqual(updated_user.first_name, 'Updatedcustomer')

# class caregiverProfileTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username="testcaregiver", password="testpassword", 
#                                              first_name="caregiver", last_name="Test", email="test@example.com")
#         UserProfile.objects.create(user=self.user, address="123 Test Street, TestSuburb, TestState, 12345")
#         Caregiver.objects.create(Name="testcaregiver", Cost=100)  
        
#         self.client = Client()

#     def test_get_caregiver(self):
#         self.client.login(username="testcaregiver", password="testpassword")
#         response = self.client.get(reverse('Get_caregiver'))
        
#         context_data = response.context[0] if isinstance(response.context, list) else response.context

#         self.assertIn('first_name', context_data)
#         self.assertEqual(context_data['first_name'], "caregiver")
        
#         self.assertIn('last_name', context_data)
#         self.assertEqual(context_data['last_name'], "Test")
        
#         self.assertIn('email', context_data)
#         self.assertEqual(context_data['email'], "test@example.com")
        
#         self.assertIn('street', context_data)
#         self.assertEqual(context_data['street'], "123 Test Street")
        
#         self.assertIn('suburb', context_data)
#         self.assertEqual(context_data['suburb'], "TestSuburb")
        
#         self.assertIn('state', context_data)
#         self.assertEqual(context_data['state'], "TestState")
        
#         self.assertIn('postcode', context_data)
#         self.assertEqual(context_data['postcode'], "12345")
        
#         self.assertTemplateUsed(response, 'caregiver_profile.html')

#     def test_user_without_userprofile(self):
#         UserProfile.objects.filter(user=self.user).delete()
#         self.client.login(username="testcaregiver", password="testpassword")
#         response = self.client.get(reverse('Get_caregiver'))
#         self.assertIsInstance(response, HttpResponseBadRequest)


#     def test_wrong_request_method(self):
#         response = self.client.post(reverse('Get_caregiver'))
#         self.assertIsInstance(response, HttpResponseBadRequest) 
    
#     def test_edit_caregiver_post(self):
#         self.client.login(username="testcaregiver", password="testpassword")

#         post_data = {
#             'fname': 'Updatedcaregiver',
#             'lname': 'UpdatedTest',
#             'email': 'updated@example.com',
#             'street': '456 Updated Street',
#             'suburb': 'UpdatedSuburb',
#             'state': 'UpdatedState',
#             'postcode': '67890',
#             'cost': '200'
#         }

#         response = self.client.post(reverse('Edit_caregiver'), data=post_data)

#         updated_user = User.objects.get(username="testcaregiver")
#         self.assertEqual(updated_user.first_name, 'Updatedcaregiver')
#         self.assertEqual(updated_user.last_name, 'UpdatedTest')
#         self.assertEqual(updated_user.email, 'updated@example.com')

#         updated_profile = updated_user.userprofile
#         self.assertEqual(updated_profile.address, '456 Updated Street, UpdatedSuburb, UpdatedState, 67890')

#         caregiver = Caregiver.objects.get(Name="testcaregiver")
#         self.assertEqual(caregiver.Cost, 200)

#     def test_edit_caregiver_without_cost(self):
#         self.client.login(username="testcaregiver", password="testpassword")

#         post_data = {
#             'fname': 'Updatedcaregiver',
#             'lname': 'UpdatedTest',
#             'email': 'updated@example.com',
#             'street': '456 Updated Street',
#             'suburb': 'UpdatedSuburb',
#             'state': 'UpdatedState',
#             'postcode': '67890',
#         }

#         response = self.client.post(reverse('Edit_caregiver'), data=post_data)

#         updated_user = User.objects.get(username="testcaregiver")
#         self.assertEqual(updated_user.first_name, 'Updatedcaregiver')

#         caregiver = Caregiver.objects.get(Name="testcaregiver")
#         self.assertEqual(caregiver.Cost, 100) 

# class AdminProfileTestCase(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testadmin", 
#             password="testpassword", 
#             first_name="Admin", 
#             last_name="Test", 
#             email="admin@example.com"
#         )
#         UserProfile.objects.create(user=self.user, address="123 Test Street, TestSuburb, TestState, 12345")
#         self.client = Client()

#     def test_edit_admin(self):
#         self.client.login(username="testadmin", password="testpassword")
        
#         new_data = {
#             'fname': 'UpdatedAdmin',
#             'lname': 'UpdatedTest',
#             'email': 'updatedadmin@example.com',
#             'street': '456 New Street',
#             'suburb': 'NewSuburb',
#             'state': 'NewState',
#             'postcode': '67890',
#         }
#         response = self.client.post(reverse('Edit_Admin'), data=new_data) 
        
#         updated_user = User.objects.get(id=self.user.id)
#         updated_profile = updated_user.userprofile

#         self.assertEqual(updated_user.first_name, 'UpdatedAdmin')
#         self.assertEqual(updated_user.last_name, 'UpdatedTest')
#         self.assertEqual(updated_user.email, 'updatedadmin@example.com')
#         self.assertEqual(updated_profile.address, '456 New Street, NewSuburb, NewState, 67890')
        
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your profile has been updated successfully!')

#     def test_get_admin(self):
#         self.client.login(username="testadmin", password="testpassword")
        
#         response = self.client.get(reverse('Get_Admin'))
        
#         self.assertEqual(response.context['first_name'], "Admin")
#         self.assertEqual(response.context['last_name'], "Test")
#         self.assertEqual(response.context['email'], "admin@example.com")
#         self.assertEqual(response.context['street'], "123 Test Street")
#         self.assertEqual(response.context['suburb'], "TestSuburb")
#         self.assertEqual(response.context['state'], "TestState")
#         self.assertEqual(response.context['postcode'], "12345")

# class CaregiverOrderTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#         self.caregiver = Caregiver.objects.create(CaregiverID=self.user.id)
#         self.order = CaregiverOrder.objects.create(CaregiverID=self.caregiver, UserID=self.user, Cost=100, start_time="2023-11-01 09:00:00", end_time="2023-11-01 10:00:00")
        
#         self.client = Client()
#         self.client.login(username="testuser", password="testpassword")
    
#     def test_get_caregiver_orders(self):
#         response = self.client.get(reverse('get_caregiver_orders'))
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data[0]['cost'], 100)

# class UserOrderTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#         self.caregiver = Caregiver.objects.create(CaregiverID=self.user.id)
#         self.order = CaregiverOrder.objects.create(CaregiverID=self.caregiver, UserID=self.user, Cost=100, start_time="2023-11-01 09:00:00", end_time="2023-11-01 10:00:00")
        
#         self.client = Client()
#         self.client.login(username="testuser", password="testpassword")
    
#     def test_get_user_orders(self):
#         response = self.client.get(reverse('get_user_orders'))
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data[0]['cost'], 100)

# class DoctorOrderTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username="testdoctor", password="testpassword")
#         self.doctor = GP.objects.create(GPID=self.user.id, Cost = 20)
#         self.order = GPOrder.objects.create(GPID=self.doctor, UserID=self.user, Cost=200, Date="2023-11-01")
        
#         self.client = Client()
#         self.client.login(username="testdoctor", password="testpassword")
    
#     def test_get_doctor_orders(self):
#         response = self.client.get(reverse('get_doctor_orders'))
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data[0]['cost'], 200)

# class AppointmentTestCase(TestCase):

#     def setUp(self):
#         # Setup a client for testing
#         self.client = Client()

#         # Setup a test user
#         self.user = User.objects.create_user(username="testuser", password="testpassword")

#         # Setup a test caregiver
#         self.caregiver = Caregiver.objects.create(CaregiverID=1, Name="Test Caregiver")

#     def test_successful_appointment(self):
#         # Login as the test user
#         self.client.login(username="testuser", password="testpassword")

#         # Send a POST request to create an appointment
#         response = self.client.post(reverse('appointment'), data={
#             "start-time": "08:00",
#             "end-time": "09:00",
#             "caregiver_id": self.caregiver.CaregiverID,
#             "cost": "100",
#             "selected_date": "2023-11-02"
#         })

#         # Check if the response is a redirect as expected
#         self.assertEqual(response.status_code, 302)

#         # Check if the appointment order was created in the database
#         self.assertTrue(CaregiverOrder.objects.exists())

#         # Check for a success message in the response
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Success")

#     def test_invalid_time(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.post(reverse('appointment'), data={
#             "start-time": "08:00",
#             "end-time": "08:30",
#             "caregiver_id": self.caregiver.CaregiverID,
#             "cost": "100",
#             "selected_date": "2023-11-02"
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(CaregiverOrder.objects.exists())
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "The appointment must last at least 1 hour!")

#     def test_caregiver_unavailability(self):
#         # Create an overlapping order in advance
#         CaregiverOrder.objects.create(
#             UserID=self.user,
#             CaregiverID=self.caregiver,
#             start_time=datetime.datetime(2023, 11, 2, 8, 0),
#             end_time=datetime.datetime(2023, 11, 2, 9, 0),
#             Cost=100
#         )

#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.post(reverse('appointment'), data={
#             "start-time": "08:30",
#             "end-time": "09:30",
#             "caregiver_id": self.caregiver.CaregiverID,
#             "cost": "100",
#             "selected_date": "2023-11-02"
#         })

#         # Ensure only the original order exists and a new overlapping order was not created
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(CaregiverOrder.objects.count(), 1)

#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Not an available user")

#     def test_get_request(self):
#         response = self.client.get(reverse('appointment'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'select.html')

# class AdminGetOrderTests(TestCase):

#     def setUp(self):
#         self.client = Client()

#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpassword'
#         )
#         self.caregiver_1 = Caregiver.objects.create(
#             Name="Caregiver 1",
#             Gender="Male",
#             Age=35,
#             Qualification="Nursing Degree",
#             Experience=5,
#             ServiceArea="Home Care",
#             Availability="Available",
#             Cost=500,
#             avatar="avatars/default_caregiver1.jpeg"
#         )

#         self.caregiver_2 = Caregiver.objects.create(
#             Name="Caregiver 2",
#             Gender="Female",
#             Age=40,
#             Qualification="Advanced Nursing Diploma",
#             Experience=8,
#             ServiceArea="Special Needs",
#             Availability="Available",
#             Cost=600,
#             avatar="avatars/default_caregiver2.jpeg"
#         )

#         self.caregiver_order_1 = CaregiverOrder.objects.create(
#             start_time=datetime.datetime.now(),
#             end_time=datetime.datetime.now() + datetime.timedelta(hours=2),
#             Cost=100,
#             CaregiverID=self.caregiver_1,  # Assign Caregiver instance directly
#             UserID=self.user  # Assuming user instance exists
#         )

#         self.caregiver_order_2 = CaregiverOrder.objects.create(
#             start_time=datetime.datetime.now() - datetime.timedelta(days=1),
#             end_time=datetime.datetime.now() - datetime.timedelta(days=1, hours=-1),
#             Cost=200,
#             CaregiverID=self.caregiver_2,  # Assign Caregiver instance directly
#             UserID=self.user  # Assuming user instance exists
#         )

#         # Setting up mock data for GP
#         self.gp_1 = GP.objects.create(
#             Name="Dr. John",
#             Gender="Male",
#             Age=30,
#             Qualification="MBBS",
#             Experience=5,
#             ServiceArea="Cardiology",
#             Availability=True,
#             Cost=1000,
#             avatar="avatars/default2.jpeg"
#         )

#         self.gp_2 = GP.objects.create(
#             Name="Dr. Smith",
#             Gender="Female",
#             Age=35,
#             Qualification="MD",
#             Experience=7,
#             ServiceArea="Neurology",
#             Availability=True,
#             Cost=1500,
#             avatar="avatars/default2.jpeg"
#         )

#         # Link GP and Caregiver orders to the created GP and Caregiver
#         self.caregiver_order_1.CaregiverID = self.caregiver_1
#         self.caregiver_order_1.UserID = self.user  # Assuming user is created
#         self.caregiver_order_1.save()

#         self.caregiver_order_2.CaregiverID = self.caregiver_2
#         self.caregiver_order_2.UserID = self.user  # Assuming user is created
#         self.caregiver_order_2.save()

#         self.gp_order_1 = GPOrder.objects.create(
#             start_time=datetime.datetime.now(),
#             end_time=datetime.datetime.now() + datetime.timedelta(hours=2),
#             Cost=1000,
#             GPID=self.gp_1,
#             UserID=self.user  # Assuming user is created
#         )

#         self.gp_order_2 = GPOrder.objects.create(
#             start_time=datetime.datetime.now() - datetime.timedelta(days=1),
#             end_time=datetime.datetime.now() - datetime.timedelta(days=1, hours=-1),
#             Cost=2000,
#             GPID=self.gp_2,
#             UserID=self.user  # Assuming user is created
#         )

#     def test_get_all_orders(self):
#         response = self.client.get(reverse('get_all_orders'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)

#     def test_get_all_dockers(self):
#         response = self.client.get(reverse('path_to_get_all_GP_view/'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)

#     def test_get_five_GP(self):
#         response = self.client.get(reverse('get_recent_GP'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)  

#     def test_get_recent_GP_orders(self):
#         response = self.client.get(reverse('get_recent_GP_orders'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)

#     def test_get_all_GP_orders(self):
#         response = self.client.get(reverse('get_all_GP_orders'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)

#     def test_get_recent_orders(self):
#         response = self.client.get(reverse('get_recent_orders'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)




# class TestSignUpFunction(TestCase):

#     def setUp(self):
#         self.client = Client()
        
#     def test_invalid_email(self):
#         response = self.client.post(reverse('SignUp'), {'Email': 'invalidemail', 'Username2': 'new_user', 'pw': 'ValidP@ss123', 'Street': '123 St', 'Suburb': 'Some Suburb', 'State': 'Some State', 'Postcode': '12345', 'register-as-caregiver': 'on'})
#         self.assertIn("Enter a valid email address.", response.content.decode())

#     def test_existing_email(self):
#         User.objects.create_user(username='existing_user', email='existing_email@example.com', password='ValidP@ss123')
#         response = self.client.post(reverse('SignUp'), {'Email': 'existing_email@example.com', 'Username2': 'new_user', 'pw': 'ValidP@ss123', 'Street': '123 St', 'Suburb': 'Some Suburb', 'State': 'Some State', 'Postcode': '12345', 'register-as-caregiver': 'on'})
#         self.assertIn("Email already exists.", response.content.decode())

#     def test_invalid_password(self):
#         response = self.client.post(reverse('SignUp'), {'Email': 'new_email@example.com', 'Username2': 'new_user', 'pw': 'short', 'Street': '123 St', 'Suburb': 'Some Suburb', 'State': 'Some State', 'Postcode': '12345', 'register-as-caregiver': 'on'})
#         self.assertIn("Password must be at least 8 characters long.", response.content.decode())

#     def test_successful_signup_as_caregiver(self):
#         response = self.client.post(reverse('SignUp'), {'Email': 'new_email@example.com', 'Username2': 'new_user', 'pw': 'ValidP@ss123', 'Street': '123 St', 'Suburb': 'Some Suburb', 'State': 'Some State', 'Postcode': '12345', 'register-as-caregiver': 'on'})
#         self.assertEqual(response.status_code, 302) 
#         self.assertEqual(response.url, '/caregiver_dashboard/')

#     def test_successful_signup_as_user(self):
#         response = self.client.post(reverse('SignUp'), {'Email': 'new_email@example.com', 'Username2': 'new_user', 'pw': 'ValidP@ss123', 'Street': '123 St', 'Suburb': 'Some Suburb', 'State': 'Some State', 'Postcode': '12345', 'register-as-caregiver': 'off'})
#         self.assertEqual(response.status_code, 302) 
#         self.assertEqual(response.url, '/user_dashboard/')

#     def test_get_request(self):
#         response = self.client.post(reverse('SignUp'))
#         self.assertEqual(response.status_code, 200)  # Assuming it's a successful render of the page.
#         self.assertNotIn("error_message", response.content.decode())  # Assuming no error messages are shown on GET.

# class TestPasswordFunction(TestCase):

#     def test_short_password(self):
#         self.assertFalse(is_password("Ab1"))

#     def test_no_lowercase(self):
#         self.assertFalse(is_password("ABCDEFGH1"))

#     def test_no_uppercase(self):
#         self.assertFalse(is_password("abcdefgh1"))

#     def test_no_digit(self):
#         self.assertFalse(is_password("Abcdefgh"))

#     def test_valid_password(self):
#         self.assertTrue(is_password("Abcdefgh1"))

# class TestCheckEmailAndUsername(TestCase):
    
#     def setUp(self):
#         self.factory = RequestFactory()
#         User.objects.create_user(username='existing_user', email='existing_email@example.com', password='ValidP@ss123')

#     def test_invalid_email(self):
#         request = self.factory.get('/dummy_url/', {'email': 'invalidemail', 'username': 'new_user', 'password': 'ValidP@ss123'})
#         response = check_email_and_username(request)
#         self.assertIn("Invalid E-Mail", response.content.decode())

#     def test_existing_username(self):
#         request = self.factory.get('/dummy_url/', {'email': 'new_email@example.com', 'username': 'existing_user', 'password': 'ValidP@ss123'})
#         response = check_email_and_username(request)
#         self.assertIn("User name exits", response.content.decode())

#     def test_existing_email(self):
#         request = self.factory.get('/dummy_url/', {'email': 'existing_email@example.com', 'username': 'new_user', 'password': 'ValidP@ss123'})
#         response = check_email_and_username(request)
#         self.assertIn("E-Mail already exists", response.content.decode())

#     def test_invalid_password(self):
#         request = self.factory.get('/dummy_url/', {'email': 'new_email@example.com', 'username': 'new_user', 'password': 'short'})
#         response = check_email_and_username(request)
#         expected_message = "The password must meet the following criteria:\\n\\nBe at least 8 characters long.\\nContain at least one lowercase letter, one uppercase letter and one number."
#         self.assertIn(expected_message, response.content.decode())

#     def test_all_valid(self):
#         request = self.factory.get('/dummy_url/', {'email': 'new_email@example.com', 'username': 'new_user', 'password': 'ValidP@ss123'})
#         response = check_email_and_username(request)
#         self.assertEqual('{"message": ""}', response.content.decode())

# class TestPasswordValidation(TestCase):

#     def test_short_password(self):
#         """Password that is too short should raise a ValidationError."""
#         with self.assertRaisesMessage(ValidationError, "Password must be at least 8 characters long."):
#             validate_password('Short1')

#     def test_missing_lowercase(self):
#         """Password without a lowercase letter should raise a ValidationError."""
#         with self.assertRaisesMessage(ValidationError, "Password must contain at least one lowercase letter."):
#             validate_password('PASSWORD123')

#     def test_missing_uppercase(self):
#         """Password without an uppercase letter should raise a ValidationError."""
#         with self.assertRaisesMessage(ValidationError, "Password must contain at least one uppercase letter."):
#             validate_password('password123')

#     def test_missing_number(self):
#         """Password without a number should raise a ValidationError."""
#         with self.assertRaisesMessage(ValidationError, "Password must contain at least one number."):
#             validate_password('PasswordOnly')

#     def test_valid_password(self):
#         """Valid password should not raise any exceptions."""
#         try:
#             validate_password('ValidPassword1')
#         except ValidationError:
#             self.fail("validate_password() raised ValidationError unexpectedly!")

# class LogoutViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='test_user', password='test_password')

#     @staticmethod
#     def add_session_to_request(request):
#         """Middleware function to add a session to the request."""
#         middleware = SessionMiddleware()
#         middleware.process_request(request)
#         request.session.save()
#         return request

#     def test_logout(self):
#         """Test if the user is logged out and redirected to the home page."""
#         # Log in the user
#         self.client.login(username='test_user', password='test_password')

#         # Ensure user is authenticated
#         self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))

#         # Call the logout view
#         request = self.factory.get('/logout/')
#         request.user = self.user
#         request = self.add_session_to_request(request)
#         response = logout_view(request)

#         # Check if the user has been logged out
#         self.assertIsInstance(request.user, AnonymousUser)

#         # Check if the response is a redirect to the home page
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/')


if __name__ == '__main__':
    unittest.main()
