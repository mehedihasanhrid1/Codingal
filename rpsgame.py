import pygame
import random
import os
import json

pygame.init()

WIDTH, HEIGHT = 1200, 710
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

BG_TOP = (245, 245, 255)
BG_BOTTOM = (210, 220, 255)
HEADER_COLOR = (30, 40, 80)
WHITE = (255, 255, 255)
TEXT = (40, 40, 40)
GREEN = (60, 200, 90)
RED = (220, 70, 70)
BLUE = (60, 120, 230)
GRAY = (180, 180, 200)
BLUEVIOLET = (138, 43, 226)

TITLE_FONT = pygame.font.SysFont("arialblack", 48)
LABEL_FONT = pygame.font.SysFont("arial", 28)
SCORE_FONT = pygame.font.SysFont("arial", 32, bold=True)
RESULT_FONT = pygame.font.SysFont("arialblack", 32)

PLAYER_IMAGES = {
    "rock": pygame.image.load("rock.png"),
    "paper": pygame.image.load("paper.png"),
    "scissors": pygame.image.load("scissors.png")
}

PC_IMAGES = {
    "rock": pygame.image.load("pc_rock.png"),
    "paper": pygame.image.load("pc_paper.png"),
    "scissors": pygame.image.load("pc_scissors.png")
}

for k in PLAYER_IMAGES:
    PLAYER_IMAGES[k] = pygame.transform.scale(PLAYER_IMAGES[k], (230, 230))
for k in PC_IMAGES:
    PC_IMAGES[k] = pygame.transform.scale(PC_IMAGES[k], (230, 230))

class Button:
    def __init__(self, x, y, text, color, hover_color, width=190, height=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
    def draw(self, screen, mouse_pos):
        clr = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, clr, self.rect, border_radius=12)
        text_surface = LABEL_FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

buttons = [
    Button(200, 550, "Rock", BLUE, (100, 150, 255)),
    Button(500, 550, "Paper", GREEN, (120, 220, 120)),
    Button(800, 550, "Scissors", RED, (255, 100, 100)),
    Button(WIDTH - 180, 20, "Reset", BLUEVIOLET, (150, 150, 180), 140, 50)
]

player_score = 0
pc_score = 0
high_score = 0
round_winner = ""
player_choice = ""
pc_choice = ""

training_path = "training_data.json"
default_training = {
    "total_games": 0,
    "player_move_count": {"rock": 0, "paper": 0, "scissors": 0},
    "player_transition": {
        "rock": {"rock": 0, "paper": 0, "scissors": 0},
        "paper": {"rock": 0, "paper": 0, "scissors": 0},
        "scissors": {"rock": 0, "paper": 0, "scissors": 0}
    },
    "last_player_move": None,
    "recent_player_moves": []
}

if os.path.exists(training_path):
    try:
        with open(training_path, "r") as f:
            training = json.load(f)
    except:
        training = default_training.copy()
else:
    training = default_training.copy()

training.setdefault("recent_player_moves", [])
training.setdefault("last_player_move", None)

# High score
if os.path.exists("highscore.txt"):
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read().strip())
    except:
        high_score = 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def save_training():
    with open(training_path, "w") as f:
        json.dump(training, f)

def get_winner(player, pc):
    if player == pc:
        return "Draw"
    elif (player=="rock" and pc=="scissors") or (player=="paper" and pc=="rock") or (player=="scissors" and pc=="paper"):
        return "Player"
    else:
        return "Computer"

def update_training_after_round(player_move):
    training.setdefault("recent_player_moves", [])
    training.setdefault("last_player_move", None)
    training["total_games"] += 1
    training["player_move_count"][player_move] += 1
    last = training.get("last_player_move")
    if last:
        training["player_transition"][last][player_move] += 1
    training["last_player_move"] = player_move
    training["recent_player_moves"].append(player_move)
    if len(training["recent_player_moves"]) > 20:
        training["recent_player_moves"].pop(0)
    save_training()

# Predict player's next move using transitions + recent moves
def predict_player_prob():
    probs = {"rock": 1.0, "paper": 1.0, "scissors": 1.0}
    last = training.get("last_player_move")
    if last in training["player_transition"]:
        trans = training["player_transition"][last]
        total = sum(trans.values())
        if total > 0:
            for k in trans:
                probs[k] = trans[k] / total
    total_count = sum(training["player_move_count"].values())
    if total_count > 0:
        freq_prob = {k: training["player_move_count"][k]/total_count for k in training["player_move_count"]}
        for k in probs:
            probs[k] = 0.6*probs[k] + 0.4*freq_prob[k]
    s = sum(probs.values())
    return {k: probs[k]/s for k in probs}

def compute_suggestion_for_player():
    player_probs = predict_player_prob()
    counter_map = {"rock":"Paper","paper":"Scissors","scissors":"Rock"}
    moves = list(player_probs.keys())
    weights = list(player_probs.values())
    predicted_player = random.choices(moves, weights=weights, k=1)[0]
    suggested_move = counter_map[predicted_player]
    confidence = int(player_probs[predicted_player]*100)
    return suggested_move, confidence

ai_suggestion, ai_confidence = compute_suggestion_for_player()

def draw_gradient():
    for i in range(HEIGHT):
        color = (
            BG_TOP[0] + (BG_BOTTOM[0]-BG_TOP[0])*i//HEIGHT,
            BG_TOP[1] + (BG_BOTTOM[1]-BG_TOP[1])*i//HEIGHT,
            BG_TOP[2] + (BG_BOTTOM[2]-BG_TOP[2])*i//HEIGHT
        )
        pygame.draw.line(SCREEN, color, (0,i), (WIDTH,i))

clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    draw_gradient()
    pygame.draw.rect(SCREEN, HEADER_COLOR, (0,0,WIDTH,100))
    title = TITLE_FONT.render("ROCK  PAPER  SCISSORS", True, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 25))

    score_panel = pygame.Rect(150, 120, WIDTH-300, 80)
    pygame.draw.rect(SCREEN, WHITE, score_panel, border_radius=12)
    pygame.draw.rect(SCREEN, GRAY, score_panel, 2, border_radius=12)
    score_text = SCORE_FONT.render(f"Player: {player_score}      |      PC: {pc_score}", True, TEXT)
    SCREEN.blit(score_text, (score_panel.centerx - score_text.get_width()//2, score_panel.y+22))
    SCREEN.blit(LABEL_FONT.render(f"High Score: {high_score}", True, WHITE), (30,35))

    pygame.draw.line(SCREEN, GRAY, (WIDTH//2, 220), (WIDTH//2, 460), 3)
    SCREEN.blit(LABEL_FONT.render("You", True, TEXT), (WIDTH//2-300,230))
    SCREEN.blit(LABEL_FONT.render("Computer", True, TEXT), (WIDTH//2+220,230))

    if player_choice:
        SCREEN.blit(PLAYER_IMAGES[player_choice], (WIDTH//2-370,260))
    if pc_choice:
        SCREEN.blit(PC_IMAGES[pc_choice], (WIDTH//2+140,260))
    if round_winner:
        clr = GREEN if round_winner=="Player" else RED if round_winner=="Computer" else BLUE
        txt = RESULT_FONT.render(f"{round_winner} Wins!" if round_winner!="Draw" else "It's a Draw!", True, clr)
        SCREEN.blit(txt, (WIDTH//2 - txt.get_width()//2, 500))

    for b in buttons:
        b.draw(SCREEN, mouse_pos)

    ai_panel = pygame.Rect(200,620,800,80)
    pygame.draw.rect(SCREEN, WHITE, ai_panel, border_radius=12)
    pygame.draw.rect(SCREEN, GRAY, ai_panel, 2, border_radius=12)
    ai_text = SCORE_FONT.render(f"AI Suggestion: {ai_suggestion}   |   Win Chance: {ai_confidence}%", True, TEXT)
    SCREEN.blit(ai_text, (ai_panel.x+20, ai_panel.y+20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            for b in buttons:
                if b.clicked(mouse_pos):
                    if b.text in ["Rock","Paper","Scissors"]:
                        player_choice = b.text.lower()
                        pc_choice = random.choice(["rock","paper","scissors"])
                        round_winner = get_winner(player_choice, pc_choice)
                        if round_winner=="Player": player_score +=1
                        elif round_winner=="Computer": pc_score +=1
                        update_training_after_round(player_choice)
                        ai_suggestion, ai_confidence = compute_suggestion_for_player()
                        if player_score > high_score:
                            high_score = player_score
                            save_high_score(high_score)
                    elif b.text=="Reset":
                        player_score = 0
                        pc_score = 0
                        round_winner = ""
                        player_choice = ""
                        pc_choice = ""
                        training = default_training.copy()
                        save_training()
                        ai_suggestion, ai_confidence = compute_suggestion_for_player()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
