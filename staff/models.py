from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from PIL import Image

from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(_('first name'), max_length=50, blank=True)
	last_name = models.CharField(_('last name'), max_length=50, blank=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	class Meta:
		verbose_name = _('user')
		
	    

	def get_full_name(self):
		#returns the first and last names with a space in the middle
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		#returns short name for the user
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		#sends an email to this User
		send_email(subject, message, from_email, [self.email], **kwargs)