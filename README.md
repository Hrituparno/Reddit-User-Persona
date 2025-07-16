# Reddit User Persona Scraper

This repository contains a Python script developed for the BeyondChats AI/LLM Engineer Intern assignment. The script scrapes a Reddit user's posts and comments, builds a user persona based on their activity, and saves the output to a text file with citations.

## Features
- Accepts a Reddit user profile URL as input (e.g., https://www.reddit.com/user/kojied/).
- Scrapes up to 50 recent posts and comments using the Reddit API (PRAW).
- Analyzes text using spaCy for interests and TextBlob for sentiment-based personality traits.
- Generates a user persona with interests and personality traits, citing specific posts/comments.
- Saves the persona to a text file (`<username>_persona.txt`) in an `output` directory.
- Follows PEP-8 guidelines for clean, readable code.

## Prerequisites
- Python 3.8+
- Reddit API credentials (Client ID, Client Secret, User Agent)
- Required Python packages (listed in `requirements.txt`)

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Reddit API Credentials**
   - Obtain Reddit API credentials from [Reddit Apps](https://www.reddit.com/prefs/apps).
   - Update the script (`RedditPersonaScraper.py`) with your credentials:
     ```python
     REDDIT_CLIENT_ID = "your_reddit_client_id"
     REDDIT_CLIENT_SECRET = "your_reddit_client_secret"
     REDDIT_USER_AGENT = "your_reddit_user_agent"
     ```
   - Alternatively, store credentials securely in a `.env` file (not included in this repository for security).

4. **Run the Script**
   ```bash
   python RedditPersonaScraper.py
   ```
   - Enter a Reddit user profile URL when prompted (e.g., https://www.reddit.com/user/kojied/).
   - The script will scrape data, generate a persona, and save it to `output/<username>_persona.txt`.

## Sample Output
Sample persona files for the provided users are included:
- `output/kojied_persona.txt`
- `output/Hungry-Move-6603_persona.txt`

**Example Output File (`kojied_persona.txt`):**
```
User Persona for u/kojied
==================================================

Interests:
- gaming
  - Source: Post: My favorite RPG this year
- technology
  - Source: Comment: Excited about new Python release...

Personality:
- Positive
  - Source: Based on overall sentiment analysis

All Citations:
1. Post: My favorite RPG this year
   URL: https://reddit.com/r/gaming/comments/abc123/...
2. Comment: Excited about new Python release...
   URL: https://reddit.com/r/technology/comments/xyz789/...
```

## Repository Structure
- `RedditPersonaScraper.py`: Main script for scraping and generating personas.
- `requirements.txt`: Lists required Python packages.
- `output/`: Directory containing generated persona text files.
- `README.md`: This file with setup and usage instructions.

## Notes
- Ensure your GitHub repository is public for evaluation by the BeyondChats team.
- The script uses keyword-based interest detection and sentiment analysis for simplicity; you can extend it with more advanced NLP techniques.
- Error handling is implemented to manage invalid URLs or API issues.
- Sample persona files are placeholders; run the script with actual Reddit URLs to generate real outputs.

## Example Usage
```bash
Enter Reddit user profile URL: https://www.reddit.com/user/kojied/
Persona generated and saved to output/kojied_persona.txt
```

