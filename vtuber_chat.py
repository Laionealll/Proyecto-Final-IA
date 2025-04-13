from io import BytesIO
import pygame
import sys
import threading
import openai
import os
import time
from pygame.locals import *
from elevenlabs import generate, set_api_key

# configuración
openai.api_key = "TU_API_KEY_OPENAI"  # open ai api
set_api_key("TU_API_KEY_ELEVENLABS")   # api elevenlabs
voice_id = "wBnAJRbu3cj93gnAm02O"       # id de voz eleven labs

WIDTH, HEIGHT = 720, 720
FPS = 60

estado = "reposo"           # estados: reposo, hablando, parpadeo
anim_toggle = False
last_toggle_time = time.time()
is_speaking = False
parpadeo_duration = 0.4
parpadeo_start_time = 0
lock_estado = threading.Lock()

def inicializar_mixer():
    # inicializa el mixer si no está iniciado
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            print("mixer iniciado")
            return True
        except Exception as e:
            print(f"error al iniciar mixer: {e}")
            return False
    return True

def obtener_respuesta(mensaje):
    # solicita respuesta a openai usando gpt-3.5-turbo
    try:
        print("obteniendo respuesta de openai...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "eres nina, una asistente anime kawaii, dulce y educada. hablas español de forma tierna, simpática y amigable. fuiste creada por laionel para su proyecto final."},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,
            max_tokens=200
        )
        respuesta = response.choices[0].message.content.strip()
        print(f"respuesta obtenida: {respuesta[:60]}...")
        return respuesta
    except Exception as e:
        print(f"error openai: {e}")
        return "lo siento, hubo un error. intenta de nuevo."

def hablar_kawaii(texto):
    # genera audio con elevenlabs en streaming, lo guarda, reproduce y elimina el archivo temporal
    global is_speaking
    is_speaking = True
    try:
        print(f"streaming audio para: '{texto[:50]}'")
        audio_stream = generate(
            text=texto,
            voice=voice_id,
            model="eleven_multilingual_v2",
            stream=True
        )
        if not inicializar_mixer():
            raise Exception("mixer no se pudo iniciar")
        temp_filename = f"temp_stream_{int(time.time() * 1000)}.mp3"
        audio_data = BytesIO()
        for chunk in audio_stream:
            audio_data.write(chunk)
        audio_data.seek(0)
        with open(temp_filename, "wb") as f:
            f.write(audio_data.read())
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"error al reproducir audio: {e}")
    finally:
        is_speaking = False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"error al detener audio: {e}")
        try:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        except Exception as e:
            print(f"error al eliminar archivo temporal: {e}")

def vtuber_habla(texto):
    # cambia a estado hablando, reproduce audio y vuelve a reposo
    global estado, last_toggle_time, anim_toggle, is_speaking
    with lock_estado:
        estado = "hablando"
        anim_toggle = False
        last_toggle_time = time.time()
        is_speaking = True
    def reproducir():
        hablar_kawaii(texto)
        with lock_estado:
            estado = "reposo"
    threading.Thread(target=reproducir, daemon=True).start()

def iniciar_parpadeo_automatico():
    # cambia a estado parpadeo si está en reposo
    def parpadeo():
        global estado, parpadeo_start_time, is_speaking
        while True:
            time.sleep(3)
            with lock_estado:
                if estado == "reposo" and not is_speaking:
                    estado = "parpadeo"
                    parpadeo_start_time = time.time()
    threading.Thread(target=parpadeo, daemon=True).start()

def main():
    # inicia pygame, carga imágenes, atiende eventos y muestra animación
    global estado, anim_toggle, last_toggle_time, parpadeo_start_time
    pygame.init()
    inicializar_mixer()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("vtuber nina")
    font = pygame.font.SysFont("arial", 24)
    try:
        vtuber_reposo = pygame.transform.scale(pygame.image.load("images/1.png").convert_alpha(), (500, 600))
        vtuber_boca = pygame.transform.scale(pygame.image.load("images/2.png").convert_alpha(), (500, 600))
        vtuber_parpadeo = pygame.transform.scale(pygame.image.load("images/3.png").convert_alpha(), (500, 600))
    except Exception as e:
        print(f"error al cargar imágenes: {e}")
        pygame.quit()
        sys.exit()
    vtuber_imgs = {
        "reposo": vtuber_reposo,
        "boca_abierta": vtuber_boca,
        "parpadeo": vtuber_parpadeo
    }
    input_box = pygame.Rect(50, 640, 620, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    user_text = ""
    iniciar_parpadeo_automatico()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and user_text.strip() != "":
                        mensaje = user_text
                        user_text = ""
                        def procesar_mensaje():
                            respuesta = obtener_respuesta(mensaje)
                            vtuber_habla(respuesta)
                        threading.Thread(target=procesar_mensaje, daemon=True).start()
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
        screen.fill((255, 228, 250))
        with lock_estado:
            current_time = time.time()
            if estado == "parpadeo" and (current_time - parpadeo_start_time >= parpadeo_duration):
                estado = "reposo"
            current_estado = estado
            speaking_status = is_speaking
        if current_estado == "parpadeo":
            current_image = vtuber_imgs["parpadeo"]
        elif current_estado == "hablando" and speaking_status:
            if current_time - last_toggle_time >= 0.2:
                anim_toggle = not anim_toggle
                last_toggle_time = current_time
            current_image = vtuber_imgs["boca_abierta"] if anim_toggle else vtuber_imgs["reposo"]
        else:
            current_image = vtuber_imgs["reposo"]
        screen.blit(current_image, (110, 20))
        txt_surface = font.render(user_text, True, (0, 0, 0))
        input_box.w = max(500, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        estado_txt = font.render(f"estado: {current_estado}", True, (0, 0, 0))
        screen.blit(estado_txt, (50, 600))
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
