# VTuber Nina: Asistente Virtual Anime con Voz e Inteligencia Artificial

**VTuber Nina** es un proyecto de asistente virtual en forma de una chica anime kawaii, programada para interactuar de manera simpática y natural con los usuarios. Utiliza inteligencia artificial avanzada para comprender preguntas por texto o voz y responder con una voz realista generada por ElevenLabs. Fue creada como parte de un proyecto final con un enfoque educativo, divertido e interactivo.

## 🚀 Características principales

- Interfaz visual animada (reposo, parpadeo y hablando)
- Chat en tiempo real con IA (GPT-4o)
- Reconocimiento de voz con Whisper
- Generación de audio realista con ElevenLabs
- Parpadeo automático mientras está en reposo
- Activación por texto o por micrófono (tecla V)

## 🎧 Tecnologías y librerías utilizadas

- `pygame`: Para la interfaz visual y animaciones
- `openai`: Para usar el modelo GPT-4o y Whisper
- `sounddevice`: Para grabar audio desde el micrófono
- `scipy`: Para guardar la grabación en formato WAV
- `elevenlabs`: Para generar audio de voz natural en español

## 🌐 Requisitos previos

Asegúrate de tener Python 3.8+ y las siguientes librerías instaladas:

```bash
pip install pygame openai sounddevice scipy elevenlabs
```

> **Nota:** Necesitarás claves de API de OpenAI y ElevenLabs para ejecutar el proyecto.

## 🎓 Configuración de APIs

Edita las siguientes líneas al inicio del archivo `vtuber_chat.py` con tus claves personales:

```python
openai.api_key = "TU_CLAVE_OPENAI"
set_api_key("TU_CLAVE_ELEVENLABS")
voice_id = "ID_DE_VOZ_ELEVENLABS"
```

## 🏋️ Instrucciones de uso

1. Asegúrate de tener una carpeta `images/` con las tres imágenes necesarias:
    - `1.png`: rostro normal
    - `2.png`: con boca abierta (hablando)
    - `3.png`: parpadeando

2. Ejecuta el programa:

```bash
python vtuber_chat.py
```

3. Puedes interactuar escribiendo en la caja de texto o presionando la tecla **`V`** para hablar por micrófono.

## 🧵 Autor

Este proyecto fue desarrollado por **Laioneall** como parte de un trabajo final de programación e inteligencia artificial.

---

✨ **VTuber Nina** no es solo una herramienta educativa, sino una experiencia encantadora e interactiva que mezcla tecnología de punta con arte digital. ¡Ideal para proyectos de IA conversacional y entretenimiento virtual!

---


> hecho con mucho amor por **Laioneall Williams** 
> matrícula: `23-EISN-2-035`
