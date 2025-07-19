"""
Data Collector for gathering LMU-specific information
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time
import re
from .utils import logger, clean_text

class LMUDataCollector:
    def __init__(self):
        """Initialize the data collector"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # LMU websites to scrape (public information only)
        self.lmu_urls = {
            "academic_calendar": "https://academics.lmu.edu/calendar/",
            "library_hours": "https://library.lmu.edu/hours/",
            "dining": "https://www.lmu.edu/campuslife/dining/",
            "parking": "https://www.lmu.edu/campuslife/commuterstudents/parking/",
            "tutoring": "https://academics.lmu.edu/arc/",
            "counseling": "https://studentaffairs.lmu.edu/cps/",
            "career_services": "https://studentaffairs.lmu.edu/cpd/",
            "study_abroad": "https://bellarmine.lmu.edu/internationalprograms/studyabroad/"
        }
        
        # Rate limiting
        self.request_delay = 2  # seconds between requests

    def collect_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Collect data from all sources"""
        all_data = {}
        
        logger.info("Starting LMU data collection...")
        
        # Collect basic LMU information
        all_data["basic_info"] = self._collect_basic_info()
        
        # Collect events (sample data for MVP)
        all_data["events"] = self._collect_sample_events()
        
        # Collect FAQ data
        all_data["faqs"] = self._collect_sample_faqs()
        
        # Collect academic information
        all_data["academic"] = self._collect_academic_info()
        
        # Save collected data
        self._save_collected_data(all_data)
        
        logger.info("Data collection completed")
        return all_data

    def _collect_basic_info(self) -> List[Dict[str, Any]]:
        """Collect basic LMU information"""
        basic_info = [
            {
                "content": "Loyola Marymount University (LMU) is a private Jesuit research university located in Los Angeles, California. Founded in 1911, LMU serves over 9,000 students across undergraduate and graduate programs.",
                "source": "LMU Official Website",
                "category": "About LMU"
            },
            {
                "content": "LMU's main campus is located in the Westchester area of Los Angeles, near LAX airport. The campus features modern facilities, beautiful architecture, and stunning views of the Pacific Ocean.",
                "source": "LMU Campus Information",
                "category": "Campus"
            },
            {
                "content": "LMU offers undergraduate degrees through six schools: Bellarmine College of Liberal Arts, College of Business Administration, School of Education, Seaver College of Science and Engineering, School of Film and Television, and College of Communication and Fine Arts.",
                "source": "LMU Academic Programs",
                "category": "Academics"
            },
            {
                "content": "The LMU Lions compete in NCAA Division I athletics. Popular sports include basketball, soccer, tennis, and volleyball. The Gersten Pavilion hosts basketball and volleyball games.",
                "source": "LMU Athletics",
                "category": "Athletics"
            }
        ]
        
        return basic_info

    def _collect_sample_events(self) -> List[Dict[str, Any]]:
        """Collect sample events data (for MVP demonstration)"""
        # In a real implementation, this would scrape actual event data
        now = datetime.now()
        
        sample_events = [
            {
                "title": "Study Abroad Information Session",
                "description": "Learn about LMU's study abroad programs in over 40 countries. Pizza will be provided!",
                "date": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
                "time": "6:00 PM - 7:30 PM",
                "location": "Student Union, Room 201",
                "category": "Academic",
                "free_food": True,
                "points": 8,
                "contact": "studyabroad@lmu.edu"
            },
            {
                "title": "Career Fair - Tech & Engineering",
                "description": "Meet with top tech companies and engineering firms. Bring your resume!",
                "date": (now + timedelta(days=5)).strftime("%Y-%m-%d"),
                "time": "10:00 AM - 4:00 PM",
                "location": "Gersten Pavilion",
                "category": "Career",
                "free_food": False,
                "points": 10,
                "contact": "career@lmu.edu"
            },
            {
                "title": "Mental Health Awareness Workshop",
                "description": "Join CPS for a workshop on stress management and wellness strategies.",
                "date": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
                "time": "2:00 PM - 3:30 PM",
                "location": "Foley Annex",
                "category": "Wellness",
                "free_food": True,
                "points": 5,
                "contact": "cps@lmu.edu"
            },
            {
                "title": "Lions Basketball vs USC",
                "description": "Cheer on the Lions at our rivalry game! Free t-shirts for students.",
                "date": (now + timedelta(days=7)).strftime("%Y-%m-%d"),
                "time": "7:00 PM",
                "location": "Gersten Pavilion",
                "category": "Athletics",
                "free_food": False,
                "points": 5,
                "contact": "athletics@lmu.edu"
            },
            {
                "title": "Taco Tuesday at the Lair",
                "description": "Special taco bar with build-your-own options. $2 tacos all day!",
                "date": now.strftime("%Y-%m-%d"),
                "time": "11:00 AM - 8:00 PM",
                "location": "The Lair Dining Hall",
                "category": "Dining",
                "free_food": False,
                "points": 2,
                "contact": "dining@lmu.edu"
            }
        ]
        
        return sample_events

    def _collect_sample_faqs(self) -> List[Dict[str, Any]]:
        """Collect sample FAQ data"""
        faqs = [
            {
                "question": "How do I register for classes?",
                "answer": "Students register for classes through PROWL (LMU's student portal). Registration dates are assigned based on class standing and credit hours. Check your registration date in PROWL and prepare an alternate schedule in case your preferred classes are full.",
                "category": "Registration"
            },
            {
                "question": "Where can I find my academic advisor?",
                "answer": "Your academic advisor assignment depends on your major. Check PROWL for your advisor's contact information, or contact your department directly. Advisors help with course planning, degree requirements, and academic guidance.",
                "category": "Academic Support"
            },
            {
                "question": "How do I apply for financial aid?",
                "answer": "Complete the FAFSA (Free Application for Federal Student Aid) by the priority deadline. LMU's school code is 001234. Also complete the CSS Profile for institutional aid. Contact the Financial Aid office for assistance.",
                "category": "Financial Aid"
            },
            {
                "question": "What are the library hours?",
                "answer": "The William H. Hannon Library is typically open Monday-Thursday 7:30 AM to 2:00 AM, Friday 7:30 AM to 8:00 PM, Saturday 9:00 AM to 8:00 PM, and Sunday 10:00 AM to 2:00 AM. Hours may vary during finals week and holidays.",
                "category": "Campus Resources"
            },
            {
                "question": "How do I get involved on campus?",
                "answer": "LMU has over 200 student organizations. Attend the Activities Fair at the beginning of each semester, check LionsConnect for organizations, or start your own group. Popular activities include Greek life, cultural organizations, academic clubs, and service groups.",
                "category": "Student Life"
            },
            {
                "question": "Where can I get tutoring help?",
                "answer": "The Academic Resource Center (ARC) in the library offers free tutoring for many subjects. You can also find subject-specific tutoring through departments, peer tutoring programs, or the Writing Center for help with papers and presentations.",
                "category": "Academic Support"
            },
            {
                "question": "How do I report a maintenance issue in my dorm?",
                "answer": "Report maintenance issues through the Residence Life portal or call the Facilities Management work order desk. For emergencies (no heat, water leaks, safety issues), call Campus Safety immediately.",
                "category": "Housing"
            },
            {
                "question": "What meal plan options are available?",
                "answer": "LMU offers several meal plan options including unlimited dining, block plans (14, 10, or 5 meals per week), and commuter plans. All residential students are required to have a meal plan. Plans include Lion Cash for use at retail locations.",
                "category": "Dining"
            }
        ]
        
        return [{"content": f"Q: {faq['question']}\nA: {faq['answer']}", 
                "source": "LMU FAQ", 
                "category": faq['category']} for faq in faqs]

    def _collect_academic_info(self) -> List[Dict[str, Any]]:
        """Collect academic policy information"""
        academic_info = [
            {
                "content": "The academic year at LMU consists of two semesters (fall and spring) plus optional summer sessions. Each semester is approximately 15 weeks long. Finals week occurs at the end of each semester.",
                "source": "LMU Academic Calendar",
                "category": "Academic Calendar"
            },
            {
                "content": "To maintain good academic standing, undergraduate students must maintain a cumulative GPA of 2.0 or higher. Students below this threshold may be placed on academic probation and must meet with an academic advisor.",
                "source": "LMU Academic Policies",
                "category": "Academic Requirements"
            },
            {
                "content": "The pass/no pass grading option allows students to take certain courses without affecting their GPA. Students must declare pass/no pass by the deadline (usually mid-semester). Some courses and majors do not allow pass/no pass grading.",
                "source": "LMU Grading Policies",
                "category": "Grading"
            },
            {
                "content": "LMU's core curriculum includes requirements in theology, philosophy, history, literature, science, mathematics, and fine arts. All undergraduate students must complete these requirements regardless of major.",
                "source": "LMU Core Curriculum",
                "category": "Graduation Requirements"
            },
            {
                "content": "Students can appeal grades by first discussing with the instructor, then the department chair, and finally the dean of the school. Grade appeals must be filed within one year of receiving the grade.",
                "source": "LMU Grade Appeal Process",
                "category": "Academic Policies"
            }
        ]
        
        return academic_info

    def scrape_lmu_website(self, url: str, category: str) -> List[Dict[str, Any]]:
        """Scrape information from an LMU website (placeholder for future implementation)"""
        # This is a placeholder function for actual web scraping
        # In a real implementation, you would:
        # 1. Make HTTP request to the URL
        # 2. Parse HTML with BeautifulSoup
        # 3. Extract relevant information
        # 4. Clean and structure the data
        
        logger.info(f"Scraping {url} for {category} information...")
        
        try:
            # Add delay to be respectful
            time.sleep(self.request_delay)
            
            # Note: Actual scraping would require careful consideration of:
            # - robots.txt compliance
            # - Terms of service
            # - Rate limiting
            # - Content structure analysis
            
            # For MVP, return empty list (use sample data instead)
            return []
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []

    def collect_events_data(self) -> List[Dict[str, Any]]:
        """Collect current events data"""
        # For MVP, return sample events
        # In production, this would scrape actual event sources
        return self._collect_sample_events()

    def update_events_file(self):
        """Update the events JSON file with current data"""
        try:
            events = self.collect_events_data()
            
            # Save to events file
            events_file = "data/events/current_events.json"
            os.makedirs(os.path.dirname(events_file), exist_ok=True)
            
            with open(events_file, 'w') as f:
                json.dump(events, f, indent=2)
            
            logger.info(f"Updated events file with {len(events)} events")
            
        except Exception as e:
            logger.error(f"Error updating events file: {e}")

    def _save_collected_data(self, data: Dict[str, List[Dict[str, Any]]]):
        """Save collected data to files"""
        try:
            # Create data directory
            os.makedirs("data/lmu_knowledge", exist_ok=True)
            
            # Save each category
            for category, items in data.items():
                filename = f"data/lmu_knowledge/{category}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved {len(items)} items to {filename}")
            
            # Save combined data
            combined_file = "data/lmu_knowledge/all_data.json"
            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info("Data collection saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving collected data: {e}")

    def validate_data_quality(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate the quality of collected data"""
        stats = {
            "total_items": len(data),
            "empty_content": 0,
            "missing_source": 0,
            "missing_category": 0,
            "avg_content_length": 0
        }
        
        total_length = 0
        
        for item in data:
            if not item.get("content", "").strip():
                stats["empty_content"] += 1
            
            if not item.get("source", "").strip():
                stats["missing_source"] += 1
            
            if not item.get("category", "").strip():
                stats["missing_category"] += 1
            
            total_length += len(item.get("content", ""))
        
        if len(data) > 0:
            stats["avg_content_length"] = total_length / len(data)
        
        return stats

    def create_knowledge_summary(self) -> Dict[str, Any]:
        """Create a summary of available knowledge"""
        try:
            knowledge_dir = "data/lmu_knowledge"
            if not os.path.exists(knowledge_dir):
                return {"error": "Knowledge directory not found"}
            
            summary = {
                "categories": {},
                "total_items": 0,
                "last_updated": datetime.now().isoformat()
            }
            
            for filename in os.listdir(knowledge_dir):
                if filename.endswith('.json') and filename != 'all_data.json':
                    filepath = os.path.join(knowledge_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        category = filename.replace('.json', '')
                        item_count = len(data) if isinstance(data, list) else 0
                        
                        summary["categories"][category] = item_count
                        summary["total_items"] += item_count
                        
                    except Exception as e:
                        logger.warning(f"Error reading {filename}: {e}")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating knowledge summary: {e}")
            return {"error": str(e)}

# Utility functions
def run_data_collection():
    """Run the data collection process"""
    collector = LMUDataCollector()
    
    print("🔍 Starting LMU data collection...")
    data = collector.collect_all_data()
    
    print("📊 Data collection summary:")
    for category, items in data.items():
        print(f"  {category}: {len(items)} items")
    
    # Update events
    collector.update_events_file()
    
    # Create summary
    summary = collector.create_knowledge_summary()
    print(f"\n📈 Knowledge base summary:")
    print(f"  Total items: {summary.get('total_items', 0)}")
    print(f"  Categories: {len(summary.get('categories', {}))}")
    
    print("✅ Data collection completed!")

if __name__ == "__main__":
    run_data_collection()