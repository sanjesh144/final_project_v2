import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyse } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(url, json=myobj, headers=header)
    
    # Check if the request was successful (status code 200) before parsing the response.
    if response.status_code == 200:
        # Parse the response text into a dictionary.
        response_dict = json.loads(response.text)
        
        # Extract emotion predictions.
        emotion_predictions = response_dict.get("emotionPredictions", [])
        
        if emotion_predictions:
            # Assuming there's only one prediction in the list (you may need to iterate if there are multiple predictions).
            prediction = emotion_predictions[0]
            
            # Extract emotions and their scores.
            emotions = prediction.get("emotion", {})
            
            # Find the dominant emotion with the highest score.
            dominant_emotion = max(emotions, key=emotions.get)
            dominant_score = emotions[dominant_emotion]
            
            # Prepare the result in the desired format.
            result = {
                "anger": emotions.get("anger", 0.0),
                "disgust": emotions.get("disgust", 0.0),
                "fear": emotions.get("fear", 0.0),
                "joy": emotions.get("joy", 0.0),
                "sadness": emotions.get("sadness", 0.0),
                "dominant_emotion": dominant_emotion
            }
            
            return result
        else:
            return {"error": "Emotion predictions not found in the response."}
    else:
        return {"error": f"Error occurred. Status code: {response.status_code}, Response: {response.text}"}