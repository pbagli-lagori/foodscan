import base64
import vertexai
import json
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

inputprompt = """You are given an image containing multiple food products. Your task is to extract the text associated with each product, such as product name and its contents. 
The output should be in the following format:
[
  {
    "product name": "Name of the product", 
    "content": {
      "content name": "value"
    }
  },
  {
    "product name": "Name of the product", 
    "content": {
      "content name": "value"
    }
  }
  ...
]

Here are some instructions:
- Each food product might have multiple contents (like ingredients, nutritional information, etc.), so ensure you capture all available text.
- Structure the information under "content" for each product clearly.
- If a content name or value is missing, exclude that field for the product.
- Present each product separately in a list format, even if multiple products share common contents."""

def generate(image, generation_config, safety_settings ):
    vertexai.init(project="sgtest-414906", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    print("generating content")
    responses = model.generate_content(
        [image, """Read the text in this image."""],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    print("content generated")
    return responses


def parse_text(text, generation_config, safety_settings):
    vertexai.init(project="sgtest-414906", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    responses = model.generate_content(
        [text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    return responses

def llm_generate(image):
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

    responses = generate(image, generation_config, safety_settings)
    # parsed_text = parse_text(responses, generation_config, safety_settings)
    results=[]
    # print(json.dumps(responses))
    print("length of responses")
    print(len(responses))
    for data in responses:
        print(data.text, end="")
        results.append(data.text)
    
    return results