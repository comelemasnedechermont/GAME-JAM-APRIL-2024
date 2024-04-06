import pygame
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

class Icon:
    def __init__(self, image_path, position, message):
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.message = message

def display_popup(screen, popup_image_rect, message):
    font = pygame.font.Font(None, 20)
    text_rendered = font.render(message, True, BLACK)
    text_rect = text_rendered.get_rect()
    text_rect.bottomleft = (300, 300)    
    screen.blit(text_rendered, text_rect)

if __name__ == "__main__":
    main()
