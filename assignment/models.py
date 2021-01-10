from django.db import models

class Document(models.Model):
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.document


class ConsumerData(models.Model):
    title = models.CharField(max_length=20)
    data = models.TextField()

    def __str__(self):
        return self.data

