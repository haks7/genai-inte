import requests
import os

class AzureCognitiveTextAgent:
    def __init__(self, source):
        self.source = source
        self.endpoint = os.getenv("AZURE_AI_SERVICES_ENDPOINT") + "/text/analytics/v3.1/keyPhrases"
        self.key = os.getenv("AZURE_AI_SERVICES_KEY")

    def extract_key_phrases(self, text):
        """Extract key phrases using Azure Text Analytics REST API."""
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json"
        }
        payload = {
            "documents": [
                {"id": "1", "language": "en", "text": text}
            ]
        }
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["documents"][0]["keyPhrases"]
        except Exception as e:
            print(f"Error extracting key phrases: {e}")
            return []
        
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