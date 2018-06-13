from rest_framework import serializers
from .models import Inpatient, Provider

class ProviderSerializer(serializers.ModelSerializer):
    """ Serializer for question sets """

    class Meta:
        model = Provider
        fields = '__all__'

class InpatientSerializer(serializers.ModelSerializer):
    """ Serializer for question sets """

    provider = ProviderSerializer()

    avg_covered_charges = serializers.SerializerMethodField()

    class Meta:
        model = Inpatient
        # fields = '__all__'
        exclude = ('drg', )

    def get_avg_covered_charges(self, obj):
        import pdb; pdb.set_trace()

    def to_representation(self, obj):
        primitive_repr = super(InpatientSerializer, self).to_representation(obj)

        primitive_repr['Average Covered Charges'] = '${:,.2f}'.format(primitive_repr['avg_covered_charges'])
        del primitive_repr['avg_covered_charges']
        primitive_repr['Average Total Payments'] = '${:,.2f}'.format(primitive_repr['avg_total_payments'])
        del primitive_repr['avg_total_payments']
        primitive_repr['Average Medicare Payments'] = '${:,.2f}'.format(primitive_repr['avg_medicare_payments'])
        del primitive_repr['avg_medicare_payments']
        primitive_repr['Total Discharges'] = primitive_repr['total_discharges']
        del primitive_repr['total_discharges']
        primitive_repr['Hospital Referral Region Description'] = primitive_repr['provider']['region_description']
        primitive_repr['Provider Zip Code'] = primitive_repr['provider']['zip_code']        
        primitive_repr['Provider State'] = primitive_repr['provider']['state']
        primitive_repr['Provider City'] = primitive_repr['provider']['city']
        primitive_repr['Provider Street Address'] = primitive_repr['provider']['street_address']
        primitive_repr['Provider Name'] = primitive_repr['provider']['name']
        del primitive_repr['provider']

        return primitive_repr