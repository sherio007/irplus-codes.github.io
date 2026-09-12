#!/usr/bin/env python3
"""
Egyptian Arabic Voice Assistant (Simple Version)
This program demonstrates a voice assistant that responds to questions in Egyptian Arabic.
It connects to a database of assets and provides text-based simulation for testing.
"""

import sqlite3
import os
from datetime import datetime

class EgyptianVoiceAssistant:
    def __init__(self):
        # Initialize database connection
        self.db_path = "assets_database.db"
        self.init_database()
        
        # Wake word detection
        self.wake_words = ["يا مساعد", "مساعد", "اهلا", "السلام"]
        
        print("تم تهيئة مساعد الصوت!")
        print("الجهاز ممكن يشتغل من غير ما يكون في مايك فعلي لأننا في وضع المحاكاة")
    
    def init_database(self):
        """Initialize the database with sample asset data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create a sample assets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT NOT NULL,
                asset_type TEXT,
                location TEXT,
                status TEXT,
                description TEXT
            )
        ''')
        
        # Insert sample data
        sample_assets = [
            ("تلفزيون سامسونج", "إلكترونيات", "غرفة المعيشة", "يعمل", "تلفزيون ذكي 55 بوصة"),
            ("ثلاجة LG", "أجهزة كهربائية", "المطبخ", "يعمل", "ثلاجة بابين سعة كبيرة"),
            ("مكيف باناسونيك", "تكييف", "غرفة النوم الرئيسية", "يعمل", "تبريد قوي وصامت"),
            ("غسالة توشيبا", "غسالات", "الشرفة", "تحتاج صيانة", "تحتاج صيانة"),
            ("موتور كهربائي", "أجزاء", "المخزن", "متاح", "استعداد للتركيب")
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO assets (asset_name, asset_type, location, status, description) VALUES (?, ?, ?, ?, ?)",
            sample_assets
        )
        
        conn.commit()
        conn.close()
        print("تم تهيئة قاعدة البيانات")
    
    def search_database(self, question):
        """Search the database based on the question"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple keyword matching for demonstration
        # In a real implementation, you'd want more sophisticated NLP
        question_lower = question.lower()
        
        # Check for asset name mentions
        if "تليفزيون" in question_lower or "تيليفزيون" in question_lower or "تي في" in question_lower or "شاشة" in question_lower:
            cursor.execute("SELECT * FROM assets WHERE asset_name LIKE '%تليفزيون%' OR asset_name LIKE '%تي في%' OR asset_name LIKE '%شاشة%' OR asset_type LIKE '%إلكترونيات%'")
        elif "ثلاجة" in question_lower or "ثلاجه" in question_lower:
            cursor.execute("SELECT * FROM assets WHERE asset_name LIKE '%ثلاجة%' OR asset_type LIKE '%أجهزة كهربائية%'")
        elif "مكيف" in question_lower or "تكييف" in question_lower:
            cursor.execute("SELECT * FROM assets WHERE asset_name LIKE '%مكيف%' OR asset_type LIKE '%تكييف%'")
        elif "غسالة" in question_lower or "غساله" in question_lower:
            cursor.execute("SELECT * FROM assets WHERE asset_name LIKE '%غسالة%' OR asset_type LIKE '%غسالات%'")
        elif "الكل" in question_lower or "كامل" in question_lower or "جميع" in question_lower:
            cursor.execute("SELECT * FROM assets")
        else:
            # General search based on keywords
            search_pattern = f"%{question}%"
            cursor.execute("SELECT * FROM assets WHERE asset_name LIKE ? OR description LIKE ? OR location LIKE ?", 
                          (search_pattern, search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def generate_response(self, question, results):
        """Generate a response based on the question and database results"""
        if not results:
            return "عذرًا، ملقتش أي معلومات متعلقة بسؤالك."
        
        # Format results into a response
        response_parts = []
        response_parts.append(f"فيه {len(results)} عناصر متعلقة بسؤالك:")
        
        for result in results:
            asset_id, asset_name, asset_type, location, status, description = result
            response_parts.append(f"{asset_name} نوعه {asset_type} موجود في {location} وحالته {status}. {description}")
        
        return " ".join(response_parts)
    
    def detect_wake_word(self, text):
        """Check if the wake word was detected"""
        for word in self.wake_words:
            if word in text:
                return True
        return False
    
    def run(self):
        """Main loop for the voice assistant"""
        print("أهلاً بيك! أنا مساعدك الصوتي. قول \"يا مساعد\" لو عايز تكلمني.")
        
        while True:
            try:
                # Simulate listening for wake word or command
                text = input("\nاكتب نص السؤال هنا (اكتب 'خروج' للإنهاء): ")
                
                if text.lower() == 'خروج':
                    print("وداعًا!")
                    break
                
                if not text:
                    continue
                
                # Check for wake word
                if self.detect_wake_word(text):
                    print("أنا مستنيك، قول سؤالك.")
                    
                    # Get the actual question
                    question = input("اكتب سؤالك هنا: ")
                    
                    if question:
                        # Search database based on question
                        results = self.search_database(question)
                        
                        # Generate and display response
                        response = self.generate_response(question, results)
                        print(f"الإجابة: {response}")
                        
                        # Ask if they need anything else
                        print("هل هناك حاجة تانية؟")
                
            except KeyboardInterrupt:
                print("\nتم إيقاف المساعد.")
                print("وداعًا!")
                break
            except Exception as e:
                print(f"حدث خطأ: {e}")

def main():
    """Main function to run the voice assistant"""
    print("جاري تشغيل مساعد الصوت باللهجة العامية المصرية (النسخة المبسطة)...")

    # Create and run the assistant
    assistant = EgyptianVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()