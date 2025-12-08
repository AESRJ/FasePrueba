from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player
from src.mechanics import Lever, Gate, Spike, Barrier

def load_level_4(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()
    
    hazards = [] 
    barriers = {} 
    specific_levers = {}

    # --- 1. ESTRUCTURA ---
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    p_start = Platform(50, 200, type="normal")
    p_up_1 = Platform(300, 200, type="chica")
    p_up_2 = Platform(500, 150, type="chica")
    p_up_3 = Platform(800, 200, type="chica")
    p_lev_top = Platform(1050, 200, type="chica")
    p_lev_bot = Platform(50, 500, type="normal")
    p_end = Platform(1050, 500, type="normal")

    platforms.add(p_start, p_up_1, p_up_2, p_up_3, p_lev_top, p_lev_bot, p_end)
    all_sprites.add(p_start, p_up_1, p_up_2, p_up_3, p_lev_top, p_lev_bot, p_end)

    # --- 2. ASCENSOR ---
    gate_elevator = Gate(650, 550, width=150, height=20, move_y=-350)
    # Sin fill para usar textura normal
    gates.add(gate_elevator)
    all_sprites.add(gate_elevator)

    # --- 3. PINCHOS ---
    for x in range(250, 1000, 50):
        s = Spike(x, floor.rect.top, width=50)
        hazards.append(s)
        all_sprites.add(s)

    # --- 4. PALANCAS ---
    lev_top = Lever(1080, p_lev_top.rect.top)
    lev_bot = Lever(100, p_lev_bot.rect.top)

    levers.add(lev_top, lev_bot)
    all_sprites.add(lev_top, lev_bot)
    
    specific_levers["top"] = lev_top
    specific_levers["bottom"] = lev_bot

    # --- 5. CRISTALES ---
    c1 = Crystal(p_up_2.rect.centerx, p_up_2.rect.top - 20) 
    c2 = Crystal(gate_elevator.rect.centerx, 500) 
    c3 = Crystal(p_lev_bot.rect.centerx + 50, p_lev_bot.rect.top - 20) 
    crystals.add(c1, c2, c3)
    all_sprites.add(c1, c2, c3)

    # --- 6. PORTAL ---
    # El portal mide 100 de ancho y está en x=1100 (hasta 1200)
    portal = Portal(1100, p_end.rect.top + 10)
    portal.rect.bottom = p_end.rect.top
    all_sprites.add(portal)

    # --- 7. JUGADOR ---
    player = Player(80, p_start.rect.top - 50)
    all_sprites.add(player)

    # --- 8. BARRERA (AL FINAL) ---
    # Ajuste de coordenadas:
    # Portal X: 1100 a 1200. Centro 1150.
    # Barrera X: 1080. Ancho 140 (Llega a 1220). Cubre perfecto.
    # Portal Y Top: 350. Barrera Y: 330. Altura 170 (Llega a 500). Cubre perfecto.
    barrier_final = Barrier(1080, 330, 140, 170, color=(50, 205, 50))
    barriers["final"] = barrier_final
    
    # IMPORTANTE: Se agrega al final para dibujarse EN FRENTE del portal
    all_sprites.add(barrier_final)

    return player, portal, None, {
        "tutorial_step": 0,
        "popup_text": "NIVEL 4: EL FOSO SINCRONIZADO",
        "show_popup": True,
        "hazards": hazards,
        "barriers": barriers,
        "specific_levers": specific_levers,
        "moving_gate": gate_elevator, 
        "moving_crystal": None
    }