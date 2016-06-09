from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User#, AbstractUser

# Create your models here.
class UserProfile(models.Model):  

	GENDER_CHOICES = (
		('Male', 'Male'),
		('Female', 'Female'),
	)

	# One to one with user model
	user = models.OneToOneField(User)

	# fields required for registration
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name  = models.CharField(max_length=100, blank=True, null=True)
	email      = models.CharField(max_length=100, blank=True, null=True)
	age        = models.PositiveIntegerField(blank=True, null=True)
	gender     = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
	weight     = models.PositiveIntegerField(blank=True, null=True)
	height     = models.PositiveIntegerField(blank=True, null=True)
	
	def __unicode__(self):
		return self.user.username

class Food(models.Model):
	food_id = models.IntegerField()
	food_name = models.CharField(max_length=100)
	food_type = models.CharField(max_length=100)
	brand_name = models.CharField(max_length=100)
	calories = models.DecimalField(max_digits=7, decimal_places=3)
	carbohydrate = models.DecimalField(max_digits=7, decimal_places=3)
	protein = models.DecimalField(max_digits=7, decimal_places=3)
	fat = models.DecimalField(max_digits=7, decimal_places=3)
	saturated_fat = models.DecimalField(max_digits=7, decimal_places=3)
	polyunsaturated_fat = models.DecimalField(max_digits=7, decimal_places=3)
	monounsaturated_fat = models.DecimalField(max_digits=7, decimal_places=3)
	trans_fat = models.DecimalField(max_digits=7, decimal_places=3)
	cholesterol = models.DecimalField(max_digits=7, decimal_places=3)
	sodium = models.DecimalField(max_digits=7, decimal_places=3)
	potassium = models.DecimalField(max_digits=7, decimal_places=3)
	fiber = models.DecimalField(max_digits=7, decimal_places=3)
	sugar = models.DecimalField(max_digits=7, decimal_places=3)
	vitamin_a = models.IntegerField()
	vitamin_c = models.IntegerField()
	calcium = models.IntegerField()
	iron = models.IntegerField()

class Serving(models.Model):
	serving_id = models.IntegerField()
	serving_description = models.CharField(max_length=100)
	metric_serving_amount = models.DecimalField(max_digits=7, decimal_places=3)
	metric_serving_unit = models.CharField(max_length=3)
	number_of_units = models.DecimalField(max_digits=7, decimal_places=3)
	measurement_description = models.CharField(max_length=100)

#class Nutrition(models.Model):
#	calories = models.DecimalField(max_digits=7, decimal_places=3)
#	carbohydrate = models.DecimalField(max_digits=7, decimal_places=3)
#	protein = models.DecimalField(max_digits=7, decimal_places=3)
#	fat = models.DecimalField(max_digits=7, decimal_places=3)
#	saturated_fat = models.DecimalField(max_digits=7, decimal_places=3)
#	polyunsaturated_fat = models.DecimalField(max_digits=7, decimal_places=3)
#	monounsaturated_fat = models.DecimalField(max_digits=7, decimal_places=3)
#	trans_fat = models.DecimalField(max_digits=7, decimal_places=3)
#	cholesterol = models.DecimalField(max_digits=7, decimal_places=3)
#	sodium = models.DecimalField(max_digits=7, decimal_places=3)
#	potassium = models.DecimalField(max_digits=7, decimal_places=3)
#	fiber = models.DecimalField(max_digits=7, decimal_places=3)
#	sugar = models.DecimalField(max_digits=7, decimal_places=3)
#	vitamin_a = models.IntegerField()
#	vitamin_c = models.IntegerField()
#	calcium = models.IntegerField()
#	iron = models.IntegerField()

#class MyUser(AbstractUser):
#	GENDER_CHOICES = (
#		('M', 'Male'),
#		('F', 'Female'),
#	)
#
#	age    = models.IntegerField()
#	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#	weight = models.FloatField()
#	height = models.FloatField()
#
#	REQUIRED_FIELDS = ['email', 'age', 'gender', 'weight', 'height']
