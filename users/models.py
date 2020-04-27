from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True,help_text='Designates whether this user is customer oor not!')
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', default='avatar.jpg', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    @property
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip() + (' (staff)' if self.is_staff else ' (customer)')

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
