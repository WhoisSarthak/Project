import pygame
import sys
from main_game import run_game
from highscore import load_highscore, update_highscore

# ============================
# Home Screen
# ============================
def home_screen(screen, clock):
    """Main menu screen."""
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_option = pygame.font.SysFont("consolas", 32)

    options = ["Start", "High Score", "Quit"]
    selected_index = 0

    while True:
        screen.fill((20, 20, 30))

        title = font_title.render("Zombie Deflect", True, (200, 220, 255))
        screen.blit(title, title.get_rect(center=(400, 120)))

        subtitle = pygame.font.SysFont("consolas", 24).render("10 Rooms | 10 Levels Each", True, (150, 150, 200))
        screen.blit(subtitle, subtitle.get_rect(center=(400, 180)))

        option_rects = []
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_index else (150, 150, 150)
            surf = font_option.render(option, True, color)
            rect = surf.get_rect(center=(400, 280 + i * 80))
            screen.blit(surf, rect)
            option_rects.append(rect)

            if rect.collidepoint(pygame.mouse.get_pos()):
                selected_index = i

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected_index]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            return options[i]

        clock.tick(60)

# ============================
# Difficulty Screen
# ============================
def difficulty_screen(screen, clock):
    """Select difficulty before starting."""
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_option = pygame.font.SysFont("consolas", 32)
    font_small = pygame.font.SysFont("consolas", 18)

    options = ["Easy", "Medium", "Hard"]
    descriptions = [
        "Slower projectiles, longer intervals",
        "Standard speed and intervals",
        "Faster projectiles, tighter timing"
    ]
    selected_index = 0

    while True:
        screen.fill((25, 25, 35))

        title = font_title.render("Select Difficulty", True, (200, 220, 255))
        screen.blit(title, title.get_rect(center=(400, 100)))

        option_rects = []
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_index else (150, 150, 150)
            surf = font_option.render(option, True, color)
            rect = surf.get_rect(center=(400, 220 + i * 90))
            screen.blit(surf, rect)
            option_rects.append(rect)

            # Description
            desc = font_small.render(descriptions[i], True, (100, 100, 150))
            screen.blit(desc, desc.get_rect(center=(400, 255 + i * 90)))

            if rect.collidepoint(pygame.mouse.get_pos()):
                selected_index = i

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected_index]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            return options[i]

        clock.tick(60)

# ============================
# High Score Screen
# ============================
def highscore_screen(screen, clock):
    """Display and manage high scores."""
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_option = pygame.font.SysFont("consolas", 32)
    font_small = pygame.font.SysFont("consolas", 20)

    highscore = load_highscore()

    while True:
        screen.fill((30, 30, 40))

        title = font_title.render("High Score", True, (255, 200, 100))
        screen.blit(title, title.get_rect(center=(400, 150)))

        if highscore > 0:
            score_text = font_option.render(str(highscore), True, (100, 255, 100))
            screen.blit(score_text, score_text.get_rect(center=(400, 280)))
        else:
            no_score = font_option.render("No score yet", True, (150, 150, 150))
            screen.blit(no_score, no_score.get_rect(center=(400, 280)))

        back = font_small.render("Press ESC to return to menu", True, (150, 150, 150))
        screen.blit(back, back.get_rect(center=(400, 420)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(60)

# ============================
# Main
# ============================
def main():
    """Main menu loop."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Zombie Deflect")
    clock = pygame.time.Clock()

    difficulty = "Medium"  # Default difficulty

    while True:
        choice = home_screen(screen, clock)

        if choice == "Start":
            difficulty = difficulty_screen(screen, clock)
            final_score = run_game(screen, clock, difficulty)
            # Update highscore and show results
            if final_score > 0:
                high = update_highscore(final_score)
                show_results(screen, clock, final_score, high)
        
        elif choice == "High Score":
            highscore_screen(screen, clock)
        
        elif choice == "Quit":
            pygame.quit()
            sys.exit()

def show_results(screen, clock, score, highscore):
    """Show game results after completion."""
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_option = pygame.font.SysFont("consolas", 32)

    while True:
        screen.fill((20, 40, 20))

        if score >= 100:
            title = font_title.render("YOU WIN!", True, (100, 255, 100))
        else:
            title = font_title.render("Game Over", True, (255, 100, 100))

        screen.blit(title, title.get_rect(center=(400, 120)))

        score_text = font_option.render(f"Score: {score}", True, (200, 200, 255))
        screen.blit(score_text, score_text.get_rect(center=(400, 220)))

        if score == highscore:
            new_high = font_option.render("New High Score!", True, (255, 200, 100))
            screen.blit(new_high, new_high.get_rect(center=(400, 280)))

        back = font_option.render("Press ESC to return", True, (150, 150, 150))
        screen.blit(back, back.get_rect(center=(400, 380)))

        pygame.display.flip()

        for event in pygame.event.get():wd
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(60)

if __name__ == "__main__":
    main()
