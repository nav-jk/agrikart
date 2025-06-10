from django.db import models

class Farmer(models.Model):
    phone_number = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class Produce(models.Model):
    farmer = models.ForeignKey(Farmer, related_name='produce', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.quantity} units"
