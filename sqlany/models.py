from django.db import models

class Query(models.Model):
    description = models.CharField(max_length=100)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.PROTECT, related_name='created_queries')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.PROTECT, related_name='updated_queries')
    parameters = models.ManyToManyField('QueryParameter', blank=True)

    def __str__(self):
        return self.description

class QueryParameter(models.Model):
    description = models.CharField(max_length=100)
    parameter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.PROTECT, related_name='created_query_parameters')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.PROTECT, related_name='updated_query_parameters')

    def __str__(self):
        return self.description