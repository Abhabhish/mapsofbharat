from django.db import models
import pandas as pd
from django.contrib.auth.models import User


class Csv(models.Model):
    csv_file = models.FileField(upload_to='csvs/')
    upload_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.csv_file)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.process_csv_data()

    def process_csv_data(self):
        data = pd.read_csv(self.csv_file.file)
        for index, row in data.iterrows():
            Population.objects.create(
                state=row['state'],
                district=row['district'],
                sub_district=row['sub_district'],
                block=row['block'],
                pincode = row['pincode'],
                population=row['population'],
                csv=self
            )

class Population(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100,null=True)
    sub_district = models.CharField(max_length=100,null=True)
    block = models.CharField(max_length=100,null=True)
    pincode = models.CharField(max_length=100,null=True)
    gram_panchayat = models.CharField(max_length=100,null=True)
    town_village = models.CharField(max_length=100,null=True)

    population = models.IntegerField()
    csv = models.ForeignKey(Csv,on_delete=models.CASCADE)



class Geojson(models.Model):
    state_name = models.CharField(max_length=100)
    state_geojson = models.FileField(upload_to='1state_geojson/',null=True)
    district_geojson = models.FileField(upload_to='2district_geojsons/',null=True)
    sub_district_geojson = models.FileField(upload_to='3sub_district_geojson/',null=True)
    block_geojson = models.FileField(upload_to='4block_geojson/',null=True)
    pincode_geojson = models.FileField(upload_to='5pincode_geojson/',null=True)
    gram_panchayat_geojson = models.FileField(upload_to='6gram_panchayat_geojson/',null=True)
    town_village_geojson = models.FileField(upload_to='7town_village_geojson/',null=True)
    


class ColorRangeFamily(models.Model):
    family_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.family_name

class ColorRange(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()
    color = models.CharField(max_length=50)
    color_range_family = models.ForeignKey(ColorRangeFamily,on_delete=models.CASCADE,related_name='color_ranges')

