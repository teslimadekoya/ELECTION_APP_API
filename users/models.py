from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import generate_voter_id
from .managers import CustomUserManager

class User(AbstractUser):
    ROLE_CHOICES = (
        ('voter', 'Voter'),
        ('admin', 'Admin'),
    )
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    voters_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    state_of_origin = models.CharField(max_length=200)
    address = models.CharField(max_length=3000)
    occupation = models.CharField(max_length=200)
    gender = models.CharField(max_length=6)
    email = models.EmailField(max_length=1000, unique=True)
    phone_number = models.CharField(max_length=11)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=40, choices=ROLE_CHOICES, blank=False, null=False, default='voter')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.role = 'admin'
            self.voters_id = None  # Ensure that staff users have None for voters_id
        else:
            self.role = 'voter'
            if not self.voters_id:  # If not a staff user and voters_id is not set, generate it
                self.voters_id = generate_voter_id(20)
        
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
