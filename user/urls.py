from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')

# Initialize a nested router for prescriptions under patients
patients_router = NestedDefaultRouter(router, r'patients', lookup='patient')
patients_router.register(r'prescriptions', PrescriptionViewSet, basename='patient-prescriptions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(patients_router.urls)), 
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
