from django.test import TestCase, Client, RequestFactory
from EMediCenter import views
from EMediCenter.views import *
from datetime import datetime, timedelta
from EMediCenter.models import *
from django.utils import timezone
import unittest
from unittest import mock
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser,User
from django.contrib.sessions.middleware import SessionMiddleware

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




class LoginViewTestCase(TestCase):
    
    @staticmethod
    def add_session_to_request(request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        return request
    
    def setUp(self):
        self.factory = RequestFactory()
        # Create a user and profile
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.profile = UserProfile.objects.create(user=self.user)  

    def test_non_existing_user(self):
        request = self.factory.post('/login/', {'Username': 'non_existing_user', 'password': 'some_password'})
        request = self.add_session_to_request(request)
        response = login_view(request)

        self.assertEqual(response.status_code, 200)  # render the login page again
        self.assertIn("User doesn&#x27;t exist.", response.content.decode())

    def test_wrong_password(self):
        request = self.factory.post('/login/', {'Username': 'test_user', 'password': 'wrong_password'})
        request = self.add_session_to_request(request)
        response = login_view(request)

        self.assertEqual(response.status_code, 200)  # render the login page again
        self.assertIn("Incorrect password.", response.content.decode())

    def test_inactive_user(self):
        # Make the user inactive
        self.user.is_active = False
        self.user.save()

        request = self.factory.post('/login/', {'Username': 'test_user', 'password': 'test_password'})
        request = self.add_session_to_request(request)
        response = login_view(request)
        self.assertEqual(response.status_code, 200)  # render the login page again
        self.assertIn("Your account is inactive.", response.content.decode()) # check error msg



    def test_login_successful(self):
        
        test_cases = [
            {"is_staff": True, "is_doctor": False, "is_caregiver": False, "expected_url": "/admin_dashboard/"},
            {"is_staff": False, "is_doctor": True, "is_caregiver": False, "expected_url": "/doctor_dashboard/"},
            {"is_staff": False, "is_doctor": False, "is_caregiver": True, "expected_url": "/caregiver_dashboard/"},
            {"is_staff": False, "is_doctor": False, "is_caregiver": False, "expected_url": "/user_dashboard/"}
        ]

        for test_case in test_cases:
            with self.subTest(**test_case):
                # Setting the user profile attributes
                self.user.is_staff = test_case["is_staff"]
                self.user.save()
                self.profile.is_doctor = test_case["is_doctor"]
                self.profile.is_caregiver = test_case["is_caregiver"]
                self.profile.save()

                request = self.factory.post('/login/', {'Username': 'test_user', 'password': 'test_password'})
                request = self.add_session_to_request(request)
                request.user = self.user
                response = login_view(request)

                # Redirect
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, test_case["expected_url"])





if __name__ == '__main__':
    unittest.main()
