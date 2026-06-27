import os
import json

KNOWLEDGE_PATH = "knowledge/capsules"


class KnowledgeManager:

    def __init__(self):
        self.capsules = []
        self.load_capsules()

    def load_capsules(self):

        self.capsules = []

        if not os.path.exists(KNOWLEDGE_PATH):
            return

        for filename in os.listdir(KNOWLEDGE_PATH):

            if filename.endswith(".json"):

                path = os.path.join(KNOWLEDGE_PATH, filename)

                with open(path, "r", encoding="utf-8") as file:

                    capsule = json.load(file)

                self.capsules.append(capsule)

    def search(self, question):

        question = question.lower()

        for capsule in self.capsules:

            if capsule["question"].lower() in question:

                return capsule

        return None
