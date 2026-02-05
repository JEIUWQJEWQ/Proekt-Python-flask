# from google import genai
# import os
#
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#
#
# def generate_summary(prasanje, rezultati):
#     if not rezultati:
#         return "Нема доволно податоци за AI резиме."
#
#     rezultati_text = ""
#     for r in rezultati:
#         rezultati_text += (
#             f"- {r['opcija']}: {r['glasovi']} гласови "
#             f"({r['procent']}%)\n"
#         )
#
#     prompt = f"""
#     Прашање на анкетата:
#     {prasanje}
#
#     Резултати од гласањето:
#     {rezultati_text}
#
#     Задача:
#     Напиши кратко резиме од 2–4 реченици на македонски јазик.
#     Додај 1 интересна забелешка (дали има јасен победник или резултатите се тесни).
#     """
#
#     model = genai.GenerativeModel("gemini-1.5-flash")
#
#     response = model.generate_content(prompt)
#
#     return response.text