#!/usr/bin/env python3
"""
Convertidor de YouTube/YouTube Music a audio
Descarga canciones, playlists y albumes en multiples formatos.
"""

import yt_dlp
import os
import sys
import shutil
import argparse
from pathlib import Path

SUPPORTED_FORMATS = ['mp3', 'flac', 'aac', 'opus', 'm4a', 'wav']
SUPPORTED_BROWSERS = ['chrome', 'firefox', 'edge', 'brave', 'opera', 'vivaldi']
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

def check_ffmpeg():
    """Verifica si ffmpeg esta instalado."""
    return shutil.which('ffmpeg') is not None

def progress_hook(d):
    """Muestra el progreso de la descarga."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r  Descargando: {percent} | Velocidad: {speed} | ETA: {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\n  Descarga completa. Procesando audio...")

def download_music(url, audio_format='mp3', output_dir=None, browser=None, cookies_file=None):
    """
    Descarga audio desde YouTube o YouTube Music.

    Args:
        url: URL del video o playlist
        audio_format: Formato de audio (mp3, flac, aac, opus, m4a, wav)
        output_dir: Directorio de salida
        browser: Nombre del navegador para extraer cookies
        cookies_file: Ruta al archivo de cookies
    """
    if audio_format not in SUPPORTED_FORMATS:
        print(f"Error: Formato '{audio_format}' no soportado.")
        print(f"Formatos validos: {', '.join(SUPPORTED_FORMATS)}")
        return False

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)

    use_ffmpeg = check_ffmpeg()
    if not use_ffmpeg:
        print("Advertencia: ffmpeg no encontrado. El audio NO sera convertido.")
        print("Instale ffmpeg: sudo pacman -S ffmpeg")
        print("Se descargara el archivo original.\n")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'addmetadata': True,
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'no_warnings': False,
    }

    # Autenticacion con cookies
    if browser:
        ydl_opts['cookiesfrombrowser'] = (browser,)
        print(f"Usando cookies del navegador: {browser}")
    elif cookies_file:
        if not os.path.exists(cookies_file):
            print(f"Error: Archivo de cookies no encontrado: {cookies_file}")
            return False
        ydl_opts['cookiefile'] = cookies_file
        print(f"Usando archivo de cookies: {cookies_file}")
    else:
        print("Sin autenticacion. Si hay error, use --browser o --cookies")

    if use_ffmpeg:
        ydl_opts['postprocessors'] = [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '0',
            },
            {
                'key': 'FFmpegThumbnail',
            },
            {
                'key': 'FFmpegMetadata',
            },
        ]

    try:
        print(f"\n{'='*50}")
        print(f"URL: {url}")
        print(f"Formato: {audio_format.upper()}")
        print(f"Directorio: {output_dir}")
        print(f"{'='*50}\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"\n{'='*50}")
        print("Descarga completada exitosamente!")
        print(f"Archivos guardados en: {output_dir}")
        print(f"{'='*50}\n")
        return True

    except Exception as e:
        print(f"\nError durante la descarga: {e}")
        return False

def interactive_mode():
    """Modo interactivo para descargar musica."""
    print("\n" + "="*50)
    print("  CONVERTIDOR DE YOUTUBE MUSIC")
    print("="*50)

    if not check_ffmpeg():
        print("\nAdvertencia: ffmpeg no instalado.")
        print("Para conversion de audio: sudo pacman -S ffmpeg\n")

    url = input("\nIngrese la URL de YouTube o YouTube Music: ").strip()
    if not url:
        print("URL invalida.")
        return

    print(f"\nFormatos disponibles: {', '.join(SUPPORTED_FORMATS)}")
    fmt = input("Formato de audio [mp3]: ").strip().lower() or 'mp3'

    if fmt not in SUPPORTED_FORMATS:
        print(f"Formato '{fmt}' no valido. Usando mp3.")
        fmt = 'mp3'

    out = input(f"Directorio de salida [{DEFAULT_OUTPUT_DIR}]: ").strip() or None

    # Preguntar por autenticacion
    print("\n--- Autenticacion (opcional) ---")
    print("Si YouTube pide login, seleccione su navegador o indique archivo de cookies.")
    print(f"Navegadores soportados: {', '.join(SUPPORTED_BROWSERS)}")
    auth_choice = input("Metodo de autenticacion (navegador/cookies/ninguno) [ninguno]: ").strip().lower() or 'ninguno'

    browser = None
    cookies_file = None

    if auth_choice in SUPPORTED_BROWSERS:
        browser = auth_choice
    elif auth_choice == 'cookies':
        cookies_file = input("Ruta al archivo de cookies: ").strip()
        if not cookies_file:
            print("Ruta invalida. Continuando sin autenticacion.")
            cookies_file = None
    elif auth_choice not in ('ninguno', 'no', 'n', ''):
        print(f"Opcion '{auth_choice}' no reconocida. Continuando sin autenticacion.")

    download_music(url, audio_format=fmt, output_dir=out, browser=browser, cookies_file=cookies_file)

def main():
    """Punto de entrada principal."""
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Modo CLI legacy: python convertidor.py URL [formato]
        url = sys.argv[1]
        fmt = sys.argv[2] if len(sys.argv) > 2 else 'mp3'
        out = sys.argv[3] if len(sys.argv) > 3 else None
        download_music(url, audio_format=fmt, output_dir=out)
    elif len(sys.argv) > 1:
        # Modo CLI con argparse
        parser = argparse.ArgumentParser(
            description='Convertidor de YouTube/YouTube Music a audio',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Ejemplos:
  %(prog)s "https://music.youtube.com/watch?v=..."
  %(prog)s "URL" --format flac --browser firefox
  %(prog)s "URL" --cookies cookies.txt
  %(prog)s "URL" --format mp3 --output ./musica
            '''
        )

        parser.add_argument('url', help='URL de YouTube o YouTube Music')
        parser.add_argument('-f', '--format', default='mp3',
                          choices=SUPPORTED_FORMATS,
                          help='Formato de audio (default: mp3)')
        parser.add_argument('-o', '--output', default=None,
                          help=f'Directorio de salida (default: {DEFAULT_OUTPUT_DIR})')
        parser.add_argument('-b', '--browser', default=None,
                          choices=SUPPORTED_BROWSERS,
                          help='Navegador para extraer cookies de autenticacion')
        parser.add_argument('-c', '--cookies', default=None,
                          help='Ruta al archivo de cookies (formato Netscape)')

        args = parser.parse_args()

        download_music(
            url=args.url,
            audio_format=args.format,
            output_dir=args.output,
            browser=args.browser,
            cookies_file=args.cookies
        )
    else:
        # Modo interactivo
        interactive_mode()

if __name__ == '__main__':
    main()
