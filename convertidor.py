from pytube import YouTube
from customtkinter import CTk, set_appearance_mode, set_default_color_theme, CTkFont, CTkLabel, CTkEntry, CTkButton, CTkComboBox, CTkTabview, CTkTextbox
from tkinter import END, messagebox as mb
from os import rename, path    

#descarga
def download(format):
    if link.get() == '':
        mb.showwarning('Advertencia', 'Ingrese una URL')
    elif format == 'formatos de video' or format == 'formatos de audio':
        mb.showwarning('Formato de archivo', 'Seleccione el formato al que desea convertir el video')
    else:
        try:
            content = YouTube(link.get())
            title = content.title
            if format == 'formatos de video' or format == 'formatos de audio':
                mb.showwarning('Formato de archivo', 'Seleccione el formato al que desea convertir el video')
            elif format == '.avi': 
                    getVid = content.streams.get_highest_resolution().download(output_path='media/video')
                    filename, old = path.splitext(getVid)
                    saved = filename + format
                    rename(getVid, saved)
            elif format == '.mp4':
                    getVid = content.streams.get_highest_resolution().download(output_path='media/video')
            elif format == '.wav' or format == '.mp3':
                    getSnd = content.streams.get_audio_only().download(output_path='media/audio')
                    filename, old = path.splitext(getSnd)
                    saved = filename + format
                    rename(getSnd, saved)
        except:
            mb.showerror('Error al buscar URL','Revise la URL e intentelo de nuevo')
        if len(historial) == 4:
            historial.pop(next(iter(historial)))
        historial[title] = link.get()  
        j = 3
        for titleyt, linkyt in historial.items():
            links = CTkTextbox(navbar.tab('Historial'), height=51, width=390,font=('consolas', 14))
            links.grid(row=j, column=0, columnspan=2)
            links.insert(END, f'{j-2}. {titleyt}:\n{linkyt}')
            links.configure(state='disabled')
            j += 1

#instanciar de ventana Tk
main = CTk()
main.title('Convertidor de Youtube')
main.configure(background='#161a1d')
#main.iconbitmap('./icon/youtube.ico')
set_default_color_theme("dark-blue")
set_appearance_mode("dark")

#centrar ventana de app
appw = 450
apph = 305
screenw = main.winfo_screenwidth()
screenh = main.winfo_screenheight()
x = (screenw//2)-(appw//2)
y = (screenh//2)-(apph//2)
main.geometry(f'{appw}x{apph}+{x}+{y}')
main.resizable(width=False, height=False)

#button fonts
btnFont = CTkFont(family="consolas bold", size=14)

#tabs
navbar = CTkTabview(main)
navbar._segmented_button.configure(font=btnFont)
navbar.grid(padx=10)
navbar.add('Inicio')
navbar.add('Historial')

#texto = Title
txt = CTkLabel(master=navbar.tab('Inicio'), text='Ingrese el link del video a convertir:', 
                  font=('consolas bold', 18), pady=10, padx=20).grid(row=1, column=0, columnspan=2)

#entry - Entrada de link de YT
link = CTkEntry(master=navbar.tab('Inicio'), width=375, height=30, border_width=2, 
                   corner_radius=5, font=('consolas', 16))
link.grid(row=2, column=0, columnspan=2, pady=10)

btnClear = CTkButton(master=navbar.tab('Inicio'), font=(btnFont), text='Limpiar entrada', 
                        command=lambda: link.delete(0,END)).grid(row=4, column=0, columnspan=2, pady=10)

#button - Descargar video
vidRes = ['.AVI', '.MP4']
vidResBox = CTkComboBox(master=navbar.tab('Inicio'), values=vidRes, font=('consolas', 12), width=160)
vidResBox.grid(row=5, column=0, pady=15)
vidResBox.set('Formatos de video')
btnVid = CTkButton(master=navbar.tab('Inicio'), font=(btnFont), text='Descarga video', 
                   command=lambda: download(vidResBox.get().lower())).grid(row=6, column=0, pady=10) 

#button - Descargar audio
sndRes = ['.WAV', '.MP3']
sndResBox = CTkComboBox(master=navbar.tab('Inicio'), values=sndRes, font=('consolas', 12), width=160)
sndResBox.grid(row=5, column=1, pady=15)
sndResBox.set('Formatos de audio')
btnSnd = CTkButton(master=navbar.tab('Inicio'), font=(btnFont), text='Descarga audio', 
                   command=lambda: download(sndResBox.get().lower())).grid(row=6, column=1, pady=10)

#historial
histLabel = CTkLabel(master=navbar.tab('Historial'), text='Historial de Descargas', 
                    font=('consolas bold', 18), pady=10, width=420).grid(row=1, column=0, columnspan=2)
historial = {}

main.mainloop()