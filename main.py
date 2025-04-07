import pygame
import random
import sys
import os

# === Constants ===
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 200, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
RED = (255, 60, 60)
GREEN = (34, 139, 34)

HIGH_SCORE_FILE = "turkmen_hero_score.txt"

# === Initialization ===
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero of the Desert: Quest for the Artifact")
clock = pygame.time.Clock()
font = pygame.font.SysFont('georgia', 22)


# === Classes ===
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spirit = 10
        self.score = 0
        self.invincible_timer = 0
        self.dehydration_timer = 0

    def move(self, dx, dy, world):
        nx, ny = self.x + dx, self.y + dy
        if world.is_walkable(nx, ny):
            self.x, self.y = nx, ny

    def take_damage(self):
        if self.invincible_timer <= 0:
            self.spirit -= 1
            self.invincible_timer = 30

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        self.dehydration_timer += 1
        if self.dehydration_timer >= 70:
            self.dehydration_timer = 0
            self.spirit -= 1

    def draw(self):
        if self.invincible_timer > 0:
            if (self.invincible_timer // 5) % 2 == 0:
                color = CYAN
            else:
                color = GREEN
        else:
            color = GREEN
        pygame.draw.rect(win, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Scorpion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, player, world):
        distance = abs(player.x - self.x) + abs(player.y - self.y)
        if distance <= 5:
            if random.random() < 0.7:
                dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
                dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
            else:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
        else:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

        nx, ny = self.x + dx, self.y + dy
        if world.is_walkable(nx, ny):
            self.x, self.y = nx, ny

    def draw(self):
        pygame.draw.rect(win, RED, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class WaterJug:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.taken = False

    def draw(self):
        if not self.taken:
            pygame.draw.rect(win, ORANGE, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 10, 20, 20))


class Artifact:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.active = False

    def draw(self):
        if self.active:
            pygame.draw.rect(win, PURPLE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Desert:
    def __init__(self):
        self.map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.generate()

    def generate(self):
        for y in range(1, MAP_HEIGHT - 1):
            for x in range(1, MAP_WIDTH - 1):
                if random.random() < 0.75:
                    self.map[y][x] = 0
        self.map[1][1] = 0

    def is_walkable(self, x, y):
        return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and self.map[y][x] == 0

    def get_random_walkable(self):
        walkable = []
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.is_walkable(x, y):
                    walkable.append((x, y))
        return random.choice(walkable)

    def draw(self):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                color = (194, 178, 128) if self.map[y][x] == 0 else (139, 115, 85)
                pygame.draw.rect(win, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Game:
    def __init__(self):
        self.desert = Desert()
        self.player = Player(1, 1)
        self.artifact = Artifact()

        self.scorpions = []
        for _ in range(5):
            x, y = self.desert.get_random_walkable()
            while abs(x - self.player.x) < 5 and abs(y - self.player.y) < 5:
                x, y = self.desert.get_random_walkable()
            self.scorpions.append(Scorpion(x, y))

        self.jugs = [WaterJug(*self.desert.get_random_walkable()) for _ in range(8)]
        self.high_score = self.load_high_score()
        self.running = True

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(max(self.high_score, self.player.score)))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(0, -1, self.desert)
        elif keys[pygame.K_s]:
            self.player.move(0, 1, self.desert)
        elif keys[pygame.K_a]:
            self.player.move(-1, 0, self.desert)
        elif keys[pygame.K_d]:
            self.player.move(1, 0, self.desert)

    def update(self):
        self.player.update()

        for scorpion in self.scorpions:
            scorpion.move_towards(self.player, self.desert)
            if scorpion.x == self.player.x and scorpion.y == self.player.y:
                self.player.take_damage()

        for jug in self.jugs:
            if not jug.taken and jug.x == self.player.x and jug.y == self.player.y:
                jug.taken = True
                self.player.dehydration_timer = 0
                self.player.spirit += 1
                self.player.score += 10

        if all(jug.taken for jug in self.jugs) and not self.artifact.active:
            self.artifact.x, self.artifact.y = self.desert.get_random_walkable()
            while abs(self.artifact.x - self.player.x) < 5 and abs(self.artifact.y - self.player.y) < 5:
                self.artifact.x, self.artifact.y = self.desert.get_random_walkable()
            self.artifact.active = True

        if self.artifact.active and self.player.x == self.artifact.x and self.player.y == self.artifact.y:
            self.victory()

    def draw_ui(self):
        spirit_text = font.render(f"Spirit: {self.player.spirit}", True, CYAN)
        score_text = font.render(f"Score: {self.player.score}", True, YELLOW)
        high_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        jugs_left = sum(not jug.taken for jug in self.jugs)
        jugs_text = font.render(f"Jugs left: {jugs_left}", True, ORANGE)

        win.blit(spirit_text, (10, 10))
        win.blit(score_text, (10, 40))
        win.blit(high_text, (10, 70))
        win.blit(jugs_text, (10, 100))

        if self.artifact.active:
            artifact_text = font.render("Artifact Active! Find the Purple Artifact!", True, PURPLE)
            win.blit(artifact_text, (WIDTH - 300, 10))

    def draw(self):
        self.desert.draw()
        self.player.draw()
        for scorpion in self.scorpions:
            scorpion.draw()
        for jug in self.jugs:
            jug.draw()
        self.artifact.draw()
        self.draw_ui()

    def intro_screen(self):
        win.fill(BLACK)
        lines = [
            "As a Turkmen warrior, seek the ancient artifact hidden in Karakum.",
            "Collect water jugs to survive and activate the artifact.",
            "Beware of guardian scorpions!",
            "", "Use WASD to move. Press any key to begin."
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, WHITE)
            win.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 180 + i * 30))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def game_over(self):
        self.save_high_score()
        win.fill(BLACK)
        msg = font.render("Your journey ends in the shifting sands...", True, RED)
        score_msg = font.render(f"Final Score: {self.player.score}", True, YELLOW)
        prompt = font.render("Press ESC to Exit", True, WHITE)
        win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
        win.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, HEIGHT // 2))
        win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
                    self.running = False

    def victory(self):
        self.save_high_score()
        win.fill(BLACK)
        msg = font.render("You claimed the ancient artifact! Glory to Turkmen!", True, PURPLE)
        score_msg = font.render(f"Final Score: {self.player.score}", True, YELLOW)
        prompt = font.render("Press ESC to Exit", True, WHITE)
        win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
        win.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, HEIGHT // 2))
        win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
                    self.running = False

    def run(self):
        self.intro_screen()
        while self.running:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.update()

            win.fill(BLACK)
            self.draw()
            pygame.display.flip()

            if self.player.spirit <= 0:
                self.game_over()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()