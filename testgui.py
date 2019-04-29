from tkinter import *
import tkinter.font as tkf
from numpy.random import *
import numpy as np
from numpy import sin, cos, exp, sqrt, log, tan, arccos, arcsin, arctan, sinc, pi
import time
import importlib
import fc
import edit_vector_field
import vitx
import vity
import vitr
import vitth

importlib.reload(edit_vector_field)
#from numba import vectorize

tk = Tk()
height = 500
width = 500
bg_buttons = "#222222"
fg_buttons = "#ffffff"
ofont = ("Courrier", 10)
tk.geometry("500x500")
frame = Frame(tk, bg='#ffffff', bd=0)
toolbar = Frame(tk, width=width, height = 30, bg=bg_buttons)
options = Frame(tk,width = width, height = 30, bg = bg_buttons)
frame.pack()
toolbar.place(x=0, y=0)
options.place(x=0, y=height-30)
canvas = Canvas(frame, width=width, height=height, bd=0, highlightthickness=0)
tk.title("Vector Field Generator")
canvas.pack()
canvas.configure(background="#000000")
bg_buttons = "#222222"
fg_buttons = "#ffffff"
ofont = ("Courrier", 10)

def zoomplus():
    global fenetre
    global fenetre_initiale
    global long
    global v

    fenetre = np.divide(fenetre, 2)
    fenetre_initiale/=2
    fc.reset_vectors(gouttes, canvas)

def zoommoins():
    global fenetre
    global fenetre_initiale

    global long
    global v
    fenetre*=2
    fenetre_initiale*=2
    fc.reset_vectors(gouttes, canvas)

zoom_plus_button = Button(toolbar, text="+", width=1, height = 1, bg=bg_buttons, fg = fg_buttons, command = zoomplus, font=ofont)
zoom_plus_button.grid(row=0, column=0)
zoom_moins_button = Button(toolbar, text="-", width=1, height = 1, bg=bg_buttons, fg = fg_buttons, command = zoommoins, font=ofont)
zoom_moins_button.grid(row=0, column=1)

time_disp_label = Label(toolbar, text="", width=10, height = 2, bg=bg_buttons, fg = fg_buttons, font=ofont)
time_disp_label.grid(row = 0, column=2)

def reset_time():
    global t
    t=0
    return

time_reset_button = Button(toolbar, text="t=0", width=1, height = 1, bg=bg_buttons, fg = fg_buttons, command = reset_time, font=ofont)
time_reset_button.grid(row = 0, column = 3)

def print_on_label(label, toprint):
    label.config(text=toprint)

no_time = False
def stop_time():
    global no_time
    no_time = not no_time
    if no_time:
        stop_time_button.config(text="Make Dynamic")
    else:
        stop_time_button.config(text="Make Static")

stop_time_button = Button(toolbar,text="Make Static",width=12, height = 1, bg=bg_buttons, fg = fg_buttons, command = stop_time, font=ofont)
stop_time_button.grid(row=0, column=4)

fenetre_label = Label(toolbar, text="", width=20, height = 2, bg=bg_buttons, fg = fg_buttons, font=ofont)
fenetre_label.grid(row = 0, column=5)

def slow_down():
    global v
    v/=2
slow_down_button = Button(toolbar, text = "Slow Down Vectors", height = 1, bg=bg_buttons, fg = fg_buttons, command = slow_down, font=ofont)
slow_down_button.grid(row = 0, column = 6)

def speed_up():
    global v
    v*=2
speed_up_button = Button(toolbar, text = "Speed Up Vectors", height = 1, bg=bg_buttons, fg = fg_buttons, command = speed_up, font=ofont)
speed_up_button.grid(row = 0, column = 7)

def shorten_vec_len():
    global long
    long/=2
shorten_button = Button(toolbar, text = "Shorten Vectors", height = 1, bg=bg_buttons, fg = fg_buttons, command = shorten_vec_len, font=ofont)
shorten_button.grid(row = 0, column = 8)

def extend_vec_len():
    global long
    long*=2
extend_button = Button(toolbar, text = "Extend Vectors", height = 1, bg=bg_buttons, fg = fg_buttons, command = extend_vec_len, font=ofont)
extend_button.grid(row = 0, column = 9)


def reset_figure():
    global v
    global long
    global vmin
    global vmax
    global vmed
    vminp, vmaxp, vmedp = max_relation(fenetre, True, t=t)
    vminc, vmaxc, vmedc = max_relation(fenetre, False, t=t)
    if polaire:
        vmin = vminp
        vmax = vmaxp
        vmad = vmedp
    else:
        vmin = vminc
        vmax = vmaxc
        vmed = vmedc
    long = speedmod*min(longueur*200/vmax, longueur*100)
    v =  speedmod*dt*vitesse*25/vmax
    fc.reset_vectors(gouttes, canvas)
    return

reset_figure_button = Button(toolbar, text = "Auto Speed & Length", height = 1, bg=bg_buttons, fg = fg_buttons, command = reset_figure, font=ofont)
reset_figure_button.grid(row = 0, column = 10)

reset_vectors_button = Button(toolbar, text = "Reset Vectors", height = 1, bg=bg_buttons, fg = fg_buttons, command = lambda: fc.reset_vectors(gouttes, canvas), font=ofont)
reset_vectors_button.grid(row = 0, column = 11)


def change_coordinates(menu, p):
    global polaire
    global v
    global long
    global vmin
    global vmax
    global vmed
    polaire = not p
    if not p:
        vmin = vminp
        vmax = vmaxp
        vmad = vmedp
    else:
        vmin = vminc
        vmax = vmaxc
        vmed = vmedc
    long = speedmod*min(longueur*200/vmax, longueur*100)
    v =  speedmod*dt*vitesse*25/vmax
    if polaire:
        disp_menu_coord = "Set Cartesian Coordinates"
        label_vx.config(text="Vr")
        label_vy.config(text="Vth")
        button_change_coord.config(text="Cartesian")
    else:
        label_vx.config(text="Vx")
        label_vy.config(text="Vy")
        disp_menu_coord = "Set Polar Coordinates"
        button_change_coord.config(text="Polar")
    menu.entryconfig(3, label = disp_menu_coord)
    fc.reset_vectors(gouttes, canvas)
    return


fenetre_initiale = np.array([10.0, 10.0])
fenetre = fenetre_initiale
vitesse = 100
longueur = 7 * sqrt(fenetre[0]**2 + fenetre[1]**2)
lmax = 1
p_disparition = 0.000025*vitesse
t=0.01

dt = 0.001
polaire = False
if polaire:
    disp_menu_coord = "Set Cartesian Coordinates"
else:
    disp_menu_coord = "Set Polar Coordinates"

# Update Cartesian
def update_field(equation1, equation2, p, autosize):

    if p:
        print("Vr = "+equation1+"\nVth = "+equation2)
        edit_vector_field.edit_vr_func(equation1)
        edit_vector_field.edit_vth_func(equation2)
        importlib.reload(vitr)
        importlib.reload(vitth)
    else:
        print("Vx = "+equation1+"\nVy = "+equation2)
        edit_vector_field.edit_vx_func(equation1)
        edit_vector_field.edit_vy_func(equation2)
        importlib.reload(vitx)
        importlib.reload(vity)
    if autosize:
        reset_figure()
    return
new_vx = StringVar()
new_vy = StringVar()
label_vx = Label(options, text="Vx = ", height = 1, bg=bg_buttons, fg = fg_buttons, font=ofont)
label_vy = Label(options, text="Vy = ", height = 1, bg=bg_buttons, fg = fg_buttons, font=ofont)
entry_box_vx=Entry(options, textvariable=new_vx, width=30,bg=bg_buttons, fg = 'white', font=ofont)
entry_box_vy=Entry(options, textvariable=new_vy, width=30,bg=bg_buttons, fg = 'white', font=ofont)
label_vx.grid(row = 2, column = 1)
label_vy.grid(row = 2, column = 3)
entry_box_vx.grid(row = 2, column = 2)
entry_box_vy.grid(row = 2, column = 4)
button_updatefield = Button(options, text="Apply", height = 1, bg=bg_buttons, fg = fg_buttons, command = lambda: update_field(str(new_vx.get()), str(new_vy.get()), polaire, False), font=ofont, borderwidth=0)
button_updatefield2 = Button(options, text="Apply & Compute", height = 1, bg=bg_buttons, fg = fg_buttons, command = lambda: update_field(str(new_vx.get()), str(new_vy.get()), polaire, True), font=ofont, borderwidth=0)
button_updatefield.grid(row = 2, column = 5)
button_updatefield2.grid(row = 2, column = 6)



# Init Field
edit_vector_field.edit_vx_func("y*sin(10*t)")
edit_vector_field.edit_vy_func("x*cos(20*t)")
edit_vector_field.edit_vr_func("1")
edit_vector_field.edit_vth_func("r")
importlib.reload(vitx)
importlib.reload(vitr)
importlib.reload(vitth)
importlib.reload(vity)

#relation
def relation(x, y, t=0, polaire = False):
    x = x*fenetre[0]/width-fenetre[0]/2
    y = y*fenetre[1]/height-fenetre[1]/2
    vx = vitx.vx(x, y, t)
    vy = vity.vy(x, y, t)
    if polaire:
        # Conversion en coordonnées polaires
        r = np.sqrt(x**2+y**2)
        if r+x != 0:
            th = 2*np.arctan(y/(r+x))
        else:
            th = np.pi
        # Valeurs de vr et vth
        if abs(r) > 0:
            vr = vitr.vr(r, th, x, y, t)
        else:
            vr=0.0
        vth = vitth.vth(r, th, x, y, t)
        #conversion en coordonnées cartésiennes
        vx = np.cos(th)*vr - r * np.sin(th) * vth
        vy = np.sin(th)*vr + r * np.cos(th) * vth
    return np.array([vx, height/width*vy])

def max_relation(fenetre, p, t=0):
    nbpoints = 400
    allx = fenetre[0] * np.array([(i-nbpoints/2)/(nbpoints/2) for i in range(0,nbpoints)])
    ally = fenetre[1] * np.array([(i-nbpoints/2)/(nbpoints/2) for i in range(0,nbpoints)])
    values = []
    for x in allx:
        for y in ally:
            resx, resy = relation(x,y, t=t, polaire=p)
            values.append(np.sqrt(resx**2+resy**2))
    return min(values), max(values), np.percentile(np.abs(np.array(values)), 50)

vminp, vmaxp, vmedp = max_relation(fenetre, True, t)
vminc, vmaxc, vmedc = max_relation(fenetre, False, t)
if polaire:
    vmin = vminp
    vmax = vmaxp
    vmad = vmedp
else:
    vmin = vminc
    vmax = vmaxc
    vmed = vmedc
long = min(longueur*200/vmax, longueur*100)
v =  dt*vitesse*25/vmax

#Menu
menu_bar = Menu(tk)
file_menu= Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quit", command=tk.destroy)
file_menu.add_command(label= "Reset Vectors", command =lambda: fc.reset_vectors(gouttes, canvas))
file_menu.add_command(label="Reset time", command=lambda:reset_time())
file_menu.add_command(label = disp_menu_coord, command=lambda:change_coordinates(file_menu, polaire))
file_menu.add_command(label = "Reset Figure", command = reset_figure)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
tk.config(menu=menu_bar)

button_change_coord = Button(options, text = "Polar", width = 10, height = 1, bg=bg_buttons, fg = fg_buttons, command = lambda: change_coordinates(file_menu, polaire), font=ofont)
button_change_coord.grid(row = 2, column = 0)

def concatenatecolors(ro, vt, bl):
    r = hex(ro)[2:]
    if len(r)==1:
        r = "0"+r
    g = hex(vt)[2:]
    if len(g)==1:
        g = "0"+g
    b = hex(bl)[2:]
    if len(b)==1:
        b = "0"+b
    return "#"+r+g+b



class Goutte:
    def __init__(self, x,y):
        self.x=x
        self.y = y
        self.init_speed = np.array([0, 0])
        self.speed = relation(self.x,self.y, t, polaire = polaire)
        self.globalspeed = np.sqrt(self.speed[0]**2 + self.speed[1]**2)
        self.lengthx = v*self.speed[0]
        self.lengthy = v*self.speed[1]
        self.gui = canvas.create_line(self.x, self.y, self.x + self.lengthx, self.y + self.lengthy)
        self.length = np.sqrt(self.lengthx**2 + self.lengthy**2)

    def __str__(self):
        s = "x = "+str(self.x)+"\nY = "+str(self.y)+"\nl = "+str(self.length)+"\nSpeed = "+str(self.speed)
        return s
    def update(self):
        # updates properties
        self.y += v*self.speed[1]
        self.x += v*self.speed[0]
        self.globalspeed = np.sqrt(self.speed[0]**2 + self.speed[1]**2)
        self.length = np.sqrt(self.lengthx**2 + self.lengthy**2)
        self.lengthx = long * self.speed[0] / width
        self.lengthy = long * self.speed[1] / height

    def color(self):
        '''
        Updates the color of the vector
        '''
        r = int(255*(1-max(0,min(1, np.abs(self.globalspeed*0.5/vmin)))))
        g = int(255*((max(0,min(0.85, np.abs(self.globalspeed+2.5/vmax))))))
        b = int(255*((max(0,min(1,0.1*(self.globalspeed-0.7*vmax))))))#int(255-g)
        return concatenatecolors(r,g,b)

#@vectorize("g", target='gpu')
def affichage(g):
    g.speed = relation(g.x,g.y, t, polaire = polaire)
    g.update()
    canvas.coords(g.gui,g.x, g.y, g.x+v*g.speed[0]+g.lengthx,g.y+v*g.speed[1] + g.lengthy)
    canvas.itemconfigure(g.gui, fill=g.color())
    # Reset si sortie de l'écran
    if (not (0 < g.y < height)) or (not (0 < g.x < width)):
        g.y = height*rand()
        g.x = width*rand()
        g.init_speed = np.array([0, 0])
        g.speed = relation(g.x,g.y,t, polaire = polaire)
        g.lengthx = v*g.speed[0]
        g.lengthy = v*g.speed[1]
        g.length = np.sqrt(g.lengthx**2 + g.lengthy**2)
        canvas.coords(g.gui, g.x, g.y, g.x + g.lengthx, g.y + g.lengthy)
    #choix des vecteurs supprimés
    if rand() < p_disparition or np.abs(g.lengthx)>width*lmax or np.abs(g.lengthy)>height*lmax:
        to_del.append(k)
        canvas.delete(g.gui)
    return



gouttes = []
nbgouttes = int(width*height/250)
for i in range(nbgouttes):
    g = Goutte(width*rand(), height*rand())
    gouttes.append(g)

t=0.01
speedmod = 1
longmod = 1
new_f0 = fenetre[0]
new_f1 = fenetre[1]
while(1):


    to_del = []
    k = 0
    for g in gouttes:
        affichage(g)
        k+=1
    #suppression des vecteurs
    for supp in to_del[::-1]:
        gouttes.pop(supp)

    tk.update()
    newheight = tk.winfo_height()
    newwidth = tk.winfo_width()
    v*=1+(newheight*newwidth-width*height)/(width*height)
    aggfx = newwidth/width
    aggfy = newheight/height
    new_f0 *= aggfx
    new_f1 *= aggfy
    if new_f0 > new_f1:
        fenetre = [fenetre_initiale[0]*new_f0/new_f1, fenetre_initiale[1]]
    else:
        fenetre = [fenetre_initiale[0], fenetre_initiale[1]*new_f1/new_f0]
    speedmod*=1+(newheight*newwidth-width*height)/(width*height)
    long*=1+(newheight*newwidth-width*height)/(width*height)
    height = newheight
    width = newwidth
    canvas.config(width=width-2, height=height-2)
    toolbar.config(width=width)
    options.config(width=width)
    options.place(x=0, y=height-30)
    while len(gouttes)>nbgouttes:#int(width*height/250):
        torem = gouttes.pop()
        canvas.delete(torem.gui)
    while len(gouttes)<nbgouttes:#int(width*height/250):
        g = Goutte(width*rand(), height*rand())
        gouttes.append(g)
    if not no_time:
        t+=dt
    print_on_label(time_disp_label, "t = "+str(t)[:5])
    print_on_label(fenetre_label, "x[±"+str(np.round(fenetre[0], 2))+"] y[±"+str(np.round(fenetre[1]))+"]")
    time.sleep(dt)

tk.mainloop()
