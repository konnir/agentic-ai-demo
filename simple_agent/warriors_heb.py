import pygame
import random
import sys
from bidi.algorithm import get_display
import arabic_reshaper

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("לוחמה מבוססת סוכנים: מכבים נגד רומאים")

# Fonts (יש לוודא שהגופן תומך בעברית)
# מומלץ להשתמש בגופן שתומך בעברית כמו "Arial", "David", "FrankRuehl" וכו'
font_path = "arial.ttf"  # שנה לנתיב של גופן עברי במערכת שלך אם צריך
try:
    font = pygame.font.Font(font_path, 20)
    info_font = pygame.font.Font(font_path, 16)
except:
    # אם הגופן לא נמצא, השתמש בגופן ברירת מחדל
    font = pygame.font.SysFont("Arial", 20, bold=True)
    info_font = pygame.font.SysFont("Arial", 16)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Frame rate
clock = pygame.time.Clock()

def render_text(text, font, color):
    """
    עיבוד טקסט עברי להצגה נכונה ב-Pygame.
    """
    reshaped_text = arabic_reshaper.reshape(text)  # משנה את צורת האותיות
    bidi_text = get_display(reshaped_text)  # משנה את סדר המילים
    return font.render(bidi_text, True, color)

class AgenticWarrior:
    """
    מדגים "סוכנים אייג'נטיים" במסגרת לוחם:
      1) תופס את הסביבה ומצב היריב
      2) מחליט פעולה הבאה
      3) מבצע את הפעולה
    """
    def __init__(self, name, leader, health=30):
        self.name = name
        self.leader = leader
        self.health = health

    def perceive(self, opponent):
        """
        (1) תפיסה:
            איסוף מידע על הסביבה (כאן, אירוע אקראי בלבד)
            ומצב היריב (האם היריב חי או לא).
        """
        random_event = random.choice(['ריפוי', 'הגברה', 'שום דבר'])
        if opponent.health > 0:
            perceived_threat = "איום"
        else:
            perceived_threat = "אין איום"
        return perceived_threat, random_event

    def decide_action(self, perception):
        """
        (2) החלטה:
            בהתבסס על רמת האיום והאירוע האקראי:
             - אם אין איום, לחגוג.
             - אם יש אירוע 'ריפוי' והחיים נמוכים, לרפא.
             - אם יש אירוע 'הגברה', לתקוף.
             - אחרת, לתקוף או להגן באקראי.
        """
        perceived_threat, random_event = perception

        if perceived_threat == "אין איום":
            return "לחגוג"

        if random_event == 'ריפוי' and self.health < 15:
            return "לרפא"
        elif random_event == 'הגברה':
            return "לתקוף"
        else:
            return random.choice(["לתקוף", "להגן"])

    def act(self, action, opponent):
        """
        (3) פעולה:
            ביצוע הפעולה שנבחרה, המשפיעה על היריב
            (חיים של היריב) או על הלוחם עצמו.
        """
        if action == "לתקוף":
            dmg = random.randint(5, 10)
            opponent.health -= dmg
            return f"{self.name} תוקף {opponent.name} ב-{dmg} נזק!"
        elif action == "להגן":
            return f"{self.name} מגן על עצמו!"
        elif action == "לרפא":
            heal_amt = random.randint(5, 10)
            self.health += heal_amt
            return f"{self.name} מרפא ב-{heal_amt} חיים!"
        elif action == "לחגוג":
            return f"{self.name} חוגג (היריב לא פעיל)!"
        else:
            return f"{self.name} מחכה..."

# יצירת שני לוחמים אייג'נטיים
maccabees = AgenticWarrior("המכבים", "מתתיהו", 30)
romans = AgenticWarrior("הרומאים", "אנטיוכוס", 30)

battle_over = False
round_number = 1
info_maccabees = ["פעולות המכבים:"]
info_romans = ["פעולות הרומאים:"]

def health_to_color(health):
    """החזרת צבע (ירוק, כתום, או אדום) בהתאם לרמת הבריאות."""
    if health > 20:
        return GREEN
    elif health > 10:
        return ORANGE
    else:
        return RED

def draw_screen():
    """הצגת הלוחמים, בריאותם, וסיכומי הקרב האחרונים בכל טור."""
    screen.fill(WHITE)

    # כותרת
    title_text = "לוחמה מבוססת בינה מלאכותית: מכבים נגד רומאים (לחץ רווח כל סיבוב)"
    title_surf = render_text(title_text, font, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 10))

    # חלוקה לשני טורים
    column_width = WIDTH // 2 - 100
    maccabees_x = 50
    romans_x = WIDTH // 2 + 50
    y_start = 50

    # טור המכבים
    # בריאות
    maccabees_color = health_to_color(maccabees.health)
    maccabees_width = max(0, int((maccabees.health / 30) * 150))
    pygame.draw.rect(screen, maccabees_color, (maccabees_x, y_start + 30, maccabees_width, 25))
    # תווית בריאות
    maccabees_label_text = f"{maccabees.name} ({maccabees.leader}) - חיים: {maccabees.health}"
    maccabees_label = render_text(maccabees_label_text, font, BLACK)
    screen.blit(maccabees_label, (maccabees_x, y_start))

    # טור הרומאים
    # בריאות
    romans_color = health_to_color(romans.health)
    romans_width = max(0, int((romans.health / 30) * 150))
    pygame.draw.rect(screen, romans_color, (romans_x, y_start + 30, romans_width, 25))
    # תווית בריאות
    romans_label_text = f"{romans.name} ({romans.leader}) - חיים: {romans.health}"
    romans_label = render_text(romans_label_text, font, BLACK)
    screen.blit(romans_label, (romans_x, y_start))

    # הצגת הסיבובים האחרונים בכל טור
    y_offset_m = y_start + 70
    for line in info_maccabees[-10:]:  # הצגת עד 10 שורות אחרונות
        info_surf = render_text(line, info_font, BLACK)
        screen.blit(info_surf, (maccabees_x, y_offset_m))
        y_offset_m += 20

    y_offset_r = y_start + 70
    for line in info_romans[-10:]:  # הצגת עד 10 שורות אחרונות
        info_surf = render_text(line, info_font, BLACK)
        screen.blit(info_surf, (romans_x, y_offset_r))
        y_offset_r += 20

    pygame.display.flip()

def next_round():
    """ניהול סיבוב אחד של הקרב אם הקרב עדיין לא נגמר."""
    global round_number, battle_over

    if battle_over:
        info_maccabees.append("הקרב כבר נגמר!")
        info_romans.append("הקרב כבר נגמר!")
        return

    round_texts_m = [f"--- סיבוב {round_number} ---"]
    round_texts_r = [f"--- סיבוב {round_number} ---"]

    # קביעת מי הולך ראשון בסיבוב (אקראי)
    first = random.choice([maccabees, romans])
    second = romans if first == maccabees else maccabees

    if first == maccabees:
        round_texts_m.append("המכבים פועלים ראשון.")
    else:
        round_texts_r.append("הרומאים פועלים ראשון.")

    # תור הלוחם הראשון
    perception_first = first.perceive(second)
    action_first = first.decide_action(perception_first)
    text_first = first.act(action_first, second)

    if first == maccabees:
        round_texts_m.append(f"תפיסה: {perception_first[0]}, אירוע: {perception_first[1]}")
        round_texts_m.append(f"החלטה: {action_first}")
        round_texts_m.append(text_first)
    else:
        round_texts_r.append(f"תפיסה: {perception_first[0]}, אירוע: {perception_first[1]}")
        round_texts_r.append(f"החלטה: {action_first}")
        round_texts_r.append(text_first)

    # בדיקת האם היריב הראשון נהרג
    if second.health <= 0:
        if first == maccabees:
            round_texts_m.append(f"{second.name} נהרג! {first.name} ניצח!")
            round_texts_r.append(f"{second.name} נהרג! {first.name} ניצח!")
        else:
            round_texts_r.append(f"{second.name} נהרג! {first.name} ניצח!")
            round_texts_m.append(f"{second.name} נהרג! {first.name} ניצח!")
        battle_over = True
    else:
        # תור הלוחם השני
        perception_second = second.perceive(first)
        action_second = second.decide_action(perception_second)
        text_second = second.act(action_second, first)

        if second == maccabees:
            round_texts_m.append(f"תפיסה: {perception_second[0]}, אירוע: {perception_second[1]}")
            round_texts_m.append(f"החלטה: {action_second}")
            round_texts_m.append(text_second)
        else:
            round_texts_r.append(f"תפיסה: {perception_second[0]}, אירוע: {perception_second[1]}")
            round_texts_r.append(f"החלטה: {action_second}")
            round_texts_r.append(text_second)

        # בדיקת האם הלוחם השני נהרג
        if first.health <= 0:
            if second == maccabees:
                round_texts_m.append(f"{first.name} נהרג! {second.name} ניצח!")
                round_texts_r.append(f"{first.name} נהרג! {second.name} ניצח!")
            else:
                round_texts_r.append(f"{first.name} נהרג! {second.name} ניצח!")
                round_texts_m.append(f"{first.name} נהרג! {second.name} ניצח!")
            battle_over = True

    # הוספת טקסטים לסיכום הסיבוב
    round_number += 1
    info_maccabees.extend(round_texts_m)
    info_romans.extend(round_texts_r)

# לולאת המשחק העיקרית
while True:
    clock.tick(30)  # 30 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # לחיצה על מקש הרווח להמשך לסיבוב הבא
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            next_round()

    draw_screen()