import pygame
from src.settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Orbitron", 60, bold=True)
        self.font_button = pygame.font.SysFont("Rajdhani", 30, bold=True)
        
        print("--- Iniciando carga de UI ---")
        
        self.menu_bg = self.safe_load('assets/images/menu_bg.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level_select_bg = self.safe_load('assets/images/level_select_bg.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Botones de Menú
        self.btn_play_img = self.safe_load('assets/images/btn_play.png', (250, 100))
        self.btn_exit_img = self.safe_load('assets/images/btn_exit.png', (250, 100))
        
        # Botón Ayuda (Intenta cargar imagen, si no, usa texto)
        self.btn_help_img = self.safe_load('assets/images/btn_help.png', (250, 100))
        
        self.level_images = {}
        for i in range(1, 6): 
            img = self.safe_load(f'assets/images/nivel{i}.png', (80, 80))
            if img:
                self.level_images[i] = img
            else:
                self.level_images[i] = self.safe_load('assets/images/level_button.png', (80, 80))
        
        print("--- Carga de UI finalizada ---")

    def safe_load(self, path, size=None):
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except FileNotFoundError:
            return None
        except Exception:
            return None

    def draw_text(self, text, size, x, y, color=COLOR_TEXT):
        font = pygame.font.SysFont("Arial", size) 
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw_image_button(self, image, x, y, clicked, text="", action_code=None, scale_hover=1.1):
        mouse_pos = pygame.mouse.get_pos()
        
        rect = image.get_rect(center=(x, y))
        final_image = image
        action_triggered = None
        
        if rect.collidepoint(mouse_pos):
            new_size = (int(rect.width * scale_hover), int(rect.height * scale_hover))
            final_image = pygame.transform.scale(image, new_size)
            rect = final_image.get_rect(center=rect.center)
            if clicked:
                action_triggered = action_code

        self.screen.blit(final_image, rect.topleft)
        
        if text:
            shadow_surf = self.font_button.render(text, True, (0,0,0))
            shadow_rect = shadow_surf.get_rect(center=(rect.centerx + 2, rect.centery + 2))
            self.screen.blit(shadow_surf, shadow_rect)
            
            text_surf = self.font_button.render(text, True, COLOR_TEXT)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            
        return action_triggered

    def draw_button(self, text, x, y, w, h, clicked, action_code):
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(0, 0, w, h)
        rect.center = (x, y)
        
        color = COLOR_BUTTON
        action_triggered = None

        if rect.collidepoint(mouse_pos):
            color = COLOR_BUTTON_HOVER
            if clicked: action_triggered = action_code

        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        text_surf = self.font_button.render(text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        return action_triggered

    def draw_main_menu(self, clicked):
        if self.menu_bg:
            self.screen.blit(self.menu_bg, (0, 0))
        else:
            self.screen.fill(COLOR_BG)
            self.draw_text("ECO RESONANCIA", 60, SCREEN_WIDTH//2, 100, COLOR_ECHO)
        
        action = None
        
        # --- JUGAR ---
        if self.btn_play_img:
            if self.draw_image_button(self.btn_play_img, SCREEN_WIDTH//2, 250, clicked, "", "goto_select"):
                action = "goto_select"
        else:
            if self.draw_button("JUGAR", SCREEN_WIDTH//2, 250, 200, 50, clicked, "goto_select"):
                action = "goto_select"

        # --- CÓMO JUGAR ---
        if self.btn_help_img:
            if self.draw_image_button(self.btn_help_img, SCREEN_WIDTH//2, 375, clicked, "", "instructions"):
                action = "instructions"
        else:
            if self.draw_button("CÓMO JUGAR", SCREEN_WIDTH//2, 375, 200, 50, clicked, "instructions"):
                action = "instructions"
            
        # --- SALIR ---
        if self.btn_exit_img:
            if self.draw_image_button(self.btn_exit_img, SCREEN_WIDTH//2, 500, clicked, "", "exit"):
                action = "exit"
        else:
            if self.draw_button("SALIR", SCREEN_WIDTH//2, 500, 200, 50, clicked, "exit"):
                action = "exit"
        
        return action

    def draw_level_select(self, unlocked_levels, clicked):
        if self.level_select_bg:
            self.screen.blit(self.level_select_bg, (0, 0))
        elif self.menu_bg:
            self.screen.blit(self.menu_bg, (0, 0))
        else:
            self.screen.fill(COLOR_BG)
        
        action = None
        start_x = SCREEN_WIDTH//2 - 250
        gap = 110
        
        for i in range(1, 6):
            x_pos = start_x + (i-1)*gap
            y_pos = 300
            
            if i > unlocked_levels:
                rect = pygame.Rect(0, 0, 80, 80)
                rect.center = (x_pos, y_pos)
                pygame.draw.rect(self.screen, COLOR_LOCKED, rect, border_radius=10)
                self.draw_text("X", 30, x_pos, y_pos, (150, 150, 150))
            else:
                img = self.level_images.get(i)
                if img:
                     if self.draw_image_button(img, x_pos, y_pos, clicked, "", f"start_game_{i}"):
                        action = f"start_game_{i}"
                else:
                    if self.draw_button(f"{i}", x_pos, y_pos, 80, 80, clicked, f"start_game_{i}"):
                        action = f"start_game_{i}"

        if self.draw_button("VOLVER", SCREEN_WIDTH//2, 550, 200, 50, clicked, "goto_menu"):
            action = "goto_menu"
        
        return action