from django.db import models


# Create your models here.
class SudokuState(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField
    state = models.CharField(max_length=200)
    shape = models.CharField(max_length=200)

    def __str__(self):
        return self.state
