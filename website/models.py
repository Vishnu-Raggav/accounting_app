from django.db import models

# Create your models here.
class Invoice(models.Model):
    date = models.DateField()
    due_date = models.DateField()
    customer = models.CharField(max_length=255)
    items = models.JSONField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"""
        ID: {self.id}
        Customer: {self.customer}
        Date: {self.date}
        Due Date: {self.due_date}
        Items: {self.items}
        Status: {self.status}
        """

class Entry(models.Model):
    transaction_id = models.IntegerField()
    start_date = models.DateField()
    debit_account_name = models.CharField(max_length=255)
    credit_account_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amount = models.FloatField()

    def __str__(self):
        return f"""
        Transaction ID: {self.transaction_id}
        Date: {self.start_date}
        Debit Account: {self.debit_account_name}
        Credit Account: {self.credit_account_name}
        Category: {self.category}
        Amount: {self.amount}
        """