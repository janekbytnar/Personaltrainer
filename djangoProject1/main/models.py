from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Plans(models.Model):
    name = models.CharField(max_length=200, unique=True)
    priceMonthly = models.IntegerField()
    priceYearly = models.IntegerField()
    description = models.TextField()
    descriptionLong = models.TextField()
    sex = models.CharField(max_length=10)
    stripe_product_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):

        return {
            'plan': self.name,
            'description': str(self.description),
            'priceMonthly': str(self.priceMonthly),
            'priceYearly': self.priceYearly,
            'descriptionLong': self.descriptionLong,
            'sex': self.sex,
        }


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    video = models.CharField(max_length=500)
    partOfBody = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Workout(models.Model):
    day = models.IntegerField()
    series = models.IntegerField(null=True, blank=True)
    reps1 = models.IntegerField(null=True, blank=True)
    reps2 = models.IntegerField(null=True, blank=True)
    reps3 = models.IntegerField(null=True, blank=True)
    reps4 = models.IntegerField(null=True, blank=True)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def to_dict(self):
        if self.series == 1:
            reps = [self.reps1]
        elif self.series == 2:
            reps = [self.reps1, self.reps2]
        elif self.series == 3:
            reps = [self.reps1, self.reps2, self.reps3]
        elif self.series == 4:
            reps = [self.reps1, self.reps2, self.reps3, self.reps4]
        else:
            reps = []

        return {
            'day': self.day,
            'plan': str(self.plan),
            'exercise': str(self.exercise),
            'series': self.series,
            'reps': reps,
        }
    def __str__(self):
        return f"{str(self.plan)} - dzien: {str(self.day)}"


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE, null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    nextPlan = models.ForeignKey(Plans, on_delete=models.CASCADE, null=True, blank=True, related_name='next_plan')
    active = models.BooleanField(default=False)
    subscription_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{str(self.user)} - {str(self.plan)}"


class Messages(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

