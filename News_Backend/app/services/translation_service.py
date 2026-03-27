import os
from app.services.hardware_engine import get_hardware_type, get_engine

class TranslationService:
    def __init__(self):
        # We prefer Gemini for translation as it has excellent vernacular support
        pass

    def translate(self, text: str, target_lang: str) -> str:
        """
        Translates text to a vernacular language like Hindi, Marathi, 
        Bengali, etc. using Gemini or the active LLM.
        """
        prompt = f"Translate the following news into {target_lang} while maintaining " \
                 f"the professional and engaging tone:\n\n{text}"
                 
        hw = get_hardware_type()
        
        if hw == "GEMINI":
            try:
                model = get_engine()["model"]
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"❌ Gemini translation error: {e}")
                return self._mock_translation(text, target_lang)
        
        # Fallback to general LLM or Mock
        from app.services.llm_service import generate_llm_response
        return generate_llm_response(prompt)

    def _mock_translation(self, text: str, target_lang: str):
        # Simple placeholder if no model is available
        return f"[Translation to {target_lang} for]: {text[:50]}..."

translation_service = TranslationService()
