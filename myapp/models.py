from django.db import models

class Phone(models.Model):
    phone_id = models.CharField(max_length=20, db_column='phone_id')
    serial_number = models.CharField(max_length=50, db_column='serial_number')
    full_name = models.CharField(max_length=100, db_column='full_name')

    class Meta:
        db_table = 'phones'  # Имя таблицы в БД
        managed = False      # Важно: Django не будет управлять таблицей через миграции

    def __str__(self):
        return self.full_name
