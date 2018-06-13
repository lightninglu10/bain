from django.db import models

class Provider(models.Model):
    """
    A specific medical provider location
    @field name -- Name of the medical provider
    @field street -- Street of provider
    @field city -- City of provider
    @field state -- State of provider, as uppercase 2 char short state
    @field zip_code -- the zip code of the provider
    @field region_description -- additional information about the region
    """
    provider_id = models.IntegerField()
    name = models.CharField(max_length=1024)
    street_address = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=3, db_index=True)
    zip_code = models.CharField(max_length=10)
    region_description = models.CharField(max_length=1024)

    def __str__(self):
        """
        Returns stringified version of the Provider model
        """
        return 'Provider: {}'.format(self.name)

class Inpatient(models.Model):
    """
    A specific inpatient
    @field provider -- The medical provider
    @field drg -- drg definition
    @field total_discharges -- total amount of discharges
    @field avg_covered_charges -- the average covered charges in cents
    @field avg_total_payments -- avg in total payments in cents
    @field avg_medicare_payments -- avg in medicare payments in cents
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    drg = models.CharField(max_length=1024)
    total_discharges = models.IntegerField(default=0, db_index=True)
    avg_covered_charges = models.IntegerField(default=0, db_index=True)
    avg_total_payments = models.IntegerField(default=0, db_index=True)
    avg_medicare_payments = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        """
        Returns stringified version of the Inpatient model
        """
        return 'Description: {}'.format(self.drg)
