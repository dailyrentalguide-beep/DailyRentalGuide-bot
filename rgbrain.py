"""
=========================================
RG Brain v3
The Heart of RG AI
=========================================
"""

from config import MIN_CONFIDENCE
from knowledge_manager import KnowledgeManager
from Ai import RGAI


class RGBrain:

    def __init__(self):

        self.version = "3.0"

        self.knowledge = KnowledgeManager()

        self.ai = RGAI()

    def search(self, question):

        return self.knowledge.search(question)

    def answer(self, question):

        result = self.search(question)

        if result:

            rewritten_answer = self.ai.rewrite(
                question,
                result["answer"]
            )

            return {
                "status": "FOUND",
                "answer": rewritten_answer,
                "confidence": 0.95,
                "source": result.get("source", "Book"),
                "category": result.get("category", "General")
            }

        return {
            "status": "NOT_FOUND",
            "answer": None,
            "confidence": 0.0
        }
