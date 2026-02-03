from django.db import models

class EquipmentDataset(models.Model):
    name = models.CharField(max_length=100)
    upload_time = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return self.name
