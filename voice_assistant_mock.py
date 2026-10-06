#!/usr/bin/env python3
"""
Egyptian Arabic Voice Assistant (Mock Version for Testing)
This program simulates a voice assistant that listens for voice questions in Egyptian Arabic and responds with audio.
It connects to a database of assets and uses the table headers as possible questions.
This mock version allows testing without requiring physical microphone/speaker hardware.
"""

import pyttsx3
import sqlite3
import json
import os
from datetime import datetime
import time

class EgyptianVoiceAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Initialize database connection
        self.db_path = "assets_database.db"
        self.init_database()
        
        # Wake word detection
        self.wake_words = ["يا مساعد", "مساعد", "اهلا", "السلام"]
        
        print("تم تهيئة مساعد الصوت!")
        print("الجهاز ممكن يشتغل من غير ما يكون في مايك فعلي لأننا في وضع المحاكاة")
    
    def setup_tts(self):
        """Configure the text-to-speech engine"""
        # Set TTS properties
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find an Arabic voice if available
        for voice in voices:
            if 'arabic' in voice.name.lower() or 'ar' in voice.id.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate
        self.tts_engine.setProperty('rate', 150)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"المساعد يقول: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def simulate_listen(self):
        """Simulate listening for voice input (in real app, this would use microphone)"""
        print("\nأنا أستمع... (الوضع دلوقتي في المحاكاة)")
        print("من فضلك اكتب سؤالك في العربية العامية:")
        print("مثال: 'قولي عن التليفزيون' أو 'شنو معاك في الثلاجة'")
        
        try:
            # Simulate listening by getting input from user
            text = input("اكتب سؤالك هنا: ")
            print(f"النص اللي دخلته: {text}")
            return text.lower()
        except Exception as e:
            print(f"خطأ أثناء الاستماع: {e}")
            return ""
    
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
        
        # Format results into a spoken response
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
        self.speak("أهلاً بيك! أنا مساعدك الصوتي. قول يا مساعد لو عايز تكلمني.")
        
        while True:
            try:
                # Listen for wake word or command (simulated)
                text = self.simulate_listen()
                
                if not text:
                    continue
                
                # Check for wake word
                if self.detect_wake_word(text):
                    self.speak("أنا مستنيك، قول سؤالك.")
                    
                    # Listen for the actual question (simulated)
                    question = self.simulate_listen()
                    
                    if question:
                        # Search database based on question
                        results = self.search_database(question)
                        
                        # Generate and speak response
                        response = self.generate_response(question, results)
                        self.speak(response)
                        
                        # Ask if they need anything else
                        self.speak("هل هناك حاجة تانية؟")
                
                # Add a small delay to prevent overloading
                time.sleep(1)
            
            except KeyboardInterrupt:
                print("\nتم إيقاف المساعد.")
                self.speak("وداعًا!")
                break
            except Exception as e:
                print(f"حدث خطأ: {e}")
                self.speak("حصل خطأ، برهمني.")

def main():
    """Main function to run the voice assistant"""
    print("جاري تشغيل مساعد الصوت باللهجة العامية المصرية (الوضع التجريبي)...")

    # Create and run the assistant
    assistant = EgyptianVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()