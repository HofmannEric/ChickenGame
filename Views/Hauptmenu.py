import pygame
import sqlite3


class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.start_button = pygame.Rect(25, 200, 220, 50)
        self.leaderboard_title = pygame.Rect(650, 140, 350, 50)
        self.leaderboard_placements = [
            pygame.Rect(650, 200, 350, 35),
            pygame.Rect(650, 240, 350, 35),
            pygame.Rect(650, 280, 350, 35),
            pygame.Rect(650, 320, 350, 35),
            pygame.Rect(650, 360, 350, 35)
        ]
        self.Highscores = []

    def draw(self, screen):
        mm_background = pygame.image.load("Background/background_test.png")
        screen.blit(mm_background, (0, 0))
        pygame.draw.rect(screen, (133, 166, 45), self.start_button)
        start_text = self.font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))

        self.get_highscores()
        # drawing the Leaderboard

        pygame.draw.rect(screen, (100, 100, 100), self.leaderboard_title)
        highscore_text = self.font.render("Your highscores:", True, (255, 255, 255))
        screen.blit(highscore_text, (self.leaderboard_title.x + 10, self.leaderboard_title.y + 10))

        highscore_counter = 0
        while highscore_counter < 5:
            pygame.draw.rect(screen, (150, 0, 0), self.leaderboard_placements[highscore_counter])
            print("drawn rect")

            if self.Highscores.__len__() > highscore_counter:
                highscore_text_raw = str(self.Highscores[highscore_counter][1]) + " || " + \
                                     str(self.Highscores[highscore_counter][2])
                highscore_text = self.font.render(highscore_text_raw, True, (255, 255, 255))
                screen.blit(highscore_text, (self.leaderboard_placements[highscore_counter].x + 5,
                                             self.leaderboard_placements[highscore_counter].y))
                print("blitted text")
            highscore_counter += 1

    def get_highscores(self):
        conn = sqlite3.connect('Database/Highscores.db')
        cursor = conn.cursor()
        cursor.execute(
            '''Create Table if not exists leaderboard (id Integer PRIMARY KEY, day_date TEXT, score INTEGER)''')
        cursor.execute('''select * from leaderboard Order by score DESC LIMIT 5''')
        self.Highscores = cursor.fetchall()
        conn.commit()
        conn.close()

    def start_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                return "start_game"
        return None
