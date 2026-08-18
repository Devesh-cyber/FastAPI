import base64
import json
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CROP_ANALYSIS_PROMPT = """
    You are an expert agricultural scientist specializing in crop disease detection.
Analyze this image of a crop/plant and provide a detailed disease assessment.

Provide your analysis as a JSON object with exactly this structure:

{
"crop_detected": "Name of the crop or plant visible in the image",
"severity": "healthy" or "mild" or "moderate" or "severe" or "critical",
"diseases": [
        {
            "name": "Disease name",
            "confidence": 0.0 to 1.0,
            "description": "Brief description of the disease and visible symptoms"
        }
    ],
"treatments": [
        {
            "treatment_name": "Name of treatment",
            "treatment_type": "organic" or "chemical" or "preventive",
            "instructions": "Step by step treatment instructions",
            "urgency": "immediate" or "within_week" or "seasonal"
        }
    ],
    "overall_health": "One sentence summary of plant health",
    "additional_notes": "Any other observations or recommendations"
}
"""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()


async def analyse_image(image_path: str, content_type: str):
    """
    Analyse the image content using Google GenAI for disease detection.
    """

    base64_image = encode_image(image_path)

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=[
            {"type": "text", "text": CROP_ANALYSIS_PROMPT},
            {
                "type": "image",
                "data": base64.b64encode(base64_image).decode('utf-8'),
                "mime_type": "image/jpeg"
            }
        ]
    )

    output = interaction.output_text.strip()

    if output.startswith("```json"):
        output = output[7:]

    if output.endswith("```"):
        output = output[:-3]

    output = output.strip()

    return json.loads(output)
        
   