import random

class Room:
    """Manages a room with multiple levels and zombies."""
    
    def __init__(self, room_number, screen_width, screen_height, zombie_class):
        self.room_number = room_number  # 1-10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_level = 1
        self.max_levels = 10
        self.zombies = []
        self.zombie_class = zombie_class
        self.base_difficulty = room_number - 1  # Room 1 has 0, Room 10 has 9
        
    def generate_zombies(self):
        """Generate zombies for current level."""
        self.zombies.clear()
        # More zombies as level increases
        num_zombies = 1 + (self.current_level + self.base_difficulty) // 3
        
        for i in range(num_zombies):
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(50, min(200, self.screen_height // 3))
            # First zombie is always the king
            king = (i == 0)
            effective_level = self.current_level + self.base_difficulty
            self.zombies.append(self.zombie_class(x, y, effective_level, king=king))
    
    def advance_level(self):
        """Move to next level in room. Returns True if level advanced, False if room cleared."""
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.generate_zombies()
            return True
        return False  # Room cleared
    
    def get_info(self):
        """Return formatted room and level info."""
        return f"Room {self.room_number}/10 | Level {self.current_level}/10"
