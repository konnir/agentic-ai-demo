import pygame
import random
import sys

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agentic AI Warriors (Pygame)")

# Fonts
font = pygame.font.SysFont("Arial", 20, bold=True)
info_font = pygame.font.SysFont("Arial", 16)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Frame rate
clock = pygame.time.Clock()

class AgenticWarrior:
    """
    Demonstrates a simple "agentic AI" within a warrior framework:
      1) perceive environment & opponent status
      2) decide next action
      3) act on that decision
    """
    def __init__(self, name, health=30):
        self.name = name
        self.health = health

    def perceive(self, opponent):
        """
        (1) PERCEIVE:
            Gather data about the environment (here, just a random event)
            and the opponent's status (is opponent alive or not).
        """
        random_event = random.choice(['heal', 'boost', 'nothing'])
        if opponent.health > 0:
            perceived_threat = "threat"
        else:
            perceived_threat = "no_threat"
        return perceived_threat, random_event

    def decide_action(self, perception):
        """
        (2) DECIDE:
            Given the threat level and random event:
             - If there's no threat, celebrate.
             - If we get a 'heal' event & health is low, heal.
             - If we get a 'boost' event, attack.
             - Otherwise randomly attack or defend.
        """
        perceived_threat, random_event = perception

        if perceived_threat == "no_threat":
            return "celebrate"

        if random_event == 'heal' and self.health < 15:
            return "heal"
        elif random_event == 'boost':
            return "attack"
        else:
            return random.choice(["attack", "defend"])

    def act(self, action, opponent):
        """
        (3) ACT:
            Execute the chosen action, affecting the environment
            (opponent's health) or the warrior's own health.
        """
        if action == "attack":
            dmg = random.randint(5, 10)
            opponent.health -= dmg
            return f"{self.name} attacks {opponent.name} for {dmg} damage!"
        elif action == "defend":
            return f"{self.name} defends!"
        elif action == "heal":
            heal_amt = random.randint(5, 10)
            self.health += heal_amt
            return f"{self.name} heals for {heal_amt} HP!"
        elif action == "celebrate":
            return f"{self.name} celebrates (opponent down)!"
        else:
            return f"{self.name} waits..."

# Create two agentic warriors
warrior1 = AgenticWarrior("Thor", 30)
warrior2 = AgenticWarrior("Loki", 30)

battle_over = False
round_number = 1
info_lines = ["Press SPACE to start the fight!"]

def health_to_color(health):
    """Return a color (green, orange, or red) based on health thresholds."""
    if health > 20:
        return GREEN
    elif health > 10:
        return ORANGE
    else:
        return RED

def draw_screen():
    """Render the warriors, health bars, and the recent fight logs."""
    screen.fill(WHITE)

    # Title
    title_surf = font.render("Agentic AI Warriors (Press SPACE Each Round)", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 10))

    # Warrior 1
    w1_color = health_to_color(warrior1.health)
    w1_width = max(0, int((warrior1.health / 30) * 100))
    pygame.draw.rect(screen, w1_color, (50, 80, w1_width, 40))
    w1_label_surf = font.render(f"{warrior1.name} (HP: {warrior1.health})", True, BLACK)
    screen.blit(w1_label_surf, (50, 50))

    # Warrior 2
    w2_color = health_to_color(warrior2.health)
    w2_width = max(0, int((warrior2.health / 30) * 100))
    pygame.draw.rect(screen, w2_color, (450, 80, w2_width, 40))
    w2_label_surf = font.render(f"{warrior2.name} (HP: {warrior2.health})", True, BLACK)
    screen.blit(w2_label_surf, (450, 50))

    # Show last few info lines
    y_offset = 150
    for line in info_lines[-4:]:  # Show up to last 4 lines
        info_surf = info_font.render(line, True, BLACK)
        screen.blit(info_surf, (50, y_offset))
        y_offset += 20

    pygame.display.flip()

def next_round():
    """Handle one round of the fight if it's not over."""
    global round_number, battle_over

    if battle_over:
        info_lines.append("The battle is already over!")
        return

    round_texts = [f"--- Round {round_number} ---"]

    # Warrior1's turn (Perceive -> Decide -> Act)
    perception1 = warrior1.perceive(warrior2)
    action1 = warrior1.decide_action(perception1)
    text1 = warrior1.act(action1, warrior2)
    round_texts.append(text1)

    # Check if Warrior2 is defeated
    if warrior2.health <= 0:
        round_texts.append(f"{warrior2.name} is defeated! {warrior1.name} wins!")
        battle_over = True
    else:
        # Warrior2's turn (Perceive -> Decide -> Act)
        perception2 = warrior2.perceive(warrior1)
        action2 = warrior2.decide_action(perception2)
        text2 = warrior2.act(action2, warrior1)
        round_texts.append(text2)

        if warrior1.health <= 0:
            round_texts.append(f"{warrior1.name} is defeated! {warrior2.name} wins!")
            battle_over = True

    # Increment round number and add text lines
    round_number += 1
    info_lines.extend(round_texts)

# Main loop
while True:
    clock.tick(30)  # 30 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Press SPACE to trigger next round
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            next_round()

    draw_screen()