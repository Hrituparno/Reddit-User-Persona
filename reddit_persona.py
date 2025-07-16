import praw
import spacy
import re
import os
from urllib.parse import urlparse
from datetime import datetime
from textblob import TextBlob  # Added for sentiment analysis

# TODO: Replace with your actual Reddit API credentials
REDDIT_CLIENT_ID = "oOZHJ5jrbQcUd2PIaz_v3g"
REDDIT_CLIENT_SECRET = "augmf8Wz_ohiikjLw9SsZu7zwI0h1g"
REDDIT_USER_AGENT = "BeyondChatsInternship/1.0 by Inspection-Solid"

# Moved interest_keywords to global scope
interest_keywords = {
    'gaming': ['game', 'gaming', 'playstation', 'xbox', 'nintendo'],
    'technology': ['tech', 'programming', 'software', 'computer'],
    'sports': ['sport', 'football', 'basketball', 'soccer'],
    'books': ['book', 'reading', 'novel', 'literature'],
    'music': ['music', 'band', 'song', 'album']
}

def initialize_reddit():
    """Initialize Reddit API client with PRAW."""
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

def extract_username(url):
    """Extract username from Reddit profile URL."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    if 'user' in path_parts:
        return path_parts[path_parts.index('user') + 1]
    raise ValueError("Invalid Reddit profile URL")

def fetch_user_data(reddit, username):
    """Fetch posts and comments for a given Reddit user."""
    try:
        redditor = reddit.redditor(username)
        posts = list(redditor.submissions.new(limit=50))
        comments = list(redditor.comments.new(limit=50))
        return posts, comments
    except Exception as e:
        raise Exception(f"Error fetching data for {username}: {str(e)}")

def analyze_text(nlp, text):
    """Analyze text to extract interests and personality traits."""
    doc = nlp(text)
    interests = set()
    personality = set()
    
    # Simple keyword-based analysis for interests
    for token in doc:
        for category, keywords in interest_keywords.items():
            if any(keyword in token.text.lower() for keyword in keywords):
                interests.add(category)
    
    # Sentiment analysis for personality using TextBlob
    blob = TextBlob(text)
    sentiment = float(getattr(blob.sentiment, "polarity", 0.0))
    if sentiment > 0.1:
        personality.add("Positive")
    elif sentiment < -0.1:
        personality.add("Negative")
    else:
        personality.add("Neutral")
    
    return interests, personality

def build_persona(posts, comments):
    """Build user persona based on posts and comments."""
    nlp = spacy.load("en_core_web_sm")
    persona = {"Interests": [], "Personality": []}
    citations = []
    
    # Combine all text from posts and comments
    all_text = ""
    for post in posts:
        all_text += (post.title + " " + (post.selftext or "") + " ")
        citations.append((f"Post: {post.title}", f"https://reddit.com{post.permalink}"))
    
    for comment in comments:
        all_text += comment.body + " "
        citations.append((f"Comment: {comment.body[:50]}...", f"https://reddit.com{comment.permalink}"))
    
    # Analyze combined text
    interests, personality = analyze_text(nlp, all_text)
    
    # Populate persona
    for interest in interests:
        relevant_citations = [cit for cit, url in citations if any(keyword in cit.lower() for keyword in interest_keywords.get(interest, []))]
        persona["Interests"].append((interest, relevant_citations or ["No specific citation"]))
    
    for trait in personality:
        persona["Personality"].append((trait, ["Based on overall sentiment analysis"]))
    
    return persona, citations

def save_persona_to_file(username, persona, citations, output_dir="output"):
    """Save user persona to a text file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"{output_dir}/{username}_persona.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"User Persona for u/{username}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Interests:\n")
        for interest, cites in persona["Interests"]:
            f.write(f"- {interest}\n")
            for cite in cites:
                f.write(f"  - Source: {cite}\n")
        
        f.write("\nPersonality:\n")
        for trait, cites in persona["Personality"]:
            f.write(f"- {trait}\n")
            for cite in cites:
                f.write(f"  - Source: {cite}\n")
        
        f.write("\nAll Citations:\n")
        for i, (text, url) in enumerate(citations, 1):
            f.write(f"{i}. {text}\n   URL: {url}\n")
    
    return filename

def main():
    """Main function to process Reddit user profile and generate persona."""
    reddit_url = input("Enter Reddit user profile URL: ")
    try:
        reddit = initialize_reddit()
        username = extract_username(reddit_url)
        posts, comments = fetch_user_data(reddit, username)
        persona, citations = build_persona(posts, comments)
        filename = save_persona_to_file(username, persona, citations)
        print(f"Persona generated and saved to {filename}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()