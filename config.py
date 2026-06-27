"""
=========================================
RG AI Configuration
=========================================
Central configuration file for the project.

Do NOT place secrets directly in the code.
All sensitive values are loaded from Railway / .env
=========================================
"""

import os


# ==========================================================
# Project Information
# ==========================================================

PROJECT_NAME = "RG AI"

PROJECT_VERSION = "2.0"

EXPERT_NAME = "Fahad Alghamdi"

LANGUAGE = "Arabic"


# ==========================================================
# Telegram
# ==========================================================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# ==========================================================
# Google Gemini
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"


# ==========================================================
# Database
# ==========================================================

DATABASE_PATH = "database/rg.db"


# ==========================================================
# Knowledge Base
# ==========================================================

KNOWLEDGE_FOLDER = "knowledge"

DOCUMENTS_FOLDER = "knowledge/documents"

VECTOR_FOLDER = "knowledge/vectors"


# ==========================================================
# RG Brain
# ==========================================================

MIN_CONFIDENCE = 0.80

MAX_RESULTS = 3


# ==========================================================
# Consultation
# ==========================================================

CONSULTATION_USERNAME = "@YOUR_USERNAME"

CONSULTATION_MESSAGE = """
هذا السؤال يحتاج استشارة خاصة لأنه خارج محتوى دليل RG AI.

للتواصل مع الخبير:

{}
""".format(CONSULTATION_USERNAME)


# ==========================================================
# Bot Messages
# ==========================================================

WELCOME_MESSAGE = """
👋 أهلاً بك في RG AI

أنا مساعد متخصص في التأجير اليومي عبر Airbnb.

أجيب فقط من دليل RG AI.

إذا احتاج سؤالك إلى تحليل خاص،
فسأحولك مباشرة إلى الخبير.
"""
