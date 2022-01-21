from django.shortcuts import render, get_object_or_404
from rest_framework import status
from toysModel.models import ToyModel
from toysModel.serializers import ToySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
	
@api_view(['GET', 'POST'])
def toyM_list(request):
	if request.method == 'GET':
		toys = ToyModel.objects.all()
		toys_serializer = ToySerializer(toys, many=True)
		return Response(toys_serializer.data)
	
	elif request.method == 'POST':
		toy_serializer = ToySerializer(data=request.data)  # generando un nuevo objeto
		if toy_serializer.is_valid():
			toy_serializer.save()
			return Response(toy_serializer.data,\
				status= status.HTTP_201_CREATED)
		
		return Response(toy_serializer.errors, \
			status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def toyM_detail(request, pk):

	toy = get_object_or_404(ToyModel, pk=pk)  # usando metodo abreviado.

	if request.method == 'GET':
		toy_serializer = ToySerializer(toy)
		return Response(toy_serializer.data)
	
	elif request.method == 'PUT':
		toy_serializer = ToySerializer(toy, data=request.data) # actualizando un objeto
		if toy_serializer.is_valid():
			toy_serializer.save()
			return Response(toy_serializer.data)
		return Response(toy_serializer.errors, \
			status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		toy.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
