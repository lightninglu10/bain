from healthset.models import Provider, Inpatient
from django.core.management.base import BaseCommand
import csv
from decimal import Decimal

class Command(BaseCommand):
    help = 'CSV to SQL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', dest='path', required=True,
            help='the path to process',
        )

    def handle(self, *args, **options):
        path = options['path']
        # process the url
        with open(path) as f:
            reader = csv.reader(f)

            for index, row in enumerate(reader):
                if index == 0:
                    continue

                provider, created_provider = Provider.objects.get_or_create(
                    provider_id=row[1],
                    name=row[2],
                    street_address=row[3],
                    city=row[4],
                    state=row[5],
                    zip_code=row[6],
                    region_description=row[7]
                )

                _, created = Inpatient.objects.get_or_create(
                    provider=provider,
                    drg=row[0],
                    total_discharges=row[8],
                    avg_covered_charges=int(row[9].strip('$').replace('.', '')),
                    avg_total_payments=int(row[10].strip('$').replace('.', '')),
                    avg_medicare_payments=int(row[11].strip('$').replace('.', ''))
                )
            return 