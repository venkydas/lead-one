from rest_framework import serializers
from api.users.models import User
from .models import ClientProfile, VolunteerProfile, PaymentHistory, Task
from api.users.serializers import UserSerializer, UserCreateSerializer




# class PaymentHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentHistory
#         fields = ['id', 'date', 'amount_paid']

# class ClientProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     payment_history = PaymentHistorySerializer(source='paymenthistory_set', many=True, read_only=True)
#     amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     due_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
#     class Meta:
#         model = ClientProfile
#         fields = [
#             'id', 'user', 'party_name', 'total_amount', 'joined_date',
#             'amount_paid', 'due_amount', 'payment_history',
#         ]

# class VolunteerProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = VolunteerProfile
#         fields = ['id', 'user', 'skills', 'joined_date']

# class ClientProfileSerializer(serializers.ModelSerializer):
#     user = UserCreateSerializer()
#     amount_paid = serializers.SerializerMethodField()
#     due_amount = serializers.SerializerMethodField()

#     class Meta:
#         model = ClientProfile
#         fields = [
#             'id', 'user', 'party_name', 'total_amount', 'joined_date', 'amount_paid', 'due_amount'
#         ]
#         read_only_fields = ['id', 'joined_date']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(
#             email=user_data['email'],
#             name=user_data['name'],
#             role='CLIENT',
#             password='goated'  # Or use a more secure generation!
#         )
#         client_profile = ClientProfile.objects.create(user=user, **validated_data)
#         return client_profile

#     def get_amount_paid(self, obj):
#         return obj.amount_paid

#     def get_due_amount(self, obj):
#         return obj.due_amount
    




class VolunteerProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = VolunteerProfile
        fields = [
            'id', 'user', 'skills', 'joined_date'
        ]
        read_only_fields = ['id', 'joined_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            email=user_data['email'],
            name=user_data['name'],
            role='VOLUNTEER',
            password='goated'
        )
        volunteer_profile = VolunteerProfile.objects.create(user=user, **validated_data)
        return volunteer_profile


class TaskSerializer(serializers.ModelSerializer):
    # Accept IDs for POST/PATCH, show nested info for GET
    client = serializers.PrimaryKeyRelatedField(
        queryset=ClientProfile.objects.all()
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=VolunteerProfile.objects.all()
    )

    # client_detail = ClientProfileSerializer(source='client', read_only=True)
    # assigned_to_detail = VolunteerProfileSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description',
            'client', 'assigned_to',
            'status', 'created_on',
            # 'client_detail', 'assigned_to_detail'
        ]
        read_only_fields = ['id', 'created_on', 'client_detail', 'assigned_to_detail']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Include nested info for GET
        # rep['client'] = rep.pop('client_detail')
        # rep['assigned_to'] = rep.pop('assigned_to_detail')
        return rep

class PaymentHistorySerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=ClientProfile.objects.all())
    client_name = serializers.CharField(source='client.user.name', read_only=True)

    class Meta:
        model = PaymentHistory
        fields = ['id', 'client', 'client_name', 'date', 'amount_paid']
        read_only_fields = ['client_name', 'date']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            client_profile = ClientProfile.objects.get(user=user)
            return PaymentHistory.objects.select_related('client__user').filter(client=client_profile)
        return PaymentHistory.objects.select_related('client__user').all()

class PaymentHistorySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'date', 'amount_paid']

class TaskSummarySerializer(serializers.ModelSerializer):
    assigned_date = serializers.DateField(source='created_on')

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'assigned_date']

class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    amount_paid = serializers.SerializerMethodField()
    due_amount = serializers.SerializerMethodField()
    payment_history = PaymentHistorySummarySerializer(source='paymenthistory_set', many=True, read_only=True)
    tasks = TaskSummarySerializer(source='task_set', many=True, read_only=True)

    class Meta:
        model = ClientProfile
        fields = [
            'id', 'user', 'party_name', 'total_amount', 'joined_date',
            'amount_paid', 'due_amount','tasks', 'payment_history'
        ]
        read_only_fields = ['id', 'joined_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            email=user_data['email'],
            name=user_data['name'],
            role='CLIENT',
            password='goated'
        )
        client_profile = ClientProfile.objects.create(user=user, **validated_data)
        return client_profile

    def get_amount_paid(self, obj):
        return obj.amount_paid

    def get_due_amount(self, obj):
        return obj.due_amount

