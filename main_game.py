import pygame
import sys
import math
import random
from room import Room
from design import draw_player, draw_zombie, draw_projectile, draw_blade

# ============================
# Utility Functions
# ============================
def normalize(vx, vy):
    """Normalize a vector."""
    mag = math.hypot(vx, vy)
    return (0, 0) if mag == 0 else (vx / mag, vy / mag)

# ============================
# Pause Screen
# ============================
def pause_screen(screen, clock):
    """Show pause menu."""
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_option = pygame.font.SysFont("consolas", 32)

    while True:
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("PAUSED", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(400, 200)))

        resume = font_option.render("Press P to Resume", True, (150, 200, 255))
        screen.blit(resume, resume.get_rect(center=(400, 320)))

        menu = font_option.render("Press M for Menu", True, (150, 150, 150))
        screen.blit(menu, menu.get_rect(center=(400, 380)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"
                elif event.key == pygame.K_m:
                    return "menu"

        clock.tick(60)

# ============================
# Classes
# ============================
class Player:
    """Player character."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 16
        self.max_hp = 100
        self.hp = self.max_hp
        self.blade = Blade(self)
        self.speed = 200

    def update(self, keys, dt):
        """Update player position and blade."""
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        dx, dy = normalize(dx, dy)
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        # Clamp to screen
        self.x = max(self.radius, min(800 - self.radius, self.x))
        self.y = max(self.radius, min(600 - self.radius, self.y))

        self.blade.update(dt)

    def draw(self, screen):
        """Draw player and blade."""
        draw_player(screen, self.x, self.y, self.radius)
        self.blade.draw(screen)

    def take_damage(self, amount):
        """Reduce HP."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        """Check if player is alive."""
        return self.hp > 0

class Blade:
    """Player's blade weapon."""
    
    def __init__(self, player):
        self.player = player
        self.active = False
        self.elapsed = 0
        self.duration = 0.15
        self.length = 60
        self.width = 8
        self.tip = (0, 0)
        self.target_angle = 0

    def swing(self, mx, my):
        """Trigger blade swing toward mouse position."""
        if not self.active:
            self.active = True
            self.elapsed = 0
            self.target_angle = math.degrees(math.atan2(
                my - self.player.y, 
                mx - self.player.x
            ))

    def update(self, dt):
        """Update blade animation."""
        if not self.active:
            return
        
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
            return

        progress = self.elapsed / self.duration
        angle = self.target_angle - 90 + 180 * progress
        rad = math.radians(angle)
        self.tip = (
            self.player.x + math.cos(rad) * self.length,
            self.player.y + math.sin(rad) * self.length
        )

    def draw(self, screen):
        """Draw blade if active."""
        if self.active:
            draw_blade(
                screen,
                self.player.x,
                self.player.y,
                self.tip[0],
                self.tip[1],
                self.width
            )

    def get_tip(self):
        """Return blade tip position."""
        return self.tip if self.active else None

class Projectile:
    """Zombie projectile."""
    
    def __init__(self, x, y, target_x, target_y, owner):
        self.x = x
        self.y = y
        dx, dy = normalize(target_x - x, target_y - y)
        self.vx = dx * 250
        self.vy = dy * 250
        self.radius = 8
        self.alive = True
        self.chopped = False
        self.owner = owner

    def update(self, dt):
        """Update projectile position."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, screen):
        """Draw projectile."""
        if self.alive:
            draw_projectile(screen, self.x, self.y, self.radius, self.owner.king)

    def is_alive(self):
        """Check if projectile is alive."""
        return self.alive

    def chop(self):
        """Mark projectile as chopped."""
        self.alive = False
        self.chopped = True
        self.owner.vulnerable = True

class Zombie:
    """Enemy zombie."""
    
    def __init__(self, x, y, level, king=False):
        self.x = x
        self.y = y
        self.radius = 20
        self.level = level
        self.king = king
        self.vulnerable = False
        self.throw_timer = 0
        self.alive = True

    def update(self, dt, player, projectiles, difficulty):
        """Update zombie behavior."""
        self.throw_timer += dt
        
        # Base throw interval decreased with level
        base_interval = 1.5
        level_factor = 0.05
        difficulty_factor = {"Easy": 1.0, "Medium": 0.8, "Hard": 0.6}[difficulty]
        
        interval = max(0.2, base_interval - self.level * level_factor) * difficulty_factor

        if self.throw_timer >= interval and self.alive:
            self.throw_timer = 0
            projectiles.append(Projectile(self.x, self.y, player.x, player.y, self))

    def draw(self, screen):
        """Draw zombie."""
        if not self.alive:
            return
        draw_zombie(screen, self.x, self.y, self.radius, self.king)

    def is_alive(self):
        """Check if zombie is alive."""
        return self.alive

# ============================
# Main Game Loop
# ============================
def run_game(screen, clock, difficulty):
    """Main game loop with room progression."""
    
    # Initialize
    player = Player(400, 500)
    current_room = 1
    room = Room(current_room, 800, 600, Zombie)
    room.generate_zombies()
    projectiles = []
    
    final_score = 0

    while True:
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    action = pause_screen(screen, clock)
                    if action == "menu":
                        return final_score
                
                if event.key == pygame.K_ESCAPE:
                    return final_score
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                player.blade.swing(mx, my)

        # Update
        player.update(keys, dt)
        
        for z in room.zombies:
            z.update(dt, player, projectiles, difficulty)
        
        for p in projectiles:
            p.update(dt)

        # Blade collision with projectiles
        blade_tip = player.blade.get_tip()
        if blade_tip:
            bx, by = blade_tip
            for p in projectiles:
                if p.is_alive() and math.hypot(p.x - bx, p.y - by) < 20:
                    p.chop()

        # Projectile collision with player
        for p in projectiles:
            if p.is_alive() and math.hypot(p.x - player.x, p.y - player.y) < player.radius + p.radius:
                player.take_damage(10)
                p.alive = False
                
                if not player.is_alive():
                    # Calculate final score
                    final_score = (current_room - 1) * 10 + room.current_level
                    return final_score

        # Blade collision with zombies
        if blade_tip and player.blade.active:
            bx, by = blade_tip
            blade_hit = False
            for z in room.zombies:
                dist = math.hypot(z.x - bx, z.y - by)
                # Collision radius is half the visual image size (image is radius*6, so collision is radius*3)
                collision_radius = z.radius * 3
                if z.is_alive() and z.vulnerable and dist < collision_radius:
                    z.alive = False
                    blade_hit = True
                    
                    if z.king:
                        # King zombie killed
                        if not room.advance_level():
                            # Room cleared
                            current_room += 1
                            
                            if current_room > 10:
                                # All rooms cleared - WIN!
                                final_score = 100
                                return final_score
                            
                            # Start new room
                            room = Room(current_room, 800, 600, Zombie)
                            room.generate_zombies()
                        
                        projectiles.clear()
            
            # Reset zombie vulnerability after blade hit
            if blade_hit:
                for z in room.zombies:
                    z.vulnerable = False

        # Render
        screen.fill((15, 15, 20))
        
        player.draw(screen)
        for z in room.zombies:
            z.draw(screen)
        for p in projectiles:
            p.draw(screen)

        # HUD
        font = pygame.font.SysFont("consolas", 20)
        room_info = room.get_info()
        hud = font.render(f"{room_info} | {difficulty} | HP {player.hp}/{player.max_hp}", True, (255, 255, 255))
        screen.blit(hud, (10, 10))
        
        # HP Bar
        bar_width = 150
        bar_height = 20
        bar_x = 10
        bar_y = 35
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_ratio = max(0, player.hp / player.max_hp)
        health_color = (100, 255, 100) if health_ratio > 0.5 else (255, 200, 0) if health_ratio > 0.25 else (255, 50, 50)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        
        # Border
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)

        pygame.display.flip()
