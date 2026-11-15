from rest_framework import serializers
from django.contrib.auth.models import User
from EventApp.models import EventDb,EventMemberDb

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id","username","email","password"]
        read_only_fields =["id"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class EventSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventDb
        fields = '__all__'
        read_only_fields = ['id','created_by','created_at','updated_at']


class EventmemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    member_username = serializers.CharField(source='user.username',read_only=True)
    member_user_id = serializers.IntegerField(source='user.id',read_only=True)

    class Meta:
        model = EventMemberDb
        fields = ['id','username','member_username','member_user_id','joined_at']
        read_only_fields = ['id','joined_at']

    def username_valid(self,value):
        try:
            user=User.objects.get(username=value)
        except:
            if User.DoesNotExist:
                raise serializers.ValidationError("Not an registered user")
        event=self.context['event']
        if user == event.created_by:
            raise serializers.ValidationError('Event creator cannot be added as a member')
        if EventMemberDb.objects.filter(user=user,event=event).exist():
            raise serializers.ValidationError('User is already added to the event')
        return value



