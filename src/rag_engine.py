"""
LMU Campus LLM - RAG Engine
Retrieval-Augmented Generation system for finding relevant LMU information
"""

import json
import re
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    """Retrieval-Augmented Generation engine for LMU campus information"""
    
    def __init__(self, qa_data_path: str = "data/qa_pairs.json", events_data_path: str = "data/events.json"):
        """
        Initialize RAG engine
        
        Args:
            qa_data_path: Path to Q&A dataset
            events_data_path: Path to events dataset
        """
        self.qa_data_path = qa_data_path
        self.events_data_path = events_data_path
        
        # Load data
        self.qa_pairs = self._load_qa_data()
        self.events = self._load_events_data()
        
        # Initialize sentence transformer for embeddings
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            self.embedding_model = None
        
        # Create embeddings for Q&A pairs
        self.qa_embeddings = self._create_qa_embeddings()
        
    def _load_qa_data(self) -> List[Dict]:
        """Load Q&A data from JSON file"""
        try:
            with open(self.qa_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('qa_pairs', [])
        except Exception as e:
            logger.error(f"Failed to load Q&A data: {e}")
            return []
    
    def _load_events_data(self) -> List[Dict]:
        """Load events data from JSON file"""
        try:
            with open(self.events_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('events', [])
        except Exception as e:
            logger.error(f"Failed to load events data: {e}")
            return []
    
    def _create_qa_embeddings(self) -> List[Tuple[np.ndarray, Dict]]:
        """Create embeddings for Q&A pairs"""
        if not self.embedding_model:
            return []
        
        embeddings = []
        for qa_pair in self.qa_pairs:
            try:
                # Combine question and answer for embedding
                text = f"{qa_pair['question']} {qa_pair['answer']}"
                embedding = self.embedding_model.encode(text)
                embeddings.append((embedding, qa_pair))
            except Exception as e:
                logger.error(f"Failed to create embedding for Q&A pair: {e}")
                continue
        
        return embeddings
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def search_qa_pairs(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant Q&A pairs using semantic similarity
        
        Args:
            query: User's question
            top_k: Number of top results to return
            
        Returns:
            List of relevant Q&A pairs
        """
        if not self.embedding_model or not self.qa_embeddings:
            # Fallback to keyword search
            return self._keyword_search(query, top_k)
        
        try:
            # Create embedding for query
            query_embedding = self.embedding_model.encode(query)
            
            # Calculate similarities
            similarities = []
            for embedding, qa_pair in self.qa_embeddings:
                similarity = self._cosine_similarity(query_embedding, embedding)
                similarities.append((similarity, qa_pair))
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[0], reverse=True)
            return [qa_pair for _, qa_pair in similarities[:top_k]]
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fallback keyword search"""
        query_lower = query.lower()
        results = []
        
        for qa_pair in self.qa_pairs:
            score = 0
            question_lower = qa_pair['question'].lower()
            answer_lower = qa_pair['answer'].lower()
            
            # Check for exact word matches
            query_words = set(query_lower.split())
            question_words = set(question_lower.split())
            answer_words = set(answer_lower.split())
            
            # Score based on word overlap
            question_overlap = len(query_words.intersection(question_words))
            answer_overlap = len(query_words.intersection(answer_words))
            
            score = question_overlap * 2 + answer_overlap  # Questions weighted more
            
            if score > 0:
                results.append((score, qa_pair))
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x[0], reverse=True)
        return [qa_pair for _, qa_pair in results[:top_k]]
    
    def search_events(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant events
        
        Args:
            query: User's question about events
            top_k: Number of top results to return
            
        Returns:
            List of relevant events
        """
        query_lower = query.lower()
        results = []
        
        # Keywords that indicate event-related queries
        event_keywords = ['event', 'activity', 'meeting', 'workshop', 'fair', 'mixer', 'movie', 'game', 'basketball', 'football', 'concert', 'lecture', 'seminar']
        
        is_event_query = any(keyword in query_lower for keyword in event_keywords)
        
        if not is_event_query:
            return []
        
        for event in self.events:
            score = 0
            title_lower = event['title'].lower()
            description_lower = event['description'].lower()
            category_lower = event['category'].lower()
            
            # Check for keyword matches
            query_words = set(query_lower.split())
            title_words = set(title_lower.split())
            desc_words = set(description_lower.split())
            
            # Score based on matches
            title_matches = len(query_words.intersection(title_words))
            desc_matches = len(query_words.intersection(desc_words))
            
            # Bonus for category matches
            category_bonus = 0
            if any(word in category_lower for word in query_words):
                category_bonus = 2
            
            score = title_matches * 3 + desc_matches + category_bonus
            
            if score > 0:
                results.append((score, event))
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x[0], reverse=True)
        return [event for _, event in results[:top_k]]
    
    def get_context_for_query(self, query: str) -> str:
        """
        Get relevant context for a user query
        
        Args:
            query: User's question
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Search for relevant Q&A pairs
        relevant_qa = self.search_qa_pairs(query, top_k=2)
        if relevant_qa:
            qa_context = "Relevant Information:\n"
            for qa in relevant_qa:
                qa_context += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
            context_parts.append(qa_context)
        
        # Search for relevant events
        relevant_events = self.search_events(query, top_k=3)
        if relevant_events:
            events_context = "Upcoming Events:\n"
            for event in relevant_events:
                events_context += f"• {event['title']} - {event['date']} at {event['time']}\n"
                events_context += f"  Location: {event['location']}\n"
                events_context += f"  Points: {event['points']}\n"
                if event['free_food']:
                    events_context += f"  🍕 Free food included!\n"
                events_context += f"  {event['description']}\n\n"
            context_parts.append(events_context)
        
        return "\n".join(context_parts)
    
    def get_events_by_category(self, category: str = None) -> List[Dict]:
        """
        Get events filtered by category
        
        Args:
            category: Event category to filter by
            
        Returns:
            List of events in the category
        """
        if not category:
            return self.events
        
        return [event for event in self.events if event['category'] == category]
    
    def get_events_with_food(self) -> List[Dict]:
        """Get all events that offer free food"""
        return [event for event in self.events if event['free_food']]

# Example usage
if __name__ == "__main__":
    rag = RAGEngine()
    
    # Test search
    test_query = "What are the library hours?"
    context = rag.get_context_for_query(test_query)
    print(f"Context for '{test_query}':\n{context}")
    
    # Test event search
    event_query = "What events have free food?"
    events = rag.search_events(event_query)
    print(f"\nEvents with free food: {len(events)} found")