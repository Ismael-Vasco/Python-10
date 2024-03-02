import pygame
import random
import math
from pygame import mixer        # para colocar musica al juego

# INICIALIZACIÓN DE PYgame
pygame.init()

# Asignación a la pantalla para que muestre algo
# --- se le asigna pygame a la pantalla 'dispay' con un set 'set_mode' y se la da el 
#     tamaño en pizeles  en tupla '(800,600)'
pantalla = pygame.display.set_mode((800, 600))

# Cambiar titulo
pygame.display.set_caption("Invasión Espacial")

# fonde del juego
fondo = pygame.image.load("fondo.png")

# Musica 
mixer.music.load("musica_fondo.mp3")
mixer.music.play(-1)

# cambiar icono
icono = pygame.image.load("extraterrestre.png")
pygame.display.set_icon(icono)

# Variables del jugador (movimiento en sus ejes)
img_jugador = pygame.image.load("nave.png")
eje_x = ((800/2) - (64/2))  #368 # (800/2) - (64/2) -> 800 de pantalla y 64 del tamaño de la imagen
eje_y = 500                      # lo mas cerca al 600 posible, para que quede ubicado centrado y en la orilla
jugador_cambio_eje_x = 0

# Variables del enemigo (movimiento en sus ejes)
img_enemigo = []
eje_x_enemigo = []           # con random para que se mueva aleatoriamente
eje_y_enemigo = []         
enemigo_cambio_eje_x = []
enemigo_cambio_eje_y = []
cantidad_enemigos = 8

for enemis in range(cantidad_enemigos):
    # Variables del enemigos nuevos enemigos y mas (movimiento en sus ejes)
    img_enemigo.append(pygame.image.load("enemigo.png"))
    eje_x_enemigo.append(random.randint(0, 736) )          
    eje_y_enemigo.append(random.randint(50,200)  )          
    enemigo_cambio_eje_x.append(1.5)
    enemigo_cambio_eje_y.append(50)

# Variables de la bala (movimiento en sus ejes)
img_bala = pygame.image.load("bala.png")
eje_x_bala = 0           # 
eje_y_bala = 500         
bala_cambio_eje_x = 0
bala_cambio_eje_y = 3 
bala_visible = False

# variable puntaje
puntaje = 0
    # font -> fuente de texto
fuente  = pygame.font.Font("Raleway-Thin.ttf",  32)
texto_x = 10
texto_y = 10

# final del juego
fuente_final = pygame.font.Font("Raleway-Thin.ttf",  60)

# función de finalización del juego
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (130,200))


# función mostrar puntaje
def mostrar_puntaje(x, y):
    #render -> imprimir en pantalla
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x, y))

# Función del jugador
def jugador(x, y):
    # 'blit' -> arrojar, colocar en ..
    pantalla.blit(img_jugador, (x, y))

# Función del enemigo
def enemigo(x, y, enemigo):
    # 'blit' -> arrojar, colocar en ..
    pantalla.blit(img_enemigo[enemigo], (x, y))

# Función disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 20, y + 15))

# Función de Colision - distancia
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False



se_ejecuta = True

            #       se crea un bucle para que la pantalla no desaparezca hasta que se haga una acción 
            #       se hace un for para asignar cualquier evento que pase en los eventos que se llaman con el 'get()'
            #       se realiza un if para saber si se realiza el evento QUIT (salir desde la x en la zona superior de la pantalla)
            #       se cambia el booleano del While para salir del bucle

while se_ejecuta:
    # Pantalla rosa RGB
    #pantalla.fill((205, 144, 228))

    # fondo de pantalla
    pantalla.blit(fondo, (0, 0))

    # evento para cerrar programa
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        
        # evento de movimiento con flechas (tecla)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_cambio_eje_x = -1.5
            if evento.key == pygame.K_RIGHT:
                jugador_cambio_eje_x = 1.5
            # evento para disparar con 'space' espacio
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    balazo = mixer.Sound('disparo_laser.mp3')
                    balazo.set_volume(0.1)
                    balazo.play()
                    eje_x_bala = eje_x
                    disparar_bala(eje_x_bala, eje_y_bala)

        # evento al soltar una flecha (tecla)
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_cambio_eje_x = 0

    # modificador ubicación en el juego del jugaron
    eje_x += jugador_cambio_eje_x

    # Mantener en bordes al jugador 
    if eje_x <= 0:          # 0 porque es el limite del borde izquierdo 
        eje_x = 0
    
    elif eje_x >= 736:      # 736 porque es la resta de 800(pantall) y 64(nave) para que no se salga dle borde derecho
        eje_x = 736
    

    # modificador ubicación en el juego del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if eje_y_enemigo[e] > 500:
            for k in range(cantidad_enemigos):
                eje_y_enemigo[k] = 1000
            texto_final()
            break
        eje_x_enemigo[e] += enemigo_cambio_eje_x[e]

    # Mantener en bordes al enemigo 
        if eje_x_enemigo[e] <= 0:
            enemigo_cambio_eje_x[e] = 1.5
            eje_y_enemigo[e] += enemigo_cambio_eje_y[e]
        
        elif eje_x_enemigo[e] >= 736:
            enemigo_cambio_eje_x[e] = -1.5
            eje_y_enemigo[e] += enemigo_cambio_eje_y[e]
   
    # colisión
        colision = hay_colision(eje_x_enemigo[e], eje_y_enemigo[e], eje_x_bala, eje_y_bala)
        if colision:
            explosion = mixer.Sound('explosion.mp3')
            explosion.play()
            eje_y_bala = 500
            bala_visible = False 
            puntaje += 1
            
            eje_x_enemigo[e] = random.randint(0, 736)            # con random para que se mueva aleatoriamente
            eje_y_enemigo[e] = random.randint(50,200)            # para que se borre la nave
        
        # llamado de enemigo 
        enemigo(eje_x_enemigo[e], eje_y_enemigo[e], e)
    
    # disparar más balas
    if eje_y_bala <= -64:
        eje_y_bala = 500
        bala_visible = False

    # movimiento bala
    if bala_visible:
        disparar_bala(eje_x_bala, eje_y_bala)
        eje_y_bala -= bala_cambio_eje_y

    

    jugador(eje_x, eje_y)
    
    mostrar_puntaje(texto_x, texto_y)



    # Actualización el movimiento del programa
    pygame.display.update()