from pytubefix import YouTube
from customtkinter import CTk, set_appearance_mode, set_default_color_theme, CTkFont, CTkLabel, CTkEntry, CTkButton, CTkComboBox, CTkTabview, CTkTextbox
from tkinter import END, messagebox as mb
from os import rename, path

vidFormats, audFormats, historial  = ['.avi', '.mp4'], ['.wav', '.mp3'], {}

def update_history(title, url): # actualizar historial
    if len(historial) == 4:
        historial.pop(next(iter(historial)))
    historial[title] = url  
    render_history()

def render_history(): # render historial
    if historial: labelHistorial.grid_remove()
    for videoInd, (titleyt, linkyt) in enumerate(historial.items(), start=2):
        links = CTkTextbox(navbar.tab('Historial'), height=60, width=449, font=('consolas bold', 16))
        links.grid(row=videoInd, column=0, columnspan=2, pady=3, padx=5)
        links.insert(END, f'{videoInd-1}. {titleyt}:\n{linkyt}')
        links.configure(state='disabled')

def download(format): #descarga
    url = link.get()
    if not url:
        mb.showwarning('Advertencia', 'Ingrese una URL')
        return
    if format not in vidFormats + audFormats:
        mb.showwarning('Formato de archivo', 'Seleccione un formato válido')
        return
    try:
        content = YouTube(url)
        if format in vidFormats:
            file = content.streams.get_highest_resolution().download(output_path='media/video')
        else:
            file = content.streams.get_audio_only().download(output_path='media/audio')
        if format != '.mp4':  
            filename, _ = path.splitext(file)
            rename(file, filename + format)
        update_history(content.title, url)
    except Exception:
        mb.showerror('Error al buscar URL', 'Revise la URL e intentelo de nuevo')

#instanciar de ventana Tk
main = CTk()
main.title('Convertidor de Youtube')
main.configure(background='#161a1d')
set_default_color_theme("dark-blue")
set_appearance_mode("dark")
appw, apph = 490, 320
x, y = (main.winfo_screenwidth()//2 - appw//2), (main.winfo_screenheight()//2 - apph//2)
main.geometry(f'{appw}x{apph}+{x}+{y}')
main.resizable(width=False, height=False)
btnFont = CTkFont(family="consolas bold", size=16) #button fonts

#tabs
navbar = CTkTabview(main)
navbar._segmented_button.configure(font=btnFont)
navbar.grid(padx=10)
navbar.add('Inicio')
navbar.add('Historial')

#texto - Title
CTkLabel(navbar.tab('Inicio'), text='Ingrese el link del video a convertir:',
         font=('consolas bold', 20), pady=10, padx=20).grid(row=1, column=0, columnspan=2)

# entrada - Entrada de link de YT
link = CTkEntry(navbar.tab('Inicio'), width=375, height=30, border_width=2, corner_radius=5, font=('consolas', 18))
link.grid(row=2, column=0, columnspan=2, pady=10)

# limpiar entrada
CTkButton(navbar.tab('Inicio'), font=btnFont, text='Limpiar entrada', 
         command=lambda: link.delete(0, END)).grid(row=4, column=0, columnspan=2, pady=10)

# selección formato y btn descarga de video y audio
vidResBox = CTkComboBox(navbar.tab('Inicio'), values=[fmt.upper() for fmt in vidFormats], 
                        font=('consolas', 14), width=175)
vidResBox.grid(row=5, column=0, pady=15)
vidResBox.set('Formatos de video')
CTkButton(navbar.tab('Inicio'), font=btnFont, text='Descarga video', 
         command=lambda: download(vidResBox.get().lower())).grid(row=6, column=0, pady=10)

# selección formato y btn descarga de audio
sndResBox = CTkComboBox(navbar.tab('Inicio'), values=[fmt.upper() for fmt in audFormats], 
                        font=('consolas', 14), width=175)
sndResBox.grid(row=5, column=1, pady=15)
sndResBox.set('Formatos de audio')
CTkButton(navbar.tab('Inicio'), font=btnFont, text='Descarga audio', 
         command=lambda: download(sndResBox.get().lower())).grid(row=6, column=1, pady=10)

# historial
labelHistorial = CTkLabel(navbar.tab('Historial'), text='Sin descargas existentes', 
         font=('consolas bold', 20), pady=50, width=459)
labelHistorial.grid(row=1, column=0, columnspan=2)

main.mainloop()