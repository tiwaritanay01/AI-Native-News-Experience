import os
from app.services.hardware_engine import get_hardware_type, get_engine

class TranslationService:
    def __init__(self):
        # We prefer Gemini for translation as it has excellent vernacular support
        pass

    def translate(self, text: str, target_lang: str) -> str:
        """
        Translates text to a vernacular language like Hindi, Marathi, 
        Bengali, etc. using Gemini or the active LLM with Cultural Adaptation.
        """
        prompt = f"""
        Translate the following news text into {target_lang}.
        
        CRITICAL INSTRUCTIONS:
        1. CULTURAL ADAPTATION: Do not translate literally. Use local idioms, business terminology (e.g., 'Samvat' context for markets if applicable), and simplify complex financial jargon into analogies understood by local audiences.
        2. CONTEXT AWARENESS: Maintain the professional urgency of ET (Economic Times) but make it accessible.
        3. FORMATTING: Use clear, readable paragraphs.
        
        Text to translate:
        {text}
        """
                 
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
