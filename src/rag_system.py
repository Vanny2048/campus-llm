"""
RAG (Retrieval-Augmented Generation) System for LMU-specific context
"""

import json
import os
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import sqlite3
from .utils import logger, clean_text

class RAGSystem:
    def __init__(self):
        """Initialize the RAG system"""
        self.embedding_model = None
        self.knowledge_base = []
        self.embeddings = []
        self.db_path = "data/rag_knowledge.db"
        
        # Initialize embedding model
        self._load_embedding_model()
        
        # Load or create knowledge base
        self._initialize_knowledge_base()

    def _load_embedding_model(self):
        """Load the sentence transformer model for embeddings"""
        try:
            # Use a lightweight model that works well for semantic search
            model_name = "all-MiniLM-L6-v2"
            logger.info(f"Loading embedding model: {model_name}")
            self.embedding_model = SentenceTransformer(model_name)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.embedding_model = None

    def _initialize_knowledge_base(self):
        """Initialize the knowledge base database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create table for knowledge chunks
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    source TEXT,
                    category TEXT,
                    embedding BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
            # Load existing knowledge base
            self._load_knowledge_base()
            
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {e}")

    def _load_knowledge_base(self):
        """Load knowledge base from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT content, source, category FROM knowledge_chunks")
            results = cursor.fetchall()
            
            self.knowledge_base = []
            for result in results:
                self.knowledge_base.append({
                    "content": result[0],
                    "source": result[1],
                    "category": result[2]
                })
            
            conn.close()
            
            logger.info(f"Loaded {len(self.knowledge_base)} knowledge chunks")
            
            # If no knowledge base exists, create default one
            if len(self.knowledge_base) == 0:
                self._create_default_knowledge_base()
                
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")

    def _create_default_knowledge_base(self):
        """Create a default knowledge base with basic LMU information and Gen Z culture"""
        default_knowledge = [
            {
                "content": "LMU's Academic Resource Center (ARC) provides free tutoring services for students. The ARC is located in the library and offers tutoring in math, science, writing, and other subjects. Students can schedule appointments online or drop in during business hours. It's the place to go when you're struggling fr.",
                "source": "LMU ARC Website",
                "category": "Academic Support"
            },
            {
                "content": "The Rock is the most popular hangout spot on campus with amazing views of LA. It's the spot fr fr, best vibes on campus. Students go there to chill, study, or just vibe with friends.",
                "source": "LMU Campus Culture",
                "category": "Campus Life"
            },
            {
                "content": "Burns Backcourt is the 24/7 study space in the library. It's where the grind happens, lowkey the best study spot. Perfect for all-nighters and cram sessions.",
                "source": "LMU Campus Culture",
                "category": "Academic Support"
            },
            {
                "content": "The Lair is the main dining hall on campus. The food be bussin sometimes ngl. It's where everyone goes for meals and to hang out.",
                "source": "LMU Campus Culture",
                "category": "Campus Life"
            },
            {
                "content": "PROWL is LMU's student portal that everyone hates but we need it. It's where you register for classes, check grades, and handle all the admin stuff. Sometimes it crashes during registration which is a whole PROWL moment.",
                "source": "LMU Student Portal",
                "category": "Administrative"
            },
            {
                "content": "First Fridays are monthly campus events that always slap. It's the monthly vibe check where students come together for fun activities and free food.",
                "source": "LMU Campus Events",
                "category": "Campus Life"
            },
            {
                "content": "Gersten Pavilion is where basketball games happen and it gets wild fr. The energy is unmatched when the Lions are playing. Free t-shirts and lots of school spirit.",
                "source": "LMU Athletics",
                "category": "Athletics"
            },
            {
                "content": "Sunset Strip is the walkway with the most aesthetic sunset views on campus, periodt. Perfect for evening walks and taking pics for the gram.",
                "source": "LMU Campus Culture",
                "category": "Campus Life"
            },
            {
                "content": "The Quad is the main campus green space perfect for vibing and people watching. Students hang out there between classes and during nice weather.",
                "source": "LMU Campus Culture",
                "category": "Campus Life"
            },
            {
                "content": "Lion Dollars are campus currency for dining and other campus services. You can use them at the C-Store, dining halls, and other campus locations. Some students flex their Lion Dollars balance.",
                "source": "LMU Campus Services",
                "category": "Campus Life"
            },
            {
                "content": "The C-Store is the convenience store on campus where you can get snacks, drinks, and basic supplies. Students make C-Store runs for quick snacks between classes.",
                "source": "LMU Campus Services",
                "category": "Campus Life"
            },
            {
                "content": "The Village is the off-campus housing area where upperclassmen live. It's Village life and has its own community vibe separate from on-campus housing.",
                "source": "LMU Housing",
                "category": "Housing"
            },
            {
                "content": "U-Hall is University Hall, the main admin building where you handle all the U-Hall hustle like registration, financial aid, and other administrative stuff.",
                "source": "LMU Administration",
                "category": "Administrative"
            },
            {
                "content": "The Writing Center helps with papers and writing assignments. It saves your essays fr fr. Located in the library and offers both in-person and online appointments.",
                "source": "LMU Academic Support",
                "category": "Academic Support"
            },
            {
                "content": "CPS (Counseling and Psychological Services) is where you go when you need to talk to someone fr. They provide mental health support and are located in Foley Annex.",
                "source": "LMU Wellness",
                "category": "Wellness"
            },
            {
                "content": "The minimum GPA requirement to remain in good academic standing at LMU is 2.0. Students with a GPA below 2.0 may be placed on academic probation. To graduate, students typically need a cumulative GPA of 2.0 or higher.",
                "source": "LMU Academic Policies",
                "category": "Academic Requirements"
            },
            {
                "content": "LMU offers study abroad programs in over 40 countries. Students typically need a 3.0 GPA to be eligible for study abroad. The application deadline is usually in February for fall programs and September for spring programs.",
                "source": "LMU Study Abroad Office",
                "category": "Study Abroad"
            },
            {
                "content": "The William H. Hannon Library is open Monday-Thursday 7:30 AM to 2:00 AM, Friday 7:30 AM to 8:00 PM, Saturday 9:00 AM to 8:00 PM, and Sunday 10:00 AM to 2:00 AM. Hours may vary during finals week and holidays.",
                "source": "LMU Library Website",
                "category": "Campus Resources"
            },
            {
                "content": "LMU's Counseling and Psychological Services (CPS) provides free mental health services to all enrolled students. Services include individual counseling, group therapy, crisis intervention, and workshops. CPS is located in the Foley Annex.",
                "source": "LMU CPS Website",
                "category": "Student Services"
            },
            {
                "content": "To file an academic grievance at LMU, students should first try to resolve the issue with the instructor. If unsuccessful, contact the department chair, then the dean of the school. The Office of the Provost handles final appeals.",
                "source": "LMU Student Handbook",
                "category": "Academic Policies"
            },
            {
                "content": "LMU dining locations include the Lair (main dining hall), Jamba Juice, Starbucks, Panda Express, and various food trucks. Meal plans are required for students living on campus. The Lair is open 7:00 AM to 10:00 PM Monday-Friday.",
                "source": "LMU Dining Services",
                "category": "Campus Life"
            },
            {
                "content": "The last day to add/drop classes is typically during the first week of the semester. The last day to withdraw from classes with a 'W' grade is usually around the 10th week of the semester. Check the academic calendar for exact dates.",
                "source": "LMU Registrar",
                "category": "Academic Calendar"
            },
            {
                "content": "LMU's Career and Professional Development office helps students with internships, job searches, resume writing, and interview preparation. They host career fairs each semester and offer one-on-one career counseling.",
                "source": "LMU Career Services",
                "category": "Career Services"
            },
            {
                "content": "Parking on campus requires a valid parking permit. Student permits cost around $400-800 per year depending on the lot. Visitor parking is available for $3 per hour. Parking violations result in fines starting at $35.",
                "source": "LMU Parking Services",
                "category": "Campus Resources"
            }
        ]
        
        # Add default knowledge to database
        for item in default_knowledge:
            self.add_knowledge(item["content"], item["source"], item["category"])
        
        logger.info("Created default knowledge base")

    def add_knowledge(self, content: str, source: str = "", category: str = "General") -> bool:
        """Add new knowledge to the database"""
        try:
            if not self.embedding_model:
                logger.warning("Embedding model not available, skipping knowledge addition")
                return False
            
            content = clean_text(content)
            if not content:
                return False
            
            # Generate embedding
            embedding = self.embedding_model.encode([content])[0]
            embedding_blob = embedding.tobytes()
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO knowledge_chunks (content, source, category, embedding)
                VALUES (?, ?, ?, ?)
            """, (content, source, category, embedding_blob))
            
            conn.commit()
            conn.close()
            
            # Add to in-memory knowledge base
            self.knowledge_base.append({
                "content": content,
                "source": source,
                "category": category
            })
            
            logger.info(f"Added knowledge chunk: {content[:100]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            return False

    def get_relevant_context(self, query: str, max_results: int = 3) -> str:
        """Get relevant context for a query using semantic search"""
        try:
            if not self.embedding_model or len(self.knowledge_base) == 0:
                return ""
            
            query = clean_text(query)
            if not query:
                return ""
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Get all embeddings from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT content, source, category, embedding FROM knowledge_chunks")
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return ""
            
            # Calculate similarities
            similarities = []
            for i, (content, source, category, embedding_blob) in enumerate(results):
                try:
                    embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                    similarity = np.dot(query_embedding, embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                    )
                    similarities.append((similarity, content, source, category))
                except Exception as e:
                    logger.warning(f"Error calculating similarity for chunk {i}: {e}")
                    continue
            
            # Sort by similarity and get top results
            similarities.sort(key=lambda x: x[0], reverse=True)
            top_results = similarities[:max_results]
            
            # Format context
            context_parts = []
            for similarity, content, source, category in top_results:
                if similarity > 0.3:  # Threshold for relevance
                    context_parts.append(f"[{category}] {content}")
                    if source:
                        context_parts.append(f"Source: {source}")
                    context_parts.append("")  # Add spacing
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting relevant context: {e}")
            return ""

    def search_knowledge(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search knowledge base with optional category filter"""
        try:
            results = []
            query_lower = query.lower()
            
            for item in self.knowledge_base:
                # Category filter
                if category and item["category"].lower() != category.lower():
                    continue
                
                # Simple text search (can be enhanced with semantic search)
                if (query_lower in item["content"].lower() or 
                    query_lower in item["category"].lower()):
                    results.append(item)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge: {e}")
            return []

    def get_categories(self) -> List[str]:
        """Get all available categories"""
        try:
            categories = set()
            for item in self.knowledge_base:
                categories.add(item["category"])
            return sorted(list(categories))
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []

    def update_knowledge_from_file(self, file_path: str) -> int:
        """Update knowledge base from a JSON file"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"Knowledge file not found: {file_path}")
                return 0
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            added_count = 0
            
            # Handle different JSON formats
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "content" in item:
                        success = self.add_knowledge(
                            item["content"],
                            item.get("source", ""),
                            item.get("category", "General")
                        )
                        if success:
                            added_count += 1
            elif isinstance(data, dict):
                for category, items in data.items():
                    if isinstance(items, list):
                        for item in items:
                            if isinstance(item, dict) and "content" in item:
                                success = self.add_knowledge(
                                    item["content"],
                                    item.get("source", ""),
                                    category
                                )
                                if success:
                                    added_count += 1
                            elif isinstance(item, str):
                                success = self.add_knowledge(item, "", category)
                                if success:
                                    added_count += 1
            
            logger.info(f"Added {added_count} knowledge items from {file_path}")
            return added_count
            
        except Exception as e:
            logger.error(f"Error updating knowledge from file: {e}")
            return 0

    def export_knowledge(self, file_path: str) -> bool:
        """Export knowledge base to JSON file"""
        try:
            # Organize by category
            categorized_knowledge = {}
            for item in self.knowledge_base:
                category = item["category"]
                if category not in categorized_knowledge:
                    categorized_knowledge[category] = []
                categorized_knowledge[category].append({
                    "content": item["content"],
                    "source": item["source"]
                })
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(categorized_knowledge, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported knowledge base to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting knowledge: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        try:
            categories = {}
            total_chunks = len(self.knowledge_base)
            
            for item in self.knowledge_base:
                category = item["category"]
                categories[category] = categories.get(category, 0) + 1
            
            return {
                "total_chunks": total_chunks,
                "categories": categories,
                "embedding_model": self.embedding_model.model_name if self.embedding_model else None
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}

# Test function
def test_rag_system():
    """Test the RAG system functionality"""
    rag = RAGSystem()
    
    # Test adding knowledge
    success = rag.add_knowledge(
        "Test knowledge content about LMU testing",
        "Test Source",
        "Testing"
    )
    print(f"Add knowledge test: {'✅' if success else '❌'}")
    
    # Test getting context
    context = rag.get_relevant_context("testing information")
    print(f"Get context test: {'✅' if context else '❌'}")
    
    # Test search
    results = rag.search_knowledge("LMU")
    print(f"Search test: {'✅' if len(results) > 0 else '❌'}")
    
    # Test stats
    stats = rag.get_stats()
    print(f"Stats test: {'✅' if 'total_chunks' in stats else '❌'}")
    
    print("🧠 RAG system test completed!")

if __name__ == "__main__":
    test_rag_system()