from xenos_admin.models import Investment, Percentage
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

class Command(BaseCommand):
	args=''
	help ='Check the Invetsment, and update necessary Investment daily'

	def handle(self, *args, **options):
		for investment in Investment.objects.all():
			investment.add_profit()






			
