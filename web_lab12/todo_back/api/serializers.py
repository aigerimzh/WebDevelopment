from rest_framework import serializers
from api.models import TaskList, Task



class TaskListSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(max_length=255)

	def create(self, validated_data):
		task_list = TaskList(**validated_data)
		task_list.save()
		return task_list
		

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.save()
		return instance

class TaskModelSerializer(serializers.ModelSerializer):
	task_list = TaskListSerializer
	class Meta:
		model = Task
		fields = ('id', 'name', 'created_at', 'due_on', 'status', 'task_list')