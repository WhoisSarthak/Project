import pygame
import os

# Asset paths
ZOMBIE_FOLDER = "assets/zombie"  # Folder containing idle.png, attack.png, dead.png
PLAYER_IMG = "assest/player/idle.png"
ZOMBIE_IMG = "assets/zombie.png"
PROJECTILE_IMG = "assets/projectile.png"
SWORD_IMG = "assets/sword.png"

# Animation frame counts (frames arranged horizontally in each PNG)
ANIMATIONS = {
    "idle": 6,      # idle.png has 6 frames
    "attack": 4,    # attack.png has 4 frames
    "dead": 5,      # dead.png has 5 frames
}

# Cache for loaded sprite frames
_sprite_cache = {}

# Cache for zombie animated sprites
_zombie_sprites = {}


def load_image(path, width, height):
    """Load image from path, return scaled surface or None if not found."""
    if os.path.exists(path):
        try:
            img = pygame.image.load(path)
            return pygame.transform.scale(img, (width, height))
        except:
            return None
    return None


def extract_frames_from_animation_png(animation_name, frame_count):
    """
    Extract animation frames from individual animation PNG files.
    Frames are arranged horizontally in the PNG.
    Returns list of pygame surfaces for each frame.
    """
    cache_key = f"{animation_name}"
    if cache_key in _sprite_cache:
        return _sprite_cache[cache_key]
    
    # Build path: assets/zombie/idle.png, assets/zombie/attack.png, etc.
    animation_path = os.path.join(ZOMBIE_FOLDER, f"{animation_name}.png")
    
    if not os.path.exists(animation_path):
        print(f"Warning: Animation file not found: {animation_path}")
        return None
    
    try:
        animation_img = pygame.image.load(animation_path)
        img_width, img_height = animation_img.get_size()
        
        # Calculate individual frame dimensions
        frame_width = img_width // frame_count
        frame_height = img_height
        
        frames = []
        
        # Extract each frame from the horizontal strip
        for frame_idx in range(frame_count):
            frame_x = frame_idx * frame_width
            # Extract frame from animation PNG
            frame_rect = pygame.Rect(frame_x, 0, frame_width, frame_height)
            frame_surface = animation_img.subsurface(frame_rect)
            frame_copy = frame_surface.copy()
            frames.append(frame_copy)
        
        _sprite_cache[cache_key] = frames
        return frames
    except Exception as e:
        print(f"Error loading animation {animation_name}: {e}")
        return None


class AnimatedSprite:
    """Handles sprite animation from individual animation PNG files."""
    
    def __init__(self, animation_name, scale_width=None, scale_height=None):
        self.animation_name = animation_name
        if animation_name in ANIMATIONS:
            self.frames = extract_frames_from_animation_png(animation_name, ANIMATIONS[animation_name])
        else:
            self.frames = None
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.1  # seconds per frame
        self.scale_width = scale_width
        self.scale_height = scale_height
    
    def update(self, dt):
        """Update animation frame."""
        if self.frames:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer -= self.frame_duration
                self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def draw(self, screen, x, y):
        """Draw current animation frame."""
        if not self.frames:
            return False
        
        frame = self.frames[self.current_frame]
        if self.scale_width and self.scale_height:
            frame = pygame.transform.scale(frame, (self.scale_width, self.scale_height))
        
        screen.blit(frame, (int(x), int(y)))
        return True
    
    def set_animation(self, animation_name):
        """Change animation."""
        if animation_name != self.animation_name:
            self.animation_name = animation_name
            if animation_name in ANIMATIONS:
                self.frames = extract_frames_from_animation_png(animation_name, ANIMATIONS[animation_name])
            self.current_frame = 0
            self.animation_timer = 0


def draw_player(screen, x, y, radius):
    """Draw player - image or circle."""
    img = load_image(PLAYER_IMG, radius * 2, radius * 2)
    if img:
        screen.blit(img, (int(x) - radius, int(y) - radius))
    else:
        pygame.draw.circle(screen, (50, 200, 220), (int(x), int(y)), radius)


def draw_zombie(screen, x, y, radius, king=False):
    """Draw zombie - animated sprite or circle."""
    # Use animated sprite if available
    sprite_key = "king" if king else "regular"
    if sprite_key not in _zombie_sprites:
        # Create animated sprite for idle animation
        _zombie_sprites[sprite_key] = AnimatedSprite("idle", scale_width=radius * 2, scale_height=radius * 2)
    
    sprite = _zombie_sprites[sprite_key]
    if not sprite.draw(screen, int(x) - radius, int(y) - radius):
        # Fallback to circle if animation not found
        color = (180, 0, 180) if king else (170, 60, 60)
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)


def draw_projectile(screen, x, y, radius, is_king=False):
    """Draw projectile (brain) - image or circle."""
    img = load_image(PROJECTILE_IMG, radius * 2, radius * 2)
    if img:
        screen.blit(img, (int(x) - radius, int(y) - radius))
    else:
        color = (255, 140, 0) if is_king else (230, 70, 70)
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)


def draw_blade(screen, x1, y1, x2, y2, width):
    """Draw blade (sword) - image or line."""
    # Draw as a more pronounced line (like a sword)
    pygame.draw.line(screen, (150, 200, 255), (x1, y1), (x2, y2), width)
    # Add a glow effect
    pygame.draw.line(screen, (100, 150, 255), (x1, y1), (x2, y2), max(1, width - 2))
