"""
=========================================
RG Brain
Version 2.0
=========================================

The heart of RG AI.

Responsibilities:

1. Search Knowledge
2. Calculate Confidence
3. Decide
4. Rewrite Answer
5. Learn
"""

from config import MIN_CONFIDENCE


class RGBrain:

    def __init__(self):
        self.version = "2.0"

    def search(self, question):
        """
        Search the knowledge base.

        Returns:
            result
        """
        pass

    def confidence(self, result):
        """
        Calculate confidence score.

        Returns:
            float
        """
        pass

    def answer(self, question):
        """
        Main function.

        Question
            ↓
        Search
            ↓
        Confidence
            ↓
        Answer / Consultation
        """
        pass

    def learn(self):
        """
        Learn from approved consultation.
        """
        pass
