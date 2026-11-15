from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from EventApp.serializers import UserSerializer,EventSerializers,EventmemberSerializer
from EventApp.models import EventDb,EventMemberDb
from rest_framework import permissions,authentication,serializers
from EventApp.permissions import OwnerOnly

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User Registered Successfully"})
        else:
            return Response(data=serializer_instance.errors)

class UsersListView(APIView):
    def get(self,request):
        user = User.objects.all()
        serializer_instance = UserSerializer(user,many=True)
        return Response(data=serializer_instance.data)

class EventCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]

    def get(self,request):
        event = EventDb.objects.filter(created_by=request.user)
        serializer_instance = EventSerializers(event,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        event=request.data
        serializer_instance=EventSerializers(data=event)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response({"Message":"Event Created",
                             "Event Details":serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)

class EventRetrieveUpdateDelete(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]

    def get(self,request,pk):
        event_object=get_object_or_404(EventDb,id=pk)
        if event_object.created_by==request.user:
            serializer_instance=EventSerializers(event_object)
            return Response(data=serializer_instance.data)
        else:
            raise serializers.ValidationError("You dont have access to this")

    def put(self,request,pk):
        event=request.data
        event_object=get_object_or_404(EventDb,id=pk)
        if event_object.created_by != request.user:
            raise serializers.ValidationError("Access denied...!")
        serializer_instance=EventSerializers(data=event,instance=event_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Event details updated successfully",
                             "Updated Event Details":serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        event_object=get_object_or_404(EventDb,id=pk)
        if event_object.created_by != request.user:
            raise serializers.ValidationError("You dont have Access")
        event_object.delete()
        return Response({"Message":"Event Have Successfully Deleted"})

    



