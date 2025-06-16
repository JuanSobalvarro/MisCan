import pygame as pg
import sys

# Configuración
ANCHO, ALTO = 800, 600
FPS = 60
BLANCO = (255, 255, 255)
VERDE = (0, 128, 0)
AZUL = (0, 0, 255)
MARRON = (139, 69, 19)
ROJO = (200, 0, 0)
NEGRO = (0, 0, 0)

pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))
pg.display.set_caption("Misioneros y Caníbales")
clock = pg.time.Clock()

# Estado inicial
estado = {"ML":3, "CL":3, "MR":0, "CR":0, "BOTE":"left"}

# Datos de NPCs
npc_tamaño = (40, 80)
npc_left = []
npc_right = []
boat_passengers = []

font = pg.font.SysFont(None, 28)

# Crear NPCs iniciales
for i in range(3):
    npc_left.append({"tipo":"M", "rect": pg.Rect(60, 100 + i*90, *npc_tamaño)})
    npc_left.append({"tipo":"C", "rect": pg.Rect(110, 100 + i*90, *npc_tamaño)})

# Bote
bote = pg.Rect(200, ALTO - 120, 80, 40)

def dibujar():
    pantalla.fill(BLANCO)
    # Dibujar río
    pg.draw.rect(pantalla, AZUL, (ANCHO//2 - 100, 0, 200, ALTO))
    # Dibujar orillas
    pg.draw.rect(pantalla, VERDE, (0, 0, ANCHO//2 - 100, ALTO))
    pg.draw.rect(pantalla, VERDE, (ANCHO//2 + 100, 0, ANCHO//2 - 100, ALTO))
    # Bote
    pg.draw.rect(pantalla, MARRON, bote)
    # Dibujar NPCs
    for npc in npc_left + npc_right + boat_passengers:
        color = NEGRO if npc["tipo"] == "M" else ROJO
        pg.draw.rect(pantalla, color, npc["rect"])
    # Estado
    texto = font.render(f"L: {estado['ML']}M {estado['CL']}C | R: {estado['MR']}M {estado['CR']}C | Bote: {estado['BOTE']}", True, NEGRO)
    pantalla.blit(texto, (10, 10))
    # Botón mover
    boton = pg.Rect(10, 50, 140, 40)
    pg.draw.rect(pantalla, (0,0,0), boton)
    pantalla.blit(font.render("Mover Bote", True, BLANCO), (20, 60))
    pg.display.flip()
    return boton

def mover_bote():
    if not boat_passengers:
        print("El bote no puede ir vacío")
        return
    if not any(npc["tipo"] == "C" for npc in boat_passengers):
        print("Debe haber al menos 1 caníbal en el bote")
        return

    if estado["BOTE"] == "left":
        for npc in boat_passengers:
            if npc["tipo"] == "M": estado["ML"] -=1
            if npc["tipo"] == "C": estado["CL"] -=1
            npc_right.append(npc)
            npc["rect"].x = ANCHO - 180 + (npc_right.index(npc)%2)*50
            npc["rect"].y = 100 + (npc_right.index(npc)//2)*90
        estado["MR"] = sum(1 for n in npc_right if n["tipo"] == "M")
        estado["CR"] = sum(1 for n in npc_right if n["tipo"] == "C")
        estado["BOTE"] = "right"
        bote.x = ANCHO - 280
    else:
        for npc in boat_passengers:
            if npc["tipo"] == "M": estado["MR"] -=1
            if npc["tipo"] == "C": estado["CR"] -=1
            npc_left.append(npc)
            npc["rect"].x = 60 + (npc_left.index(npc)%2)*50
            npc["rect"].y = 100 + (npc_left.index(npc)//2)*90
        estado["ML"] = sum(1 for n in npc_left if n["tipo"] == "M")
        estado["CL"] = sum(1 for n in npc_left if n["tipo"] == "C")
        estado["BOTE"] = "left"
        bote.x = 200
    boat_passengers.clear()

    if not estado_valido():
        print("¡Estado inválido! Los misioneros han sido devorados. Reiniciando...")
        reiniciar()

    if estado["ML"] == 0 and estado["CL"] == 0:
        print("¡Victoria! Todos cruzaron sanos y salvos.")
        reiniciar()

def estado_valido():
    for lado in ["ML", "CL", "MR", "CR"]:
        if estado[lado] < 0 or estado[lado] > 3:
            return False
    if estado["ML"] > 0 and estado["CL"] > estado["ML"]:
        return False
    if estado["MR"] > 0 and estado["CR"] > estado["MR"]:
        return False
    return True

def reiniciar():
    global npc_left, npc_right, boat_passengers, estado, bote
    npc_left, npc_right, boat_passengers = [], [], []
    estado = {"ML":3, "CL":3, "MR":0, "CR":0, "BOTE":"left"}
    for i in range(3):
        npc_left.append({"tipo":"M", "rect": pg.Rect(60, 100 + i*90, *npc_tamaño)})
        npc_left.append({"tipo":"C", "rect": pg.Rect(110, 100 + i*90, *npc_tamaño)})
    bote.x = 200

# Lógica principal
while True:
    boton = dibujar()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if boton.collidepoint(event.pos):
                mover_bote()
            else:
                grupo = npc_left if estado["BOTE"] == "left" else npc_right
                for npc in grupo:
                    if npc["rect"].collidepoint(event.pos):
                        if npc in boat_passengers:
                            boat_passengers.remove(npc)
                            continue
                        if len(boat_passengers) < 2:
                            boat_passengers.append(npc)
    clock.tick(FPS)
