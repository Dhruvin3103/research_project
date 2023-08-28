from rest_framework import serializers

from .models import UserMessage

import joblib
import pickle
model_path = 'model/voting_classifier_model.pkl'

def model_predict(text):
    with open('model/tfidf_vectorizer.pkl', 'rb') as file:
        tf1 = pickle.load(file)
    message = [text]
    print('going to vectorized')
    vectorized = tf1.transform(message).toarray()
    voting_classifier = joblib.load(model_path)
    prediction = voting_classifier.predict(vectorized)
    print(prediction)
    return prediction

class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['message']
        
    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        predictions = model_predict(validated_data['message'])
        print(predictions)
        if predictions == 1:
            validated_data['is_stressed'] = True
        elif predictions==0:
            validated_data['is_stressed'] = False
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        data['is_stressed'] = instance.is_stressed
        return data