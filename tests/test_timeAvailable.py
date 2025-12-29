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

class CaregiverAvailabilityTest(TestCase):
    def setUp(self):
        # Create a Caregiver instance
        self.caregiver = Caregiver.objects.create(
            Name="Sample Caregiver",
            Gender="Male",
            ServiceArea="Area1"
        )
        
        self.caregiver2 = Caregiver.objects.create(
            Name="Sample Caregiver2",
            Gender="Male",
            ServiceArea="Area1"
        )  
        
        # create a user instance
        user = User.objects.create_user(
            username='john_doe', 
            password='john_password',
            email='john@example.com',
            first_name='John',
            last_name='Doe'
        )

        # Use the created Caregiver instance for CaregiverOrder
        self.caregiver_id = self.caregiver.CaregiverID
        self.caregiver2_id = self.caregiver2.CaregiverID
        self.sample_start_time = timezone.make_aware(datetime(2023, 11, 1, 10, 0))  
        self.sample_end_time = self.sample_start_time + timedelta(hours=2)
        
        # no overlap 
        CaregiverOrder.objects.create(
            CaregiverID=self.caregiver,  # Updated this line
            start_time=self.sample_start_time - timedelta(hours=4), #6:00
            end_time=self.sample_start_time - timedelta(hours=2),#8:00
            Cost=100,
            UserID=user
        )
                
        # overlap
        CaregiverOrder.objects.create(
            CaregiverID=self.caregiver,  # Updated this line
            start_time=self.sample_start_time + timedelta(minutes=30), #10:30
            end_time=self.sample_end_time + timedelta(minutes=30), #12:30
            Cost=100,
            UserID=user
        )
                
        # Create a CaregiverOrder for a different caregiver
        CaregiverOrder.objects.create(
            CaregiverID=self.caregiver,  
            start_time=self.sample_start_time, #8:00
            end_time=self.sample_end_time, #10:00
            Cost=100,
            UserID=user
        )

    
    # available    
    def test_caregiver_available(self):
        is_available = is_caregiver_available(self.caregiver_id, self.sample_start_time - timedelta(hours=1), self.sample_start_time)
        self.assertTrue(is_available, "The caregiver should be available")

    # not available
    def test_caregiver_not_available(self):
        is_available = is_caregiver_available(self.caregiver_id, self.sample_start_time + timedelta(minutes=30), self.sample_end_time)
        self.assertFalse(is_available, "The caregiver should not be available")
    
    # available  
    def test_caregiver_available_for_different_caregiver(self):
        is_available = is_caregiver_available(self.caregiver2_id, self.sample_start_time, self.sample_end_time)
        self.assertTrue(is_available, "The caregiver should be available")


