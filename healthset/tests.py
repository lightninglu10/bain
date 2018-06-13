from django.test import TestCase
from healthset.models import Provider, Inpatient
from rest_framework.test import APIRequestFactory, APITestCase
from healthset.views import InpatientViewSet

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

class InpatientTest(APITestCase):
    """ 
    Test for inpatient API
    Remember that the pagination is set at 20,
    so the max of any set will be 20
    """
    def setUp(self):
        provider = Provider.objects.create(
            provider_id=1,
            name="Test Provider",
            street_address="Test",
            city="Test City",
            state="GA",
            zip_code="32317",
            region_description="Test Region"
        )
        provider2 = Provider.objects.create(
            provider_id=1,
            name="Test Provider",
            street_address="Test",
            city="Test City",
            state="CA",
            zip_code="32317",
            region_description="Test Region"
        )
        for i in range(20):
            Inpatient.objects.create(
                provider=provider,
                drg="TEST DRG",
                total_discharges=i,
                avg_covered_charges=(i * 100000),
                avg_total_payments=(i * 10000),
                avg_medicare_payments=(i * 5000)
            )

        Inpatient.objects.create(
            provider=provider2,
            drg="TEST DRG2",
            total_discharges=0,
            avg_covered_charges=(0),
            avg_total_payments=(0),
            avg_medicare_payments=(0)
        )
        self.factory = APIRequestFactory()

    def make_request(self, query_filter):
        request = self.factory.get('/providers{}'.format(query_filter))
        view = InpatientViewSet.as_view({'get': 'list'})
        return view(request)

    def test_max_discharges(self):
        response = self.make_request('?max_discharges=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 4)

    def test_min_discharges(self):
        response = self.make_request('?min_discharges=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 18)

    def test_max_average_covered_charges(self):
        response = self.make_request('?max_average_covered_charges=5000.15')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 7)

    def test_min_average_covered_charges(self):
        response = self.make_request('?min_average_covered_charges=5000.15')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 14)

    def test_max_average_medicare_payments(self):
        response = self.make_request('?max_average_medicare_payments=500.15')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 12)

    def test_min_average_medicare_payments(self):
        response = self.make_request('?min_average_medicare_payments=500.15')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 9)

    def test_state(self):
        response = self.make_request('?state=GA')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 20)

    def test_state_none(self):
        response = self.make_request('?state=FL')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_state_one(self):
        response = self.make_request('?state=CA')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_bad_inputs(self):
        response = self.make_request(
            ("?state=CAFW&"
            "min_average_medicare_payments=fa&"
            "max_average_medicare_payments=jk&"
            "max_average_covered_charges=fa&"
            "min_discharges=fa&"
            "max_discharges=ff&"
            "min_average_covered_charges=jk")
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual('max_discharges' in response.data, True)
        self.assertEqual('state' in response.data, True)
        self.assertEqual('min_average_medicare_payments' in response.data, True)
        self.assertEqual('max_average_medicare_payments' in response.data, True)
        self.assertEqual('min_average_covered_charges' in response.data, True)
        self.assertEqual('max_average_covered_charges' in response.data, True)
        self.assertEqual('min_discharges' in response.data, True)


        # self.assertEqual(response.data)

