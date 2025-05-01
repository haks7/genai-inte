import openai
import os

import requests
# In this case i cannot use the AIProjectClient
# as I cannot implement only sentiment analysis as I cannot attache message(data)) 
# or ground data as its expensive) 

# Azure AI Services configuration
ai_services_endpoint = os.getenv("AZURE_AI_SERVICES_ENDPOINT")
ai_services_key = os.getenv("AZURE_AI_SERVICES_KEY")

class AzureAITextAgent:
    def __init__(self, source):
        self.source = source

    def analyze_text(self, text):
        """Analyze text using Azure AI Services."""
        url = f"{ai_services_endpoint}/text/analytics/v3.1/sentiment"
        headers = {
            "Ocp-Apim-Subscription-Key": ai_services_key,
            "Content-Type": "application/json"
        }
        payload = {
            "documents": [
                {"id": "1", "language": "en", "text": text}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            sentiment_data = result["documents"][0]

            # Extract sentiment and confidence scores
            sentiment = sentiment_data["sentiment"]
            confidence_scores = sentiment_data["confidenceScores"]

            # Generate a statement based on the sentiment and confidence scores
            if sentiment == "positive":
                statement = f"The sentiment is positive with a confidence score of {confidence_scores['positive']:.2f}. Glad to hear that!"
            elif sentiment == "neutral":
                statement = f"The sentiment is neutral with a confidence score of {confidence_scores['neutral']:.2f}. Seems like you're feeling okay."
            elif sentiment == "negative":
                statement = f"The sentiment is negative with a confidence score of {confidence_scores['negative']:.2f}. Sorry to hear that."
            else:
                statement = "The sentiment could not be determined."

            return {
                "sentiment": sentiment,
                "confidenceScores": confidence_scores,
                "statement": statement
            }
        except Exception as e:
            print(f"Error using Azure AI Services: {e}")
            return None
        

# Use AIProjectClient When:
    # You need to manage workflows involving multiple AI agents.
    # You want to attach additional data (e.g., weather data) to prompts for context-aware decision-making.
    # You are working with Foundry AI or other project-based Azure AI services.
# Use REST API for Text Analytics When:
    # You need to perform specific text analysis tasks, such as sentiment analysis or key phrase extraction.
    # You want a lightweight and straightforward integration for analyzing text.
    # You do not need to manage threads or workflows.

# 1. Speech Analysis
# Azure Speech Services allow you to:

#     a. Speech-to-Text: Convert spoken audio to text.
#     b. Text-to-Speech: Convert text to spoken audio.
#     c. Speech Translation: Translate spoken audio into another language.
#     d. Speaker Recognition: Identify or verify speakers based on their voice.

# 2. Text Analysis
# Azure Text Analytics provides the following capabilities:

#     a. Sentiment Analysis: Determine the sentiment of text (positive, neutral, or negative).
#     b. Key Phrase Extraction: Extract important phrases from text.
#     c. Named Entity Recognition (NER): Identify entities like names, locations, dates, and organizations in text.
#     d. Language Detection: Detect the language of the text.
#     e. PII Detection: Identify and redact Personally Identifiable Information (PII) in text.
#     f. Opinion Mining: Analyze opinions and relationships between aspects of text (e.g., "The food was great, but the service was slow.").

# 3. Vision Analysis
# Azure Computer Vision provides the following capabilities:

#     a. Image Analysis: Extract information from images, such as objects, faces, and text.
#     b. OCR (Optical Character Recognition): Extract text from images or scanned documents.
#     c. Face Detection: Detect and analyze faces in images.
#     d. Form Recognizer: Extract structured data from forms and invoices.
#     e. Custom Vision: Train custom models to classify images or detect objects.

# 4. Decision Analysis
# Azure Decision Services include:

#     a. Personalizer: Deliver personalized content and experiences to users.
#     b. Anomaly Detector: Detect anomalies in time-series data.
#     c. Content Moderator: Moderate text, images, and videos for offensive or inappropriate content.

# 5. Combining Speech and Text Analysis
# You can combine speech and text analysis to build advanced workflows:

#     a. Speech-to-Text: Convert spoken audio to text.
#     b. Text Analysis: Perform sentiment analysis, key phrase extraction, or entity recognition on the transcribed text.
#     c. Text-to-Speech: Convert the analyzed text back to spoken audio.

# 6. Other Cognitive Services
#     a. Translator: Translate text into multiple languages.
#     b. QnA Maker: Build question-and-answer bots using knowledge bases.
#     d. Azure OpenAI: Use advanced language models like GPT for text generation and reasoning.