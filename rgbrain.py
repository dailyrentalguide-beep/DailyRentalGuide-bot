"""
=========================================
RG Brain v2
=========================================
"""

from config import MIN_CONFIDENCE


class RGBrain:

    def __init__(self):
        self.version = "2.0"

        # سيتم استبدالها لاحقاً بقاعدة المعرفة
        self.knowledge = [
            {
                "question": "كيف أزيد الحجوزات؟",
                "answer": "حسّن الصور، واكتب وصفاً احترافياً، وفعّل التسعير المناسب، واهتم بسرعة الرد على الضيوف."
            },
            {
                "question": "كيف أرفع التقييم؟",
                "answer": "النظافة وسرعة التواصل وتجربة الضيف هي أهم أسباب ارتفاع التقييم."
            }
        ]

    def search(self, question):

        for item in self.knowledge:

            if item["question"] == question:
                return item

        return None

    def answer(self, question):

        result = self.search(question)

        if result:

            return {
                "status": "FOUND",
                "answer": result["answer"],
                "confidence": 0.95
            }

        return {
            "status": "NOT_FOUND",
            "answer": None,
            "confidence": 0.0
        }
