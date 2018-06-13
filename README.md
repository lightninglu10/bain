# bain coding challenge 

http://ec2-52-39-138-129.us-west-2.compute.amazonaws.com:8000/providers

For this challenge, I used Python Django as the server, and django-rest-framework for the API. To manage dependencies, I used pipenv(https://github.com/pypa/pipenv), which is way nicer than just pip + requirements.txt.

I put the data into a sqlite3 db. This makes it super easy to put online without having to pay extra $$ or do extra configuration to put up Postgres which I normally would use.

I broke down the data into two models: Provider model and a Inpatient model. The provider model is the location of the hospital and includes information such as 

```python
provider_id = models.IntegerField()
name = models.CharField(max_length=1024)
street_address = models.CharField(max_length=1024)
city = models.CharField(max_length=1024)
state = models.CharField(max_length=3, db_index=True)
zip_code = models.CharField(max_length=10)
region_description = models.CharField(max_length=1024)
```

The Inpatient model held the data about the specific DRG, and then referenced the provider as a foreign key.

```python
provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
drg = models.CharField(max_length=1024)
total_discharges = models.IntegerField(default=0, db_index=True)
avg_covered_charges = models.IntegerField(default=0, db_index=True)
avg_total_payments = models.IntegerField(default=0, db_index=True)
avg_medicare_payments = models.IntegerField(default=0, db_index=True)
```

One data choice I made was to save the $$ as Integers in cents. Doing this makes it easier to overflow if the $$ is extremely large, but for this data set it looked reasonable to have cents as integers. When I convert the filter, I need to multiply the filter by 100, so if the filter is too large (greater than sys.maxint), then an error will be thrown. 

Once we got the data into a db, it was easy to query & filter the data with django's __lte or __gte fields. I added pagination to the return so that the data returns quickly. 

I added Django Silk to debug the data calls and if you take a look at http://ec2-52-39-138-129.us-west-2.compute.amazonaws.com:8000/silk, you'll see that the max amount of queries made to the DB is 3: one for the Provider, one for the Inpatient, and one for the total count. The count should be able to be optimized but I left that for now.

I've default set the pagination to just be by page and it's default 20 items per page. Currently the results are not ordered by anything, so the pagination can't guarantee the same order each time.

The return looks like this:

```
{
    "count": 1396,
    "next": "http://localhost:8007/providers/?max_discharges=89&min_discharges=88&page=3",
    "previous": "http://localhost:8007/providers/?max_discharges=89&min_discharges=88",
    "results": [
        {
            "Average Covered Charges": "$13,206.13",
            "Average Total Payments": "$4,110.28",
            "Average Medicare Payments": "$2,783.29",
            "Total Discharges": 88,
            "Hospital Referral Region Description": "MO - St. Louis",
            "Provider Zip Code": "62226",
            "Provider State": "IL",
            "Provider City": "BELLEVILLE",
            "Provider Street Address": "4500 MEMORIAL DRIVE",
            "Provider Name": "MEMORIAL HOSPITAL"
        },
        ...
```

Deployed to EC2 on a t2.micro utilizing Docker to run.

# Tests
To run tests, just run `python manage.py test` and it will run through a series of 10 tests. The tests I setup were just to count the number of items that we expect when we filter. I setup a test db with rest-framework's test framework and "pre-filled" it on each run with 21 items. We could test this more extensively, including combining queries, but I didn't feel the need to do so at the moment (if I remember my math correct, 7! combination of tests).

