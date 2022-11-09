from rest_framework import serializers
from membership.models import SalesExecutive
from crm.models import *


class SalesExecutiveBasicDetails(serializers.ModelSerializer):
    class Meta:
        model = SalesExecutive
        fields = ['id', 'name', 'typeExecutive']




class UpdateRequirementsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateRequirementsStatus
        fields = '__all__'


class InstituteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteStatus
        fields = '__all__'


class InstituteRequirementsSerializer(serializers.ModelSerializer):
    status = UpdateRequirementsStatusSerializer()

    class Meta:
        model = UpdatesRequirements
        fields = '__all__'

    def run_validation(self, data):
        data['status'] = UpdateRequirementsStatus.objects.get(
            id=data['status'])
        return data

    def create(self, validated_data):
        institute_id = self.context['institute']
        requirements = UpdatesRequirements.objects.create(
            description=validated_data['description'], status=validated_data['status'])
        requirements.save()
        institute = Institute.objects.get(id=institute_id)
        institute.update_requirements.add(requirements)
        return requirements


class GetAllInstituteSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()

    class Meta:
        model = Institute
        fields = [
            'id',
            'name',
            'phone_number',
            'status',
        ]


class InstituteDetailsSerializer(serializers.ModelSerializer):
    converted_by = SalesExecutiveBasicDetails()
    status = InstituteStatusSerializer()
    update_requirements = InstituteRequirementsSerializer(many=True)

    class Meta:
        model = Institute
        fields = '__all__'

    # def run_validation(self, data=...):
    #     if data.get('converted_by'):
    #         try:
    #             data['converted_by'] = SalesExecutive.objects.get(id=data['converted_by'])
    #         except:
    #             return serializers.ValidationError("Sales Executive does not exist")
    #     if data.get('status'):
    #         try:
    #             data['status'] = InstituteStatus.objects.filter(id=data['status']).first()
    #         except:
    #             return serializers.ValidationError("Not Define does not exist")

    #     return data

class InstituteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institute
        fields = '__all__'


class InstituteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institute
        fields = [
            'name',
            'phone_number',
            'date_of_conversion',
            'status',
            'amount_of_conversion',
            'amount_paid',
            'converted_by',
        ]

    # def update(self, instance: Institute, validated_data: dict):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.phone_number = validated_data.get('phone_number', instance.phone_number)
    #     instance.date_of_conversion = validated_data.get('date_of_conversion', instance.date_of_conversion)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.amount_of_conversion = validated_data.get('amount_of_conversion', instance.amount_of_conversion)
    #     instance.amount_paid = validated_data.get('amount_paid', instance.amount_paid)
    #     # instance.update_requirements = validated_data.get('update_requirements', instance.update_requirements)
    #     instance.converted_by = validated_data.get('converted_by',instance.converted_by)
    #     instance.save()
    #     return instance

class UpdateInstituteRequirementsSerializers(serializers.ModelSerializer):
    class Meta:
        model = UpdatesRequirements
        fields = '__all__'