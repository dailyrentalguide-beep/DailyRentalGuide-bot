"""
شغّل هذا الملف مرة واحدة فقط لإضافة كود تفعيل تجريبي:

    python add_test_code.py

بعدها احذفه أو تجاهله — مو جزء من تشغيل البوت.
"""

from database import db

TEST_CODE = "TEST-0001"

db.add_code(TEST_CODE, subscription_type="FREE")

print(f"✅ تمت إضافة كود التجربة: {TEST_CODE}")
print("جرّبه الآن داخل البوت بعد /start")
