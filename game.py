import pygame
import sys
import moviepy.editor
from pygame.locals import *
from snake import *
from tetris import *

pygame.init()

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print("Impossible de charger l'image :", image_path)
        raise SystemExit(str(e))

class Icon:
    def __init__(self, image_path, position, password, game, path):
        self.base_image = load_image(image_path)
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft=position)
        self.requires_password = password
        self.game = game
        self.new_image_path = path

class Popup:
    def __init__(self, image_path, position):
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(topleft=position)

def ask_password(screen):
    password_input = ''
    font = pygame.font.Font(None, 36)
    popup_width = 400
    popup_height = 200
    popup_rect = pygame.Rect((WINDOW_WIDTH - popup_width) // 2, (WINDOW_HEIGHT - popup_height) // 2, popup_width, popup_height)
    input_rect = pygame.Rect(popup_rect.left + 50, popup_rect.top + 80, 300, 40)
    cursor_visible = True
    cursor_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return password_input, popup_rect
                elif event.key == K_BACKSPACE:
                    password_input = password_input[:-1]
                elif event.key == K_LEFT:
                    if len(password_input) > 0:
                        password_input = password_input[:-1]
                elif event.key == K_RIGHT:
                    if len(password_input) < len(password_input):
                        password_input = password_input + password_input[len(password_input)]
                elif event.key == K_ESCAPE:
                    return None, popup_rect
                else:
                    password_input += event.unicode
        cursor_timer += 1
        if cursor_timer >= 800:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        pygame.draw.rect(screen, WHITE, popup_rect)
        pygame.draw.rect(screen, BLACK, popup_rect, 2)
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        text_surface = font.render(password_input, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        if cursor_visible:
            cursor_x = input_rect.x + 5 + font.size(password_input[:len(password_input)])[0]
            cursor_rect = pygame.Rect(cursor_x, input_rect.y + 5, 2, input_rect.height - 10)
            pygame.draw.rect(screen, BLACK, cursor_rect)
        pygame.display.flip()


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("OpenTheFile")

    background_image = load_image("assets/oui.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    icons = [
        Icon("assets/tuto.png", (700, 450), "", "", "assets/tutoMessage.png"),
        Icon("assets/secret.png", (750, 450), "7X9zP1q5rsy", "video",""),
        Icon("assets/game.png", (1400, 800), "basilic", "snake",""),
        Icon("assets/game.png", (700, 800), "", "tetris",""),
        Icon("assets/file.png", (300, 200), "", "", "assets/Enigme.png"),
        Icon("assets/file.png", (300, 400), "", "", "assets/cesar2.png"),
        Icon("assets/file.png", (200, 200), "", "", "assets/loremIpsum.png"),
        Icon("assets/file.png", (500, 300), "", "", "assets/loremIpsum1.png"),
        Icon("assets/file.png", (1200, 400), "", "", "assets/loremIpsum2.png"),
        Icon("assets/file.png", (900, 500), "", "", "assets/baitBinary.png"),
        Icon("assets/file.png", (600, 400), "", "", "assets/clue3.png"),
        Icon("assets/file.png", (1300, 500), "", "", "assets/cesar.png"),
        Icon("assets/file.png", (1100, 200), "", "", "assets/arabe.png"),
        Icon("assets/file.png", (1300, 300), "", "", "assets/coréen.png"),
        Icon("assets/file.png", (300, 700), "", "", "assets/japonais.png"),
        Icon("assets/file.png", (500, 800), "", "", "assets/allemand.png"),
    ]
    popups = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for icon in icons:
                        if icon.rect.collidepoint(event.pos):
                            if icon.requires_password:
                                password_input, popup_rect = ask_password(screen)
                                if password_input == icon.requires_password:
                                    if icon.game == "snake":
                                        startSnake()
                                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                                    elif icon.game == "tetris":
                                        game = Tetris()
                                        game.run()
                                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                                    elif icon.game == "video":
                                        video = moviepy.editor.VideoFileClip("assets/Never gonna Meow you up.mp4", target_resolution=(1000,1500))
                                        video.preview()
                                    else:
                                        popups.append(Popup(icon.new_image_path, (200, 200)))
                                pass
                            else:
                                if icon.game == "snake":
                                    startSnake()
                                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                                elif icon.game == "tetris":
                                        game = Tetris()
                                        game.run()
                                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                                elif icon.game == "video":
                                    video = moviepy.editor.VideoFileClip("assets/Never gonna Meow you up.mp4", target_resolution=(1000,1500))
                                    video.preview()
                                else:
                                    popups.append(Popup(icon.new_image_path, (200, 200)))
                        for popup in popups:
                            close_area = pygame.Rect(popup.rect.right - 40, popup.rect.top, 40, 40)
                            if close_area.collidepoint(event.pos):
                                popups.remove(popup)
                                break
        screen.blit(background_image, (0, 0))

        for icon in icons:
            screen.blit(icon.image, icon.rect)

        for popup in popups:
            screen.blit(popup.image, popup.rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
