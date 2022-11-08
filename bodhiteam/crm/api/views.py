from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from membership.models import *
from crm.models import *
from .serializers import *


# Create your views here.
class Converted_by_list(APIView):
    def get(self, request):
        queryset = SalesExecutive.objects.all()
        serializer = SalesExecutiveBasicDetails(queryset, many=True)
        context = {
            'status': "success",
            'message': serializer.data
        }

        return Response(context)


class CreateInstitute(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = InstituteCreateSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            context = {
                'status': "success",
                'message': "successfully created"
            }
        except Exception as e:
            context = {
                'status': "Failed",
                'message': f"{e}"
            }

        return Response(context)


class GetInstituteDetailAPI(APIView):
    def post(self, request):
        data = request.data
        institute = Institute.objects \
            .prefetch_related('status') \
            .prefetch_related('update_requirements') \
            .prefetch_related('update_requirements__status') \
            .filter(id=data['id']) \
            .first()
        serializer = InstituteDetailsSerializer(institute)

        context = {
            'status': "success",
            'message': serializer.data
        }

        return Response(context)


class GetInstituteAPI(APIView):
    def get(self, request):
        queryset = Institute.objects \
            .all() \
            .order_by('-id')
        serializer = GetAllInstituteSerializer(queryset, many=True)
        context = {
            'status': 'Success',
            'message': serializer.data
        }

        return Response(context)


class UpdateInstitute(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data)
            institute = Institute.objects.get(id=data['institute_id'])
            serializer = InstituteUpdateSerializer(
                instance=institute, data=data, partial=True)
            serializer.is_valid()
            print(serializer.validated_data)
            serializer.save()
            context = {
                'status': 'success',
                'message': serializer.data,
            }
        except Exception as e:
            print(e)
            context = {
                'status': 'Failed',
                'message': f'{e}',
            }
        return Response(context)


class InstituteStatusAPI(APIView):
    def get(self, request):
        queryset = InstituteStatus.objects.all()
        serializers = InstituteStatusSerializer(queryset, many=True)
        context = {
            "status": 'success',
            "message": serializers.data
        }
        return Response(context)


class InstituteRequirementsStatusAPI(APIView):
    def get(self, request):
        queryset = UpdateRequirementsStatus.objects.all()
        serializers = UpdateRequirementsStatusSerializer(queryset, many=True)
        context = {
            "status": 'success',
            "message": serializers.data
        }
        return Response(context)


class CreateInstituteRequirementsAPI(APIView):
    def post(self, request):
        try:
            data = request.data.dict()
            serializer = InstituteRequirementsSerializer(
                data=data, context={'institute': data['institute']})
            serializer.is_valid()
            print(serializer.validated_data)
            serializer.save()
            context = {
                "status": 'success',
                "message": serializer.data
            }
        except Exception as e:
            context = {
                "status": 'Failed',
                "message": f"{e}"
            }
        return Response(context)
