from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CompanyDigit(models.Model):
	reg=models.CharField(max_length=200)
	capi=models.CharField(max_length=200)
	withd=models.CharField(max_length=200)
	depo=models.CharField(max_length=200)

	#hfhfddg