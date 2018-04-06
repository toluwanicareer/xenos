from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from .core import bitcoin_dollar_rate, convert_to_dollar

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
	profit=models.DecimalField(default=0, decimal_places=10, max_digits=20)
	date=models.DateTimeField(auto_now_add=True, null=False)
	last_updated=models.DateTimeField(null=True, default=datetime.now() )
	status=models.CharField(null=True,max_length=200, default='Pending', choices=(('Pending', 'Pending'),('Active', 'Active'), ('Completed', 'Completed')))
	reinvest=models.BooleanField(default=True)
	bitaddress=models.CharField(max_length=200, null=True)


	
	
	


	def add_profit(self):
		now=timezone.now()
		day=now-self.last_updated
		payt_day=now-self.date
		percentage=Percentage.objects.get(plan=self.plan).percentage
		plan=self.plan
		user=self.user
		if self.status=='Active':
			if day.days >= 1:
				self.profit+=(percentage*self.amount)#*0.01)
				self.last_updated=now	
			if payt_day.days >= int(plan.days):
				self.status=='Completed'
				user.profile.wallet=self.profit+self.amount+user.profile.wallet
				user.profile.save()
			self.save()
		elif self.status=='Pending'	:
			if payt_day.days >=1:
				self.delete()

	def pay_referee(self):
		referee=self.user.profile.referer
		try:
			referee=User.objects.get(username=referee)
		except:
			return True
		credit_amount=float(referee.profile.wallet)+(0.05*int(self.amount))
		referee.profile.wallet=credit_amount
		Transaction.objects.create(trans_type='Credit', amount=credit_amount, status='Success', user=referee, info='Referall Credit')
		referee.profile.save()
		return True






class Transaction(models.Model):
	trans_type=models.CharField(max_length=200, choices=(('Credit', 'Credit'),('Withdrawal','Withdrwal')))
	amount=models.IntegerField(null=True)
	status=models.CharField(max_length=200, choices=(('Pending', 'Pending'), ('Success', 'Success')))
	created_date=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(User, null=True)
	info=models.CharField(max_length=200, null=True)
	model_trans=models.CharField(max_length=200, null=True)
	model_id=models.IntegerField(null=True)
	bitaddress=models.CharField(null=True, max_length=200)
	

	def complete(self, amount):
		'''
		This function will update your wallet 
		'''

		rate=bitcoin_dollar_rate()
		dollar_amount=covert_to_dollar(amount)
		self.amount=dollar_amount
		self.status='Success'
		return amount

	


class Percentage(models.Model):
	plan=models.ForeignKey(Plan)
	percentage=models.DecimalField(max_length=20, decimal_places=10,max_digits=19 )

	def __str__(self):
		return self.plan.name

class test_model(models.Model):
	justin=models.CharField(max_length=20)
	data=models.TextField()	

class Post(models.Model):
	title=models.CharField(max_length=200)
	text=models.TextField()
	created_date=models.DateTimeField(auto_now_add=True)



class xenos_bot(models.Model):
	plan_name=models.CharField(max_length=200)
	price=models.IntegerField()

	def __str__(self):
		return self.plan_name

class xenos_payment(models.Model):
	bot=models.ForeignKey(xenos_bot)
	bought_user=models.ForeignKey(User, null=True)
	status=models.CharField(max_length=200, null=True, choices=(('Pending', 'Pending'), ('Success', 'Success')))
	address=models.CharField(max_length=200, null=True)
	

	def __str__(self):
		return self.bot.plan_name


