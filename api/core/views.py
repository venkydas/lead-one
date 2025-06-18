
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task, ClientProfile, VolunteerProfile, PaymentHistory
from .serializers import TaskSerializer, ClientProfileSerializer, VolunteerProfileSerializer, PaymentHistorySerializer

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [IsAdmin()]
#         return [permissions.IsAuthenticated()]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.user.role == 'ADMIN':
          return [permissions.IsAuthenticated()]
        
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        
        if self.action in ['list', 'retrieve', 'update', 'partial_update'] and self.request.user.role == 'VOLUNTEER':
            return [permissions.IsAuthenticated()]

        raise PermissionDenied("Not allowed.")


    def get_queryset(self):
        user = self.request.user
        if user.role == 'VOLUNTEER':
            # Volunteers can see all tasks
            return Task.objects.all()
        elif user.role == 'CLIENT':
            # Clients see only their own tasks
            return Task.objects.filter(client__user=user)
        return super().get_queryset()

    def perform_update(self, serializer):
        # If volunteer is updating, only allow status update for assigned tasks
        user = self.request.user
        instance = self.get_object()
        if user.role == 'VOLUNTEER':
            if instance.assigned_to.user != user:
                raise PermissionDenied("Not allowed.")
            serializer.save()
        else:
            serializer.save()

# core/views.py

# from rest_framework import viewsets, permissions
# from .models import ClientProfile, VolunteerProfile, PaymentHistory, Task
# from .serializers import (
#     ClientProfileSerializer, VolunteerProfileSerializer,
#     PaymentHistorySerializer, TaskSerializer
# )
# from .permissions import IsAdmin, IsVolunteer, IsClient

class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer

    def get_permissions(self):
        # Only admin can create/update; client can view their own
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'CLIENT':
    #         return ClientProfile.objects.filter(user=user)
    #     return super().get_queryset()
    def get_queryset(self):
        user = self.request.user
        base_query = ClientProfile.objects.prefetch_related('paymenthistory_set', 'task_set')
        if user.role == 'CLIENT':
            return base_query.filter(user=user)
        return base_query


    # def retrieve(self, request, *args, **kwargs): the issue is resolved here because of the filter ClientProfile.objects.filter(user=user)
    #     instance = self.get_object()
    #     if request.user.role == 'CLIENT' and instance.user != request.user:
    #         return Response({'detail': 'Not authorized.'}, status=403)
    #     return super().retrieve(request, *args, **kwargs)


class VolunteerProfileViewSet(viewsets.ModelViewSet):
    queryset = VolunteerProfile.objects.all()
    serializer_class = VolunteerProfileSerializer

    def get_permissions(self):
        # Only admin can create; volunteers can view/update their own
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]
        if self.action in ['update', 'partial_update']:
            # Allow volunteers to update their own info
            if self.request.user.role == 'VOLUNTEER':
                return [permissions.IsAuthenticated()]
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'VOLUNTEER':
            return VolunteerProfile.objects.filter(user=user)
        return super().get_queryset()

class PaymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            client_profile = ClientProfile.objects.get(user=user)
            return PaymentHistory.objects.select_related('client').filter(client=client_profile)
        # Optimized with select_related for admin or other roles
        return PaymentHistory.objects.select_related('client').all()
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'CLIENT':
    #         client_profile = ClientProfile.objects.get(user=user)
    #         return PaymentHistory.objects.filter(client=client_profile)
    #     return super().get_queryset()
