from django.db import models

class ScanReport(models.Model):
    repository_name = models.CharField(max_length=255)
    review = models.TextField()
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repository_name} - {self.scanned_at}"