from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from ..models import TaskList, Task
from django.http import JsonResponse
from ..serializers import TaskListSerializer, TaskModelSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class TasklistList(APIView):
	def get(self, request):
		task_lists = TaskList.objects.all()
		serializer = TaskListSerializer(task_lists, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = TaskListSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def task_list(request, pk):
	if request.method == 'GET':
		task_lists = TaskList.objects.get(id=pk)
		tasks = task_lists.task_set.all()
		serializer = TaskModelSerializer(tasks, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = TaskModelSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


class TasklistDetail(APIView):

	def get_object(self, pk):
		try:
			return TaskList.objects.get(id=pk)
		except TaskList.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		task_lists = self.get_object(pk)
		serializer = TaskListSerializer(task_lists)
		return Response(serializer.data)

	def put(self, request, pk):
		task_lists = self.get_object(pk)
		serializer = TaskListSerializer(instance= task_lists, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def delete(self, request, pk):
		task_lists = self.get_object(pk)
		task_lists.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
	try:
		tasks = Task.objects.get(id=pk)
	except Task.DoesNotExist as e:
		return JsonResponse({'error': str(e)})

	if request.method == 'GET':
		serializer = TaskModelSerializer(tasks)
		return JsonResponse(serializer.data, status=200)

	elif request.method == 'PUT':
		#data = json.loads(request.body)
		data = JSONParser().parse(request)
		serializer = TaskModelSerializer(tasks, data=data)
		if serializer.is_valid():
			serializer.save() # update function in serializer class
			return JsonResponse(serializer.data, status=200)
		return JsonResponse(serializer.errors)
	elif request.method == 'DELETE':
		tasks.delete()
		return JsonResponse({}, status=204)

