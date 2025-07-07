"""Utility functions for Canal & River Trust integration."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any


def parse_date(date_str: str | None) -> str | None:
    """Parse date string from API response."""
    if not date_str:
        return None
    
    # Handle epoch timestamps (milliseconds)
    if isinstance(date_str, (int, float)) or (isinstance(date_str, str) and date_str.isdigit()):
        try:
            timestamp = int(date_str) / 1000 if int(date_str) > 1e10 else int(date_str)
            return datetime.fromtimestamp(timestamp).isoformat()
        except (ValueError, OSError):
            return None
    
    # Handle date strings
    if isinstance(date_str, str):
        # Try common date formats
        date_formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).isoformat()
            except ValueError:
                continue
    
    return str(date_str) if date_str else None


def clean_text(text: str | None) -> str:
    """Clean and format text from API response."""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', str(text))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common API artifacts
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    return text


def extract_waterway_name(location: str | None, waterway: str | None) -> str:
    """Extract a clean waterway name from location or waterway fields."""
    if waterway and waterway.strip():
        return clean_text(waterway)
    
    if location and location.strip():
        # Try to extract waterway name from location
        location_clean = clean_text(location)
        
        # Common patterns for waterway names in location strings
        waterway_patterns = [
            r'(.*?Canal)(?:\s|,|$)',
            r'(.*?River)(?:\s|,|$)',
            r'(.*?Navigation)(?:\s|,|$)',
            r'(.*?Waterway)(?:\s|,|$)',
        ]
        
        for pattern in waterway_patterns:
            match = re.search(pattern, location_clean, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return location_clean
    
    return "Unknown"


def categorize_issue_type(item: dict[str, Any]) -> str:
    """Categorize the type of closure or stoppage."""
    issue_type = item.get("Type", "").lower()
    reason = item.get("Reason", "").lower()
    description = item.get("Description", "").lower()
    
    combined_text = f"{issue_type} {reason} {description}"
    
    # Emergency/urgent issues
    if any(word in combined_text for word in ["emergency", "urgent", "breach", "collapse", "flood"]):
        return "Emergency"
    
    # Planned maintenance
    if any(word in combined_text for word in ["planned", "maintenance", "scheduled", "works"]):
        return "Planned Maintenance"
    
    # Lock issues
    if any(word in combined_text for word in ["lock", "gate", "chamber"]):
        return "Lock Issue"
    
    # Bridge issues
    if any(word in combined_text for word in ["bridge", "swing", "lift"]):
        return "Bridge Issue"
    
    # Water level issues
    if any(word in combined_text for word in ["water level", "low water", "high water", "drought"]):
        return "Water Level"
    
    # Vegetation/environmental
    if any(word in combined_text for word in ["vegetation", "weed", "tree", "debris"]):
        return "Environmental"
    
    return "Other"


def get_severity_level(item: dict[str, Any]) -> str:
    """Determine severity level of an issue."""
    issue_type = categorize_issue_type(item)
    status = item.get("Status", "").lower()
    
    if issue_type == "Emergency":
        return "Critical"
    
    if "closed" in status or "suspended" in status:
        return "High"
    
    if "restricted" in status or "limited" in status:
        return "Medium"
    
    return "Low"


def format_duration(start_date: str | None, end_date: str | None) -> str:
    """Format the duration of an issue."""
    if not start_date:
        return "Duration unknown"
    
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        
        if end_date:
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            duration = end - start
            
            if duration.days > 0:
                return f"{duration.days} days"
            elif duration.seconds > 3600:
                hours = duration.seconds // 3600
                return f"{hours} hours"
            else:
                minutes = duration.seconds // 60
                return f"{minutes} minutes"
        else:
            # Ongoing issue
            now = datetime.now()
            duration = now - start
            
            if duration.days > 0:
                return f"Ongoing for {duration.days} days"
            elif duration.seconds > 3600:
                hours = duration.seconds // 3600
                return f"Ongoing for {hours} hours"
            else:
                return "Recently started"
    
    except (ValueError, AttributeError):
        return "Duration unknown"
