#!/usr/bin/env python3
"""
Script to update LMU events data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collector import LMUDataCollector
from src.utils import logger
import json
from datetime import datetime, timedelta

def update_events():
    """Update the events data"""
    print("🎉 Updating LMU Events...")
    
    collector = LMUDataCollector()
    
    # Get latest events
    events = collector.collect_events_data()
    
    # Update events file
    collector.update_events_file()
    
    print(f"✅ Updated {len(events)} events")
    
    # Display upcoming events
    print("\n📅 Upcoming Events:")
    for event in events[:3]:
        print(f"   • {event['title']} - {event['date']}")
        if event.get('free_food'):
            print("     🍕 Free food!")
        print(f"     📍 {event['location']}")
        print(f"     🏆 {event['points']} points")
        print()

def add_custom_event():
    """Add a custom event"""
    print("➕ Add Custom Event")
    print("=" * 30)
    
    # Get event details
    title = input("Event Title: ").strip()
    if not title:
        print("❌ Event title is required")
        return
    
    description = input("Description: ").strip()
    date = input("Date (YYYY-MM-DD) or 'today'/'tomorrow': ").strip()
    time = input("Time (e.g., '6:00 PM - 8:00 PM'): ").strip()
    location = input("Location: ").strip()
    category = input("Category (Academic/Social/Career/Athletics/Other): ").strip() or "Other"
    
    free_food = input("Free food? (y/n): ").strip().lower() in ['y', 'yes']
    
    try:
        points = int(input("Points to award (1-10): ").strip() or "5")
        points = max(1, min(10, points))  # Clamp between 1-10
    except ValueError:
        points = 5
    
    contact = input("Contact email (optional): ").strip()
    
    # Process date
    if date.lower() == 'today':
        date = datetime.now().strftime("%Y-%m-%d")
    elif date.lower() == 'tomorrow':
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif not date:
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Create event object
    event = {
        "title": title,
        "description": description or f"Join us for {title}!",
        "date": date,
        "time": time or "TBD",
        "location": location or "TBD",
        "category": category,
        "free_food": free_food,
        "points": points,
        "contact": contact
    }
    
    # Load existing events
    events_file = "data/events/current_events.json"
    try:
        if os.path.exists(events_file):
            with open(events_file, 'r') as f:
                events = json.load(f)
        else:
            events = []
    except:
        events = []
    
    # Add new event
    events.append(event)
    
    # Save updated events
    os.makedirs(os.path.dirname(events_file), exist_ok=True)
    with open(events_file, 'w') as f:
        json.dump(events, f, indent=2)
    
    print(f"\n✅ Added event: {title}")
    print(f"   📅 {date} at {time}")
    print(f"   📍 {location}")
    print(f"   🏆 {points} points")
    if free_food:
        print("   🍕 Free food!")

def list_events():
    """List all current events"""
    print("📅 Current LMU Events")
    print("=" * 30)
    
    events_file = "data/events/current_events.json"
    
    if not os.path.exists(events_file):
        print("❌ No events file found. Run setup first.")
        return
    
    try:
        with open(events_file, 'r') as f:
            events = json.load(f)
    except:
        print("❌ Error reading events file")
        return
    
    if not events:
        print("📝 No events currently scheduled")
        return
    
    # Sort events by date
    events.sort(key=lambda x: x.get('date', ''))
    
    for i, event in enumerate(events, 1):
        print(f"\n{i}. {event['title']}")
        print(f"   📅 {event.get('date', 'TBD')} at {event.get('time', 'TBD')}")
        print(f"   📍 {event.get('location', 'TBD')}")
        print(f"   📝 {event.get('description', 'No description')}")
        print(f"   🏷️ Category: {event.get('category', 'Other')}")
        print(f"   🏆 Points: {event.get('points', 5)}")
        
        if event.get('free_food'):
            print("   🍕 Free food!")
        
        if event.get('contact'):
            print(f"   📧 Contact: {event['contact']}")

def remove_old_events():
    """Remove events that have already passed"""
    print("🧹 Cleaning up old events...")
    
    events_file = "data/events/current_events.json"
    
    if not os.path.exists(events_file):
        print("❌ No events file found")
        return
    
    try:
        with open(events_file, 'r') as f:
            events = json.load(f)
    except:
        print("❌ Error reading events file")
        return
    
    today = datetime.now().date()
    original_count = len(events)
    
    # Filter out old events
    current_events = []
    for event in events:
        try:
            event_date = datetime.strptime(event.get('date', ''), '%Y-%m-%d').date()
            if event_date >= today:
                current_events.append(event)
        except:
            # Keep events with invalid dates
            current_events.append(event)
    
    # Save updated events
    with open(events_file, 'w') as f:
        json.dump(current_events, f, indent=2)
    
    removed_count = original_count - len(current_events)
    print(f"✅ Removed {removed_count} old events")
    print(f"📅 {len(current_events)} current events remaining")

def generate_sample_week():
    """Generate sample events for the upcoming week"""
    print("📝 Generating sample events for the week...")
    
    now = datetime.now()
    sample_events = []
    
    # Generate events for the next 7 days
    for i in range(7):
        date = (now + timedelta(days=i)).strftime("%Y-%m-%d")
        day_name = (now + timedelta(days=i)).strftime("%A")
        
        if i == 0:  # Today
            sample_events.append({
                "title": "Study Group - Calculus",
                "description": "Join fellow students for a calculus study session. Bring your homework!",
                "date": date,
                "time": "4:00 PM - 6:00 PM",
                "location": "Library Study Room 3B",
                "category": "Academic",
                "free_food": False,
                "points": 3,
                "contact": "mathtutor@lmu.edu"
            })
        elif i == 1:  # Tomorrow
            sample_events.append({
                "title": "Career Workshop: Resume Building",
                "description": "Learn how to create a standout resume with Career Services. Pizza provided!",
                "date": date,
                "time": "12:00 PM - 1:30 PM",
                "location": "Student Union Room 201",
                "category": "Career",
                "free_food": True,
                "points": 5,
                "contact": "career@lmu.edu"
            })
        elif i == 2:  # Day after tomorrow
            sample_events.append({
                "title": "Mindfulness Meditation Session",
                "description": "Relax and recharge with a guided meditation session hosted by CPS.",
                "date": date,
                "time": "6:00 PM - 7:00 PM",
                "location": "Foley Annex Wellness Room",
                "category": "Wellness",
                "free_food": True,
                "points": 4,
                "contact": "cps@lmu.edu"
            })
        elif day_name == "Friday":
            sample_events.append({
                "title": "Lions Basketball Game",
                "description": "Cheer on the Lions! Free t-shirts for the first 100 students.",
                "date": date,
                "time": "7:00 PM",
                "location": "Gersten Pavilion",
                "category": "Athletics",
                "free_food": False,
                "points": 5,
                "contact": "athletics@lmu.edu"
            })
        elif day_name == "Saturday":
            sample_events.append({
                "title": "Community Service: Beach Cleanup",
                "description": "Help clean up Manhattan Beach with the Environmental Club. Lunch included!",
                "date": date,
                "time": "9:00 AM - 1:00 PM",
                "location": "Manhattan Beach Pier",
                "category": "Service",
                "free_food": True,
                "points": 8,
                "contact": "enviro@lmu.edu"
            })
    
    # Save sample events
    events_file = "data/events/current_events.json"
    os.makedirs(os.path.dirname(events_file), exist_ok=True)
    
    with open(events_file, 'w') as f:
        json.dump(sample_events, f, indent=2)
    
    print(f"✅ Generated {len(sample_events)} sample events")

def main():
    """Main function with menu"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update LMU Events")
    parser.add_argument("--add", action="store_true", help="Add a custom event")
    parser.add_argument("--list", action="store_true", help="List all events")
    parser.add_argument("--clean", action="store_true", help="Remove old events")
    parser.add_argument("--sample", action="store_true", help="Generate sample events")
    
    args = parser.parse_args()
    
    if args.add:
        add_custom_event()
    elif args.list:
        list_events()
    elif args.clean:
        remove_old_events()
    elif args.sample:
        generate_sample_week()
    else:
        # Default: update events
        update_events()

if __name__ == "__main__":
    main()