"""
Generador de video PATS con Veo 3 (image-to-video)
Toma las imagenes 1.png a 8.png y genera clips con movimiento cinematografico.
Luego los une en un solo video con FFmpeg.
"""

import os
import time
import subprocess
from pathlib import Path
from google import genai
from google.genai import types

# ── Configuracion ──────────────────────────────────────────────────
API_KEY_FILE = Path(__file__).parent / "api_veo3.txt"
IMAGENES_DIR = Path(__file__).parent / "Imagenes"
OUTPUT_DIR   = Path(__file__).parent / "video_clips"
VIDEO_FINAL  = Path(__file__).parent / "pats_video_final.mp4"

MODEL = "veo-3.0-generate-001"   # opciones: veo-3.1-generate-preview (mas nuevo), veo-3.0-fast-generate-001 (mas rapido/barato)

# Prompt cinematografico para cada imagen
PROMPTS = {
    "1.png": "Cinematic slow pan over a rural Peruvian Andean community with dirt roads, warm sunlight, gentle breeze moving the crops, documentary style",
    "2.png": "Smooth drone dolly forward along a rural dirt path in the Peruvian Andes, mountains in background, golden hour light",
    "3.png": "Cinematic slow zoom in on a rural Peruvian village, adobe houses, Andean mountains, soft natural light",
    "4.png": "Smooth forward drive on a paved Andean highway in Peru, mountains flanking both sides, clear blue sky",
    "5.png": "Cinematic crane shot slowly descending over a rehabilitated rural Peruvian road, community visible in distance",
    "6.png": "Slow cinematic pan across a wide Peruvian Andean valley with improved roads connecting villages",
    "7.png": "Documentary style slow push in on a modern paved road through Peruvian highlands, trucks passing",
    "8.png": "Aerial drone shot slowly rising to reveal a connected Peruvian Andean road network, golden hour",
}

DURACION_SEGUNDOS = 5   # 5 segundos por clip (max 8)
ASPECT_RATIO      = "16:9"

# ── Setup ──────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(exist_ok=True)

api_key = API_KEY_FILE.read_text().strip()
client  = genai.Client(api_key=api_key)

def generar_clip(imagen_nombre: str, index: int) -> Path | None:
    imagen_path = IMAGENES_DIR / imagen_nombre
    output_path = OUTPUT_DIR / f"clip_{index:02d}.mp4"

    if output_path.exists():
        print(f"  [OK] clip_{index:02d}.mp4 ya existe, saltando.")
        return output_path

    if not imagen_path.exists():
        print(f"  [!] No se encontro {imagen_path}")
        return None

    print(f"\n[{index}/8] Generando video para {imagen_nombre}...")
    print(f"  Prompt: {PROMPTS.get(imagen_nombre, 'Cinematic Peruvian landscape')[:60]}...")

    try:
        img_bytes = imagen_path.read_bytes()
        image = types.Image(image_bytes=img_bytes, mime_type="image/png")

        operation = client.models.generate_videos(
            model=MODEL,
            prompt=PROMPTS.get(imagen_nombre, "Cinematic Peruvian Andean landscape, smooth camera movement"),
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio=ASPECT_RATIO,
                number_of_videos=1,
            ),
        )

        print(f"  Esperando generacion (puede tomar 1-3 minutos)...")
        intentos = 0
        while not operation.done:
            time.sleep(15)
            operation = client.operations.get(operation)
            intentos += 1
            print(f"  ... {intentos * 15}s transcurridos")
            if intentos > 24:  # max 6 minutos
                print("  [!] Timeout esperando el video")
                return None

        if not operation.response.generated_videos:
            print("  [!] No se genero video en la respuesta")
            return None

        video = operation.response.generated_videos[0].video
        client.files.download(file=video)
        video.save(str(output_path))
        print(f"  [OK] Guardado: {output_path.name}")
        return output_path

    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def unir_clips(clips: list[Path]) -> None:
    if not clips:
        print("\n[!] No hay clips para unir.")
        return

    lista_file = OUTPUT_DIR / "lista.txt"
    with open(lista_file, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.resolve()}'\n")

    print(f"\nUniendo {len(clips)} clips con FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(lista_file),
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        str(VIDEO_FINAL)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\n[✓] Video final guardado en:\n    {VIDEO_FINAL}")
    else:
        print(f"\n[ERROR] FFmpeg: {result.stderr[-400:]}")

# ── Main ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  PATS · Generador de video con Veo 3")
    print("=" * 60)

    imagenes = [f"{i}.png" for i in range(1, 9)]
    clips_generados = []

    for i, nombre in enumerate(imagenes, 1):
        clip = generar_clip(nombre, i)
        if clip:
            clips_generados.append(clip)
        time.sleep(2)  # pausa entre llamadas a la API

    print(f"\n{len(clips_generados)} de {len(imagenes)} clips generados.")
    unir_clips(clips_generados)
    print("\nListo.")
