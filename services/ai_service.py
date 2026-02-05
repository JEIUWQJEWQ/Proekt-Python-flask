
import os

from google import genai

MODEL_NAME = "gemini-3-flash-preview"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") # овој АПИ клуч го добиваме од гемини

def generate_summary(prasanje, rezultati):
    client = genai.Client(api_key="")
    if not rezultati:
        return "Нема доволно податоци за AI резиме."

    rezultati_text = ""
    for r in rezultati:
        rezultati_text += (
            f"- {r['opcija']}: {r['glasovi']} гласови "
            f"({r['procent']}%)\n"
        )

    prompt = f"""
    Прашање на анкетата:
    {prasanje}

    Резултати од гласањето:
    {rezultati_text}

    Задача:
    Напиши кратко резиме од 2–4 реченици на македонски јазик.
    Додај 1 интересна забелешка (дали има јасен победник или резултатите се тесни).
    """


    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return (response.text or "").strip() or "Нема резултат од AI (празен текст)."
    except Exception as e:
        return f"AI грешка: {e}"

