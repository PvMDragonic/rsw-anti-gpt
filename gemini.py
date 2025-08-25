from decouple import config, UndefinedValueError
from google.genai import errors
from google import genai

class Gemini:
    MODEL = 'gemini-2.5-flash' 

    def __init__(self):
        try:
            api_key = config("GOOGLE_API_KEY")
            self.client = genai.Client(api_key = api_key)
        except UndefinedValueError:
            print("Error: GOOGLE_API_KEY not found. Make sure it's set in your .env file or environment.")

    def translate(self, title: str, text: str) -> str:
        try:
            return self.client.models.generate_content(
                model = self.MODEL,
                contents = f"""
                    Traduz o código-fonte desse artigo da RuneScape Wiki pra Português:

                    {text}
                """
            ).text
        except errors.APIError as e:
            print(f"Error on {title}: {e}")