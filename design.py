import pygame
import os

# Asset paths
PLAYER_IMG = "assest/player/idle.png"
ZOMBIE_IMG = "assest/zombie/zombieidle.png"
ZOMBIE_KING_IMG = "assest/zombie/king.png"
PROJECTILE_IMG = "assest/projectile.png"
SWORD_IMG = "assest/sword.png"



# Cache for loaded images
_image_cache = {}


def load_image(path, width, height):
    """Load image from path, return scaled surface or None if not found. Uses caching."""
    cache_key = (path, width, height)
    
    if cache_key in _image_cache:
        return _image_cache[cache_key]
    
    if os.path.exists(path):
        try:
            img = pygame.image.load(path)
            scaled = pygame.transform.scale(img, (width, height))
            _image_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None
    return None





def draw_player(screen, x, y, radius):
    """Draw player - image or circle."""
    img = load_image(PLAYER_IMG, radius * 4, radius * 4)
    if img:
        screen.blit(img, (int(x) - radius * 2, int(y) - radius * 2))
    else:
        pygame.draw.circle(screen, (50, 200, 220), (int(x), int(y)), radius)


def draw_zombie(screen, x, y, radius, king=False, dt=0.016):
    """Draw zombie - image or circle."""
    img_path = ZOMBIE_KING_IMG if king else ZOMBIE_IMG
    img = load_image(img_path, radius * 6, radius * 6)
    if img:
        screen.blit(img, (int(x) - radius * 3, int(y) - radius * 3))
    else:
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
