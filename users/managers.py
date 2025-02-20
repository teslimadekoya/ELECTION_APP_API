from django.contrib.auth.models import BaseUserManager
from .utils import generate_voter_id


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        if '@' not in email and not email.endswith('.com'):
            raise ValueError('The Email is not valid')

        email = self.normalize_email(email)
        extra_fields['voters_id'] = generate_voter_id(20)  

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
