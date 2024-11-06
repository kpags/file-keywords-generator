from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import FileSerializer
from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

class FileAPIView(APIView):
    permission_classes = []
    serializer_class = FileSerializer
    
    def post(self, request):
        data = request.data
        
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data["file"]
        
        reader = PdfReader(file)
        
        total_pages = len(reader.pages)
        
        most_used_words = []
        
        for i in range(0, total_pages):
            print(f"Reading Page #{i+1} of {str(file)}...")
            page = reader.pages[i]
            text = page.extract_text()
        
            words = word_tokenize(text.lower())        
            stop_words = set(stopwords.words('english'))
            
            filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
            pos_tagged_words = pos_tag(filtered_words)
            relevant_words = [word for word, pos in pos_tagged_words if pos.startswith('NN') or pos.startswith('JJ')]
            
            unique_relevant_words = list(set(relevant_words))
            freq_dist = FreqDist(unique_relevant_words)
            most_common_words = freq_dist.most_common(10)

            for word, frequencies in most_common_words:
                most_used_words.append(
                    {
                        "frequencies": frequencies,
                        "word": word,
                    }
                )
                
        
        top_10_words = sorted(most_used_words, key=lambda x: x['frequencies'], reverse=True)[:10]
        top_10_words_list = [entry['word'] for entry in top_10_words]
        
        return Response({"file": str(file), "keywords": top_10_words_list}, status=status.HTTP_200_OK)