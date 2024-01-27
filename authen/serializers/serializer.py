from rest_framework import serializers
from authen.models import Country, Gender


class CountrySerilaizers(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = '__all__'


class GenderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'