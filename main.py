from PIL import Image, ImageTk
import time
import tkinter
import numpy as np
import random as rd

# Création de la grille
def createGrid(dim,blockSize):
    for i in range (dim[1]+1):
        canvas.create_line(1,i*blockSize+1,blockSize*dim[0]+1,i*blockSize+1,width=1,fill="grey")
    for i in range (dim[0]+1):
        canvas.create_line(i*blockSize+1,1,i*blockSize+1,blockSize*dim[1]+1,width=1,fill="grey")

# Fin
def loose() :
    global end
    end = 1
    print("Perdu...")

# Déplacements droite - gauche
def right(event) :
    global N
    global pos
    n = np.zeros(dim,dtype=int)
    for x in range (dim[0]) :
        for y in range (dim[1]) :
            if N[x][y]!=0 :
                if x<dim[0]-1 and M[x+1][y]==0 : n[x+1][y]=N[x][y]
                else : return
    pos = (pos[0]+1,pos[1])
    N = n.copy()
    refresh()
    tk.update()

def left(event) :
    global N
    global pos
    n = np.zeros(dim,dtype=int)
    for x in range (dim[0]) :
        for y in range (dim[1]) :
            if N[x][y]!=0 :
                if x>0 and M[x-1][y]==0: n[x-1][y]=N[x][y]
                else : return
    pos = (pos[0]-1,pos[1])
    N = n.copy()
    refresh()
    tk.update()

# Tourne la pièce dans le sens horaire
def turn(event):
    if end!=1 :
        global N
        global block
        n = np.zeros(dim,dtype=int)
        for x in range (dim[0]) :
            for y in range (dim[1]) :
                if N[x][y]!=0 :
                    X,Y = pos[0]+(y-pos[1]),pos[1]-(x-pos[0])
                    if X>=0 and X<dim[0] and Y>=0 and Y<dim[1] and M[X][Y]==0 :
                        n[X][Y] = block
                    else :
                        return
        N = n.copy()
        refresh()
        tk.update()

# Fait descendre la pièce d'une case vers le bas
def down() :
    global N
    global pos
    pos = (pos[0],pos[1]+1)
    n = np.zeros(dim,dtype=int)
    for x in range (dim[0]) :
        for y in range (dim[1]-1) :
            if N[x][y]!=0 :
                n[x][y+1] = N[x][y]
    N = np.zeros(dim,dtype=int)
    N = n.copy()
    refresh()
    tk.update()

# Accélère la pièce vers le bas
def dash(event) :
    global isDashing
    if isDashing==False :
        isDashing = True
        while isLand()==False :
            down()
        tk.update()
        isDashing = False

# Supprime les lignes complètes
def line() :
    global N
    N = np.zeros(dim,dtype=int)
    refresh()
    tk.update()
    global M
    Lines = []
    for y in range (dim[1]) :
        line = 1
        for x in range (dim[0]) :
            if M[x][y]==0 : line = 0
        if line==1 : Lines.append(y)
    # Animation de disparition des lignes
    for L in Lines :
        for i in range (3) :
            for x in range (dim[0]) :
                M[x][L] = 8
            refresh()
            tk.update()
            time.sleep(0.1)
            for x in range (dim[0]) :
                M[x][L] = 0
            refresh()
            tk.update()
            time.sleep(0.1)
        for y in range (0,L-1) :
            for x in range(dim[0]) :
                M[x][L-y] = M[x][L-y-1]
                M[x][L-y-1] = 0

# Vérifie si la pièce a atteri
def isLand() :
    global N
    for x in range (dim[0]) :
        for y in range (dim[1]) :
            if N[x][y]!=0 and (y==dim[1]-1 or M[x][y+1]!=0 ) :
                for X in range (dim[0]) :
                    for Y in range (dim[1]) :
                        if N[X][Y]!=0 :
                            M[X][Y] = N[X][Y]
                return True
    return False

# Rafraichit l'affichage
def refresh() :
    for o in Objects : canvas.delete(o)
    for x in range (dim[0]) :
        for y in range (dim[1]) :
            if M[x][y]!=0 :
                Objects.append(canvas.create_image(x*blockSize+1,y*blockSize+1,image=Colors[M[x][y]-1],anchor='nw'))
            if N[x][y]!=0 :
                Objects.append(canvas.create_image(x*blockSize+1,y*blockSize+1,image=Colors[N[x][y]-1],anchor='nw'))

# Création d'un nouveau bloc
def new() :
    global N
    global block
    global pos
    N = np.zeros(dim,dtype=int)
    block = rd.randint(1,7)
    pos = (4,0)
    for i in range (4) :
        x, y = Blocks[block-1][i][0]+4, Blocks[block-1][i][1]+1
        if M[x][y]==0 : N[x][y] = block
        else :
            loose()
            return

# Gameloop
def gameLoop() :
    tk.update()
    down()
    refresh()

# Création du jeu
blockSize = 30
dim = (10,20)
fen = (dim[0]*blockSize,dim[1]*blockSize)
tk = tkinter.Tk()
tk.title("Tetris")
canvas = tkinter.Canvas(tk,width=fen[0],height=fen[1],bg='black')
createGrid(dim,blockSize)
canvas.pack()
M = np.zeros(dim,dtype=int)
N = np.zeros(dim,dtype=int)
Blocks = [[(0,-1),(0,0),(1,0),(2,0)],[(1,0),(0,0),(0,-1),(-1,-1)],[(-1,0),(0,0),(1,0),(2,0)],
        [(-1,0),(0,0),(1,0),(1,-1)],[(-1,0),(0,0),(1,0),(0,-1)],[(0,0),(1,0),(0,-1),(1,-1)],
        [(-1,0),(0,0),(0,-1),(1,-1)]]
block = 0
end = 0
Objects = []
pos = (0,0)
isDashing = False
delay = 0.5

# Importation des images
Colors = [ImageTk.PhotoImage(Image.open("assets/DarkBlue.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/Green.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/LightBlue.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/Orange.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/Pink.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/Yellow.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/Red.png").resize((blockSize,blockSize))),
          ImageTk.PhotoImage(Image.open("assets/White.png").resize((blockSize,blockSize)))
          ]

# Bind des touches
canvas.bind_all("<Up>",turn)
canvas.bind_all("<Right>",right)
canvas.bind_all("<Left>",left)
canvas.bind_all("<space>",dash)
canvas.bind_all("<Down>",dash)

# Boucle principale
while end==0 :
    new()
    if end==0 :
        while isLand()==False :
            if isLand()==False :
                gameLoop()
            delay -= 0.001
            t = time.time()
            while time.time()-t<delay :
                tk.update()
        line()