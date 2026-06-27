import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


class RGAI:

    def rewrite(self, question, answer):

        prompt = f"""
أنت مساعد لدليل التأجير اليومي.

مهمتك فقط إعادة صياغة الإجابة.

القواعد:

- لا تضف أي معلومة جديدة.
- لا تخترع.
- لا تغير المعنى.
- اجعل الرد مختصرًا.
- لا يتجاوز 120 كلمة.
- أجب باللغة العربية.

السؤال:
{question}

إجابة الكتاب:
{answer}
"""

        response = model.generate_content(prompt)

        return response.text
