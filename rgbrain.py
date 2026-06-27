"""
=========================================
RG Brain v3
The Heart of RG AI
=========================================
"""

from config import MIN_CONFIDENCE
from knowledge_manager import KnowledgeManager


class RGBrain:

    def __init__(self):

        self.version = "3.0"

        self.knowledge = KnowledgeManager()

    def search(self, question):

        return self.knowledge.search(question)

    def answer(self, question):

        result = self.search(question)

        if result:

            return {
                "status": "FOUND",
                "answer": result["answer"],
                "confidence": 0.95,
                "source": result.get("source", "Unknown"),
                "category": result.get("category", "General")
            }

        return {
            "status": "NOT_FOUND",
            "answer": None,
            "confidence": 0.0
        }
