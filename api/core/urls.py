from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ClientProfileViewSet, VolunteerProfileViewSet, PaymentHistoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'clients', ClientProfileViewSet)
router.register(r'volunteers', VolunteerProfileViewSet)
router.register(r'payments', PaymentHistoryViewSet)

urlpatterns = router.urls


