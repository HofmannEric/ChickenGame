import sqlite3
from datetime import datetime
import pygame


class GameOver:
    def __init__(self):
        self.already_saved = False
        self.score = ""
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.game_over_rect = pygame.Rect(298, 140, 400, 50)
        self.final_rect = pygame.Rect(298, 200, 270, 35)
        self.score_rect = pygame.Rect(298, 240, 270, 35)
        self.back_rect = pygame.Rect(298, 400, 270, 35)

    def draw(self, screen):
        score_background = pygame.image.load("Background/background_test.png")
        screen.blit(score_background, (0, 0))

        pygame.draw.rect(screen, (133, 0, 133), self.game_over_rect)
        game_over_text = self.font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (self.game_over_rect.x + 115, self.game_over_rect.y + 10))

        pygame.draw.rect(screen, (133, 0, 133), self.final_rect)
        final_rect_text = self.font.render("Your final score:", True, (255, 255, 255))
        screen.blit(final_rect_text, (self.final_rect.x + 5, self.final_rect.y + 5))

        pygame.draw.rect(screen, (0, 133, 0), self.score_rect)
        score_rect_text = self.font.render(self.score + " Points!", True, (255, 255, 255))
        screen.blit(score_rect_text, (self.score_rect.x + 5, self.score_rect.y + 5))

        pygame.draw.rect(screen, (0, 175, 0), self.back_rect)
        back_rect_text = self.font.render("Back to menu", True, (255, 255, 255))
        screen.blit(back_rect_text, (self.back_rect.x + 5, self.back_rect.y + 5))

        self.save_score()

    def get_score(self, game_score: int):
        self.score = str(game_score)

    def save_score(self):
        if not self.already_saved:
            conn = sqlite3.connect('Database/Highscores.db')
            cursor = conn.cursor()
            cursor.execute('''Insert into leaderboard (day_date, score) values (?, ?)''',
                           (datetime.now().date(), self.score))
            conn.commit()
            conn.close()
            self.already_saved = True

    def main_check(self, eventpos):
        return self.back_rect.collidepoint(eventpos)
