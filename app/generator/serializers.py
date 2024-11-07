from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate(self, attrs):
        file = attrs.get('file', None)
        
        if file is None:
            raise ValidationError({"message": "PDF File is missing."})
        
        if "pdf" not in str(file):
            raise ValidationError({"message": "Only PDF files are accepted."})
        
        return super().validate(attrs)