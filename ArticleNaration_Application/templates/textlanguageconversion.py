import requests
import json
import re

class OllamaChat:
    def __init__(self, base_url="http://localhost:11434/api/chat", model=None):
        """
        Initializes the OllamaChat class with the API base URL and model name.
        """
        self.base_url = base_url
        self.model = model

    def translate_text(self, text, language):
        """
        Translates the input text to the specified language using Ollama.

        Args:
            text (str): The input text to translate.
            language (str): The target language (e.g., 'English', 'Hindi', 'Tamil').

        Returns:
            str: The translated text.
        """
        new_prompt = f"Translate the text: {text} to {language}"
        response = self.send_message(new_prompt)
        return self._extract_translated_text(response, language)

    def send_message(self, prompt):
        """
        Sends a message to the Ollama API and retrieves the response.

        Args:
            prompt (str): The user input text.

        Returns:
            str: The full response from Ollama.
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.base_url, json=payload, stream=True)
        if response.status_code == 200:
            return self._extract_response_text(response)
        else:
            return f"Error {response.status_code}: {response.text}"

    def _extract_response_text(self, response):
        """
        Extracts and concatenates the assistant's response.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            str: The extracted response text.
        """
        response_text = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        response_text += json_data["message"]["content"] + " "
                except json.JSONDecodeError:
                    continue  # Ignore malformed JSON lines

        return response_text.strip()  # Remove extra spaces or newlines

    def _extract_translated_text(self, response_text, language):
        """
        Extracts only the translated text from the response.

        Args:
            response_text (str): The full response text.
            language (str): The target language for translation.

        Returns:
            str: The extracted translated text.
        """
        # Search for the phrase "Translated to {language}:" and extract only that part
        pattern = rf"Translated to {language}:(.*)"
        match = re.search(pattern, response_text, re.IGNORECASE)

        if match:
            return match.group(1).strip()  # Extract only the translated text
        return response_text  # If no match is found, return the full response


# # Example usage:
# if __name__ == "__main__":
#     ollama_chat = OllamaChat(model="mistral")  # Replace with your preferred model
#     user_input = "Hello, how are you?"
#     target_language = "Hindi"
    
#     translated_text = ollama_chat.translate_text(user_input, target_language)
#     print(f"Translated Text to {target_language}:", translated_text)
