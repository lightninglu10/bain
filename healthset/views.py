from rest_framework import viewsets
from rest_framework.response import Response
from .models import Inpatient
from .serializers import InpatientSerializer
from django.core.paginator import Paginator
from django import forms
# import settings
import sys
from rest_framework import mixins

class InpatientForm(forms.Form):
    max_discharges = forms.IntegerField(required=False, initial=sys.maxsize)
    min_discharges = forms.IntegerField(required=False, initial=0)
    max_average_covered_charges = forms.FloatField(required=False, initial=sys.maxsize)
    min_average_covered_charges = forms.FloatField(required=False, initial=0)
    min_average_medicare_payments = forms.FloatField(required=False, initial=0)
    max_average_medicare_payments = forms.FloatField(required=False, initial=sys.maxsize)
    state = forms.CharField(max_length=3, required=False, initial='')

    def clean(self):
        cleaned_data = super(InpatientForm, self).clean()
        # if data is not provided for some fields and those fields have an
        # initial value, then set the values to initial value
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data

class InpatientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Simple viewset to retrieve an inpatient list
    """
    queryset = Inpatient.objects.all()
    serializer_class = InpatientSerializer

    def list(self, request, *args, **kwargs):
        request_filters = InpatientForm(request.GET)
        if request_filters.is_valid():
            request_data = request_filters.cleaned_data
            max_discharges = request_data.get('max_discharges')
            min_discharges = request_data.get('min_discharges')
            
            # Multiply these values by 100 because we are representing the number in cents.
            max_avg_covered_charges = request_data.get('max_average_covered_charges')
            if max_avg_covered_charges != sys.maxsize:
                max_avg_covered_charges *= 100

            min_avg_covered_charges = request_data.get('min_average_covered_charges')
            if min_avg_covered_charges != 0:
                min_avg_covered_charges *= 100
            
            min_avg_medicare_payments = request_data.get('min_average_medicare_payments')
            if min_avg_medicare_payments != 0:
                min_avg_medicare_payments *= 100
            
            max_avg_medicare_payments = request_data.get('max_average_medicare_payments')
            if max_avg_medicare_payments != sys.maxsize:
                max_avg_medicare_payments *= 100
    
            # NOTE: this will error if any of these values are greater than sys.maxsize
            
            state = request_data.get('state', '')

            if state:
                inpatients = Inpatient.objects.filter(
                    total_discharges__lte=max_discharges,
                    total_discharges__gte=min_discharges,
                    avg_covered_charges__lte=max_avg_covered_charges,
                    avg_covered_charges__gte=min_avg_covered_charges,
                    avg_medicare_payments__lte=max_avg_medicare_payments,
                    avg_medicare_payments__gte=min_avg_medicare_payments,
                    provider__state=state,
                )
            else:
                inpatients = Inpatient.objects.filter(
                    total_discharges__lte=max_discharges,
                    total_discharges__gte=min_discharges,
                    avg_covered_charges__lte=max_avg_covered_charges,
                    avg_covered_charges__gte=min_avg_covered_charges,
                    avg_medicare_payments__lte=max_avg_medicare_payments,
                    avg_medicare_payments__gte=min_avg_medicare_payments,
                )

            page = self.paginate_queryset(inpatients)
            if page is not None:
                paginated_inpatient_data = InpatientSerializer(page, many=True).data
                return self.get_paginated_response(paginated_inpatient_data)

            inpatient_data = InpatientSerializer(inpatients, many=True).data
            return Response(inpatient_data)
        return Response(request_filters.errors, status=400)
