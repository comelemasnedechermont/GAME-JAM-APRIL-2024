import pygame
import sys
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PASSWORD_REQUIRED_ICONS = ["assets/secret.png"]
PASSWORD = "mdp"

def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print("Impossible de charger l'image :", image_path)
        raise SystemExit(str(e))

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Open")

    background_image = load_image("assets/window98.png")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    icons = [
        Icon("assets/tuto.png", (100, 100), "Ceci est le message de l'icône 1"),
        Icon("assets/secret.png", (300, 100), "Ceci est le message de l'icône 2"),
    ]
    popup_image = load_image("assets/newWindow.png")
    popup_image_rect = popup_image.get_rect()
    popup_image_rect.topleft = (200, 200)
    popup_top_right_corner = popup_image_rect.topright
    popup_displayed = False
    password_input = ''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for icon in icons:
                    if icon.rect.collidepoint(event.pos):
                        if icon.image_path in PASSWORD_REQUIRED_ICONS:
                            password_input, popup_rect = ask_password(screen)
                            if password_input == PASSWORD:
                                popup_displayed = True
                                current_message = icon.message
                            else:
                                print("Mot de passe incorrect")
                                password_input = ''  # Réinitialiser le mot de passe saisi
                                ##shake_popup(screen, popup_rect)  # Appel de la fonction de secousse
                        else:
                            popup_displayed = True
                            current_message = icon.message
                if popup_displayed and (popup_top_right_corner[0] - 20 <= event.pos[0] <= popup_top_right_corner[0]) and (popup_top_right_corner[1] <= event.pos[1] <= popup_top_right_corner[1] + 20):
                    popup_displayed = False

        screen.blit(background_image, (0, 0))

        for icon in icons:
            screen.blit(icon.image, icon.rect)

        if popup_displayed:
            screen.blit(popup_image, popup_image_rect)
            display_popup(screen, popup_image_rect, current_message)

        pygame.display.flip()
    pygame.quit()
    sys.exit()

def shake_popup(screen, popup_rect):
    original_pos = popup_rect.topleft
    displacement = 50  # Augmentez cette valeur pour une secousse plus intense
    shake_time = 10  # Nombre d'itérations de secousse
    for _ in range(shake_time):
        popup_rect.x += displacement
        pygame.display.update(popup_rect)  # Rafraîchir uniquement la zone de la fenêtre secouée
        pygame.time.wait(20)
        popup_rect.x -= displacement * 2
        pygame.display.update(popup_rect)  # Rafraîchir uniquement la zone de la fenêtre secouée
        pygame.time.wait(20)
        popup_rect.x += displacement
        pygame.display.update(popup_rect)  # Rafraîchir uniquement la zone de la fenêtre secouée
        pygame.time.wait(20)
    popup_rect.topleft = original_pos  # Rétablir la position initiale

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

class Icon:
    def __init__(self, image_path, position, message):
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.message = message
        self.image_path = image_path

def display_popup(screen, popup_image_rect, message):
    font = pygame.font.Font(None, 20)
    text_rendered = font.render(message, True, BLACK)
    text_rect = text_rendered.get_rect()
    text_rect.bottomleft = (300, 300)    
    screen.blit(text_rendered, text_rect)

if __name__ == "__main__":
    main()
