from django.db import models
from django.utils.timezone import now
from 

# Create your models here.

# Car Make model
clasas carMake(models.Model):
  name = models.CharField(null=False, max_lenght=50)
  descrtiption = models.CharField(null=True, max_length=500)
def __str__(self):
  return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=True)
    model_type = models.CharField(null=False, max_length=15, choices=CAR_CHOICES, default=SEDAN)
    
    YEAR_CHOICES = []
    for r in range(1969, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        ('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return self.name + ", " + str(self.year) + ", " + self.model_type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
