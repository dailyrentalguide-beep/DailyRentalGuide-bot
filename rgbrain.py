"""
=========================================
RG Brain v2
The Heart of RG AI
=========================================
"""

from config import MIN_CONFIDENCE


class RGBrain:

    def __init__(self):
        self.version = "2.0"

    def search(self, question):
        """
        Search the Knowledge Base.

        Returns:
            Capsules
        """
        print(f"Searching for: {question}")

        return []

    def calculate_confidence(self, capsules):
        """
        Calculate confidence score.
        """

        if len(capsules) == 0:
            return 0.0

        return 0.95

    def answer(self, question):
        """
        Main Brain Logic
        """

        capsules = self.search(question)

        confidence = self.calculate_confidence(capsules)

        if confidence >= MIN_CONFIDENCE:

            return {
                "status": "FOUND",
                "confidence": confidence,
                "capsules": capsules
            }

        return {
            "status": "NOT_FOUND",
            "confidence": confidence,
            "capsules": []
        }

    def learn(self, question, answer):
        """
        Learn new approved knowledge.
        """

        print("Learning new knowledge...")

        return True
