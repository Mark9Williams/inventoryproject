from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Prescription
from .serializers import CustomTokenObtainPairSerializer, PatientSerializer, PrescriptionSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
        else:
            print(serializer.errors)  # Log errors for debugging
            raise ValidationError(serializer.errors)

    @action(detail=False, methods=["get"], url_path="fetch-patients", url_name="fetch_patients")
    def fetch_patients(self, request):
        """
        Custom endpoint to fetch registered patients.
        """
        patients = self.queryset  # Retrieve all patients
        serializer = self.get_serializer(patients, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        # Check if the request is for a specific patient's prescriptions
        patient_id = self.kwargs.get('patient_pk')  # Get the nested patient ID
        if patient_id:
            return Prescription.objects.filter(patient_id=patient_id)
        return super().get_queryset()

    # Custom action to get prescriptions by patient ID
    @action(detail=True, methods=['get'])
    def patient_prescriptions(self, request, pk=None):
        patient = self.get_object()
        prescriptions = patient.prescriptions.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

    # Optionally add a method to create a prescription
    @action(detail=True, methods=['post'])
    def add_prescription(self, request, pk=None):
        patient = self.get_object()
        data = request.data
        serializer = PrescriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(patient=patient)  # Assign the patient to the prescription
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)