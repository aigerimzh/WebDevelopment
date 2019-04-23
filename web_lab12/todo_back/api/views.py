from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import TaskList, Task
from django.http import JsonResponse
from .serializers import TaskListSerializer, TaskModelSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

@csrf_exempt
def tasklist_list(request):
	if request.method == 'GET':
		task_lists = TaskList.objects.all()
		serializer = TaskListSerializer(task_lists, many=True)
		return JsonResponse(serializer.data, safe=False, status=200)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = TaskListSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
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

@csrf_exempt
def tasklist_detail(request, pk):
	try:
		task_lists = TaskList.objects.get(id=pk)
	except TaskList.DoesNotExist as e:
		return JsonResponse({'error': str(e)})

	if request.method == 'GET':
		serializer = TaskListSerializer(task_lists)
		return JsonResponse(serializer.data, status=200)
	elif request.method == 'PUT':
		#data = json.loads(request.body)
		data = JSONParser().parse(request)
		serializer = TaskListSerializer(task_lists, data=data)
		if serializer.is_valid():
			serializer.save() # update function in serializer class
			return JsonResponse(serializer.data, status=200)
		return JsonResponse(serializer.errors)
	elif request.method == 'DELETE':
		task_lists.delete()
		return JsonResponse({}, status=204)


@csrf_exempt
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

