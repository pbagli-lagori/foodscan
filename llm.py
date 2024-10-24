import base64
import vertexai
import json
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

def extract_text_from_image(image, generation_config, safety_settings ):
    vertexai.init(project="sgtest-414906", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    print("Generating content...")
    responses = model.generate_content(
        [image, """Read the text in this image."""],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    # print(responses.text)
    prompt = f"""Based on the nutrition label data presented here - {responses.text}, provide a summary  information in a markdown format"""
    # print(prompt)
    responses = model.generate_content(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    print(responses.text)
    print("Content generated.")
    return responses.text

def llm_process(image):
    image = Part.from_data(
        mime_type="image/jpeg",
        data=image,
    )
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
    ]

    extracted_text = extract_text_from_image(image, generation_config, safety_settings)
    
    return extracted_text