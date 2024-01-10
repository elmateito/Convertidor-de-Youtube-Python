from pytube import YouTube

from tkinter import Tk
from tkinter import Label
from tkinter import Menu
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox as mb

#mostrar créditos
def infobox():
    mb.showinfo('Créditos', 'Realizado por: elmateito - 2024\nGitHub: @elmateito')

#descargar video
def video():
    if link.get() == "":
        mb.showwarning('Advertencia', 'Ingrese una URL')
    else:
        try:
            getEntry = link.get()
            vid = YouTube(getEntry)
            getVid = vid.streams.get_highest_resolution().download()
        except:
            mb.showerror('Error al buscar URL','Revise la URL e intentelo de nuevo')

#descargar sonido
def sound():
    if link.get() == "":
        mb.showwarning('Advertencia', 'Ingrese una URL')
    else: 
        try:
            getEntry = link.get()
            snd = YouTube(getEntry)
            getSnd = snd.streams.get_audio_only().download()
        except:
            mb.showerror('Error al buscar URL','Revise la URL e intentelo de nuevo')

#instanciar de ventna Tk
main = Tk()
main.title('Convertidor de Youtube')
main.configure(background='#161a1d')
main.iconbitmap('youtube.ico')

#centrar ventana de app
appw = 450
apph = 180
screenw = main.winfo_screenwidth()
screenh = main.winfo_screenheight()
x = (screenw//2)-(appw//2)
y = (screenh//2)-(apph//2)
main.geometry(f'{appw}x{apph}+{x}+{y}')
main.resizable(width=False, height=False)

#menu - Acerca De
navbar = Menu(main, background='#f0f0f0')
main.config(menu = navbar)
info = Menu(navbar, tearoff=0, background='#f0f0f0')

navbar.add_cascade(label='Acerca de', menu=info)
info.add_command(label='Créditos',command=infobox)

#texto = Title
txt = Label(main, text='Ingrese el link del video a convertir:', font="consolas 14", bg='#161a1d', fg='white', pady=10, padx=20)
txt.grid(row=0, column=0, columnspan=2)

#entry - Entrada de link de YT
link = Entry(main, font='consolas 12', width=45, bg='#f0f0f0')
link.grid(row=1, column=0, columnspan=2, pady=15, padx=20)

#button - Descargar vid
btnVid = Button(main, text='Descargar video', font="consolas 11", command=video)
btnVid.grid(row=2, column=0, pady=15)

#button - Descargar audio
btnSnd = Button(main, text='Descargar audio', font="consolas 11", command=sound)
btnSnd.grid(row=2, column=1, pady=15)

main.mainloop()
