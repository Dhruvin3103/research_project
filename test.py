import joblib
import pickle

model_path = 'model/voting_classifier_model.pkl'
with open('model/tfidf_vectorizer.pkl', 'rb') as file:
    tf1 = pickle.load(file)

message = ["hi i am sad "]
# message = [message]

print('going to vectorized')
# Transform the message using the TF-IDF vectorizer
vectorized = tf1.transform(message).toarray()

# Load the saved voting classifier model
voting_classifier = joblib.load(model_path)

# print(vectorized)
# Make a prediction using the vectorized message
prediction = voting_classifier.predict(vectorized)

print(prediction)
