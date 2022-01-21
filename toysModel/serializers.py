from rest_framework import serializers
from toysModel.models import ToyModel

class ToySerializer(serializers.ModelSerializer):
	class Meta:
		model = ToyModel
		fields = ( 'id',
				'name',
				'description',
				'release_date',
				'toy_category',
				'was_included_in_home')

