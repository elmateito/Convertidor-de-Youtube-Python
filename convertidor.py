from pytube import YouTube
import customtkinter as ct
from tkinter import END
from tkinter import messagebox as mb
import os

#mostrar error
def showerr():
    mb.showerror('Error al buscar URL','Revise la URL e intentelo de nuevo')

#descarga
def downloadVid():
    if link.get() == '':
        mb.showwarning('Advertencia', 'Ingrese una URL')
    else:
        try:
            getEntry = link.get()
            content = YouTube(getEntry)
            format = vidResBox.get().lower()
            if format == 'formatos de video':
                mb.showwarning('Formato de archivo', 'Seleccione el formato al que desea convertir el video')
            else:
                getVid = content.streams.get_highest_resolution().download(output_path='video')
                base, ext = os.path.splitext(getVid)
                saved = base + format
                os.rename(getVid, saved) 
        except:
            showerr()

def downloadSnd():
    if link.get() == '':
        mb.showwarning('Advertencia', 'Ingrese una URL')
    else:
        try:
            getEntry = link.get()
            content = YouTube(getEntry)
            format = sndResBox.get().lower()
            if format == 'formatos de audio':
                mb.showwarning('Formato de archivo', 'Seleccione el formato al que desea convertir el video')
            else:
                getSnd = content.streams.get_audio_only().download(output_path='audio')
                base, ext = os.path.splitext(getSnd)
                saved = base + format
                os.rename(getSnd, saved)              
        except:
            showerr()

#instanciar de ventna Tk
main = ct.CTk()
ct.set_default_color_theme("dark-blue")
ct.set_appearance_mode("dark")
main.title('Convertidor de Youtube')
main.configure(background='#161a1d')
main.iconbitmap('appicon/youtube.ico')

#centrar ventana de app
appw = 450
apph = 250
screenw = main.winfo_screenwidth()
screenh = main.winfo_screenheight()
x = (screenw//2)-(appw//2)
y = (screenh//2)-(apph//2)
main.geometry(f'{appw}x{apph}+{x}+{y}')
main.resizable(width=False, height=False)

#button fonts
btnFont = ct.CTkFont(family="consolas bold", size=14)

#texto = Title
txt = ct.CTkLabel(master=main, text='Ingrese el link del video a convertir:', 
                  font=('consolas bold', 18), pady=10, padx=20)
txt.grid(row=0, column=0, columnspan=2)

#entry - Entrada de link de YT
link = ct.CTkEntry(master=main, width=340, height=30,border_width=2, 
                   corner_radius=5, font=('consolas', 16))
link.grid(row=1, column=0, columnspan=2, pady=15, padx=20)

btnClear = ct.CTkButton(master=main, font=(btnFont), text='Limpiar entrada', command=lambda: link.delete(0,END))
btnClear.grid(row=3, column=0, columnspan=2, pady=5)

#button - Descargar vid
vidRes = ['.AVI', '.MP4']
vidResBox = ct.CTkComboBox(master=main, values=vidRes, font=('consolas', 12), width=160)
vidResBox.grid(row=4, column=0, pady=15)
vidResBox.set('Formatos de video')
btnVid = ct.CTkButton(master=main, font=(btnFont),text='Descarga video', command=downloadVid)
btnVid.grid(row=5, column=0, pady=10) 

#button - Descargar audio
sndRes = ['.WAV', '.MP3']
sndResBox = ct.CTkComboBox(master=main, values=sndRes, font=('consolas', 12), width=160)
sndResBox.grid(row=4, column=1, pady=15)
sndResBox.set('Formatos de audio')
btnSnd = ct.CTkButton(master=main, font=(btnFont),text='Descarga audio', command=downloadSnd)
btnSnd.grid(row=5, column=1, pady=10)

main.mainloop()
