import json
import os

HIGHSCORE_FILE = "highscore.json"

def load_highscore():
    """Load highscore from file."""
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('score', 0)
        except:
            return 0
    return 0

def save_highscore(score):
    """Save highscore to file."""
    data = {'score': score}
    with open(HIGHSCORE_FILE, 'w') as f:
        json.dump(data, f)

def update_highscore(current_score):
    """Update highscore if current score is higher. Returns updated highscore."""
    high = load_highscore()
    if current_score > high:
        save_highscore(current_score)
        return current_score
    return high
