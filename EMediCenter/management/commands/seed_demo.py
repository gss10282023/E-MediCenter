from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from EMediCenter.models import Caregiver, CaregiverOrder, GP, GPOrder, PatientCase, UserProfile


class Command(BaseCommand):
    help = "Seed demo data for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default="demo12345",
            help="Password for demo users (default: demo12345).",
        )
        parser.add_argument(
            "--force-password",
            action="store_true",
            help="Reset password for existing demo users.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing demo data (users/records with 'demo_' prefix) before seeding.",
        )

    def handle(self, *args, **options):
        password: str = options["password"]
        force_password: bool = options["force_password"]
        clear: bool = options["clear"]

        with transaction.atomic():
            if clear:
                self._clear_demo_data()

            demo_admin = self._upsert_user(
                username="demo_admin",
                email="demo_admin@example.com",
                first_name="Demo",
                last_name="Admin",
                password=password,
                force_password=force_password,
                is_staff=True,
                is_superuser=True,
                profile_flags={},
            )
            demo_doctor = self._upsert_user(
                username="demo_doctor",
                email="demo_doctor@example.com",
                first_name="Demo",
                last_name="Doctor",
                password=password,
                force_password=force_password,
                is_staff=False,
                is_superuser=False,
                profile_flags={"is_doctor": True},
            )
            demo_caregiver = self._upsert_user(
                username="demo_caregiver",
                email="demo_caregiver@example.com",
                first_name="Demo",
                last_name="Caregiver",
                password=password,
                force_password=force_password,
                is_staff=False,
                is_superuser=False,
                profile_flags={"is_caregiver": True},
            )
            demo_customer = self._upsert_user(
                username="demo_customer",
                email="demo_customer@example.com",
                first_name="Demo",
                last_name="Customer",
                password=password,
                force_password=force_password,
                is_staff=False,
                is_superuser=False,
                profile_flags={},
            )

            now = timezone.now()

            doctor_gp, _ = GP.objects.update_or_create(
                GPID=demo_doctor.id,
                defaults={
                    "Name": demo_doctor.username,
                    "Gender": "M",
                    "Age": 35,
                    "Qualification": "MBBS",
                    "Experience": 10,
                    "ServiceArea": "Sydney",
                    "Availability": "Mon-Fri",
                    "Cost": 60,
                },
            )

            caregiver_obj, _ = Caregiver.objects.update_or_create(
                CaregiverID=demo_caregiver.id,
                defaults={
                    "Name": demo_caregiver.username,
                    "Gender": "F",
                    "Age": 30,
                    "Qualification": "Certificate III",
                    "Experience": 5,
                    "ServiceArea": "Sydney",
                    "Availability": "Mon-Fri",
                    "Cost": 40,
                },
            )

            # Extra GPs/caregivers for matching pages.
            self._upsert_gp(name="demo_gp_1", gender="F", service_area="Parramatta", cost=50)
            self._upsert_gp(name="demo_gp_2", gender="M", service_area="Chatswood", cost=70)
            self._upsert_gp(name="demo_gp_3", gender="F", service_area="Bondi", cost=90)
            self._upsert_caregiver(
                name="demo_caregiver_1",
                gender="M",
                service_area="Parramatta",
                cost=35,
                qualification="Certificate IV",
            )
            self._upsert_caregiver(
                name="demo_caregiver_2",
                gender="F",
                service_area="Chatswood",
                cost=55,
                qualification="Certificate III",
            )
            self._upsert_caregiver(
                name="demo_caregiver_3",
                gender="M",
                service_area="Bondi",
                cost=75,
                qualification="Certificate IV",
            )

            if not GPOrder.objects.filter(UserID=demo_customer, GPID=doctor_gp).exists():
                GPOrder.objects.create(
                    UserID=demo_customer,
                    GPID=doctor_gp,
                    Date=now.date(),
                    Cost=doctor_gp.Cost,
                    start_time=now + timedelta(days=1),
                    end_time=now + timedelta(days=1, hours=1),
                )

            if not CaregiverOrder.objects.filter(
                UserID=demo_customer, CaregiverID=caregiver_obj
            ).exists():
                CaregiverOrder.objects.create(
                    UserID=demo_customer,
                    CaregiverID=caregiver_obj,
                    Cost=caregiver_obj.Cost or 40,
                    start_time=now + timedelta(days=2),
                    end_time=now + timedelta(days=2, hours=2),
                )

            PatientCase.objects.update_or_create(
                user=demo_customer,
                disease_name="Seasonal Flu (Demo)",
                defaults={
                    "symptoms": "Fever, cough, sore throat (demo data).",
                    "diagnosing_doctor": doctor_gp,
                    "description": "This is a demo patient case record.",
                    "prescription": "Rest, fluids, and over-the-counter medication (demo only).",
                    "diagnosis_date": now.date(),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data seeded. Users: demo_admin, demo_doctor, demo_caregiver, demo_customer"
            )
        )
        self.stdout.write(self.style.SUCCESS(f"Password: {password}"))

    def _clear_demo_data(self) -> None:
        User.objects.filter(username__startswith="demo_").delete()
        GP.objects.filter(Name__startswith="demo_").delete()
        Caregiver.objects.filter(Name__startswith="demo_").delete()

    def _upsert_user(
        self,
        *,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        force_password: bool,
        is_staff: bool,
        is_superuser: bool,
        profile_flags: dict,
    ) -> User:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        if not created:
            needs_save = False
            if user.email != email:
                user.email = email
                needs_save = True
            if user.first_name != first_name:
                user.first_name = first_name
                needs_save = True
            if user.last_name != last_name:
                user.last_name = last_name
                needs_save = True
            if user.is_staff != is_staff:
                user.is_staff = is_staff
                needs_save = True
            if user.is_superuser != is_superuser:
                user.is_superuser = is_superuser
                needs_save = True
            if needs_save:
                user.save(update_fields=["email", "first_name", "last_name", "is_staff", "is_superuser"])

        if created or force_password:
            user.set_password(password)
            user.save(update_fields=["password"])

        profile, _ = UserProfile.objects.get_or_create(user=user)
        for field, value in profile_flags.items():
            setattr(profile, field, value)
        profile.save()

        return user

    def _upsert_gp(self, *, name: str, gender: str, service_area: str, cost: int) -> GP:
        gp, _ = GP.objects.update_or_create(
            Name=name,
            defaults={
                "Gender": gender,
                "Age": 40,
                "Qualification": "MBBS",
                "Experience": 8,
                "ServiceArea": service_area[:10],
                "Availability": "Mon-Fri",
                "Cost": cost,
            },
        )
        return gp

    def _upsert_caregiver(
        self,
        *,
        name: str,
        gender: str,
        service_area: str,
        cost: int,
        qualification: str,
    ) -> Caregiver:
        caregiver, _ = Caregiver.objects.update_or_create(
            Name=name,
            defaults={
                "Gender": gender,
                "Age": 28,
                "Qualification": qualification,
                "Experience": 3,
                "ServiceArea": service_area[:10],
                "Availability": "Mon-Fri",
                "Cost": cost,
            },
        )
        return caregiver
