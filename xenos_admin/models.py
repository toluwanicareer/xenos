from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.

class Plan(models.Model):
	name=models.CharField(max_length=50)
	interest=models.CharField(max_length=20)
	minimum=models.IntegerField()
	maximum=models.IntegerField()
	days=models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Investment(models.Model):
	user=models.ForeignKey(User)
	amount=models.IntegerField()
	plan=models.ForeignKey(Plan)
	profit=models.IntegerField(default=0)
	date=models.DateTimeField(auto_now_add=True, null=False)
	last_updated=models.DateTimeField(null=True, default=datetime.now())
	status=models.CharField(null=True,max_length=200, default='Pending', choices=(('Pending', 'Pending'),('Active', 'Active'), ('Completed', 'Completed')))
	reinvest=models.BooleanField(default=True)
	bitaddress=models.CharField(max_length=200, null=True)
	link=models.URLField(null=True)
	def add_profit(self):
		now=timezone.now()
		day=now-self.last_updated
		payt_day=now-self.date
		if self.status=='Active':
			if day.days >= 1:
				percentage=Percentage.objects.get(plan=self.plan).percentage
				self.profit+=(percentage*self.amount)
				self.last_updated=now
				self.save()
		elif self.status=='Pending'	:
			if payt_day.days >=1:
				self.delete()
				

			



class Percentage(models.Model):
	plan=models.ForeignKey(Plan)
	percentage=models.DecimalField(max_length=20, decimal_places=3,max_digits=19 )
	


