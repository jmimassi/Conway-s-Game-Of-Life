import json
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial 
import numpy as np


BLACK = (0, 0, 0, 1) 
GREEN = (0.1, 0.5, 0, 1)
RED = (1,0.2,0,1)
GREY = (0.3,0.3,1,0.7)
BLUE =(0.2,0.6,1,1)


class MyApp(App):
    def build(self):
        box=BoxLayout(orientation='vertical')
        self.title="Game Of Life"
        self.grille = Grille()
        layout = GridLayout(cols=40)
        self.boutons = [] 
        
        self.on_pause = True
        self.vitesse = 0.2
        Clock.schedule_interval(self.step, self.vitesse)
        
        for i in range(30):
            self.boutons.append([])
            
            for j in range(40):
                self.boutons[i].append(Button(background_normal="", background_color=BLACK, size_hint=(0.1, 0.1)))                                                
                
                if(self.grille.getCell(i, j) == 1):
                    self.boutons[i][j].background_color = GREEN
                layout.add_widget(self.boutons[i][j])
                self.boutons[i][j].bind(on_press=partial(self.buttonPressed, i, j))

        linebtn = BoxLayout(orientation='horizontal',size_hint_y = 0.15)  
        
        self.pausebtn = Button(text='Play',background_color=GREEN,font_size=35) 
        self.pausebtn.bind(on_press=self.pause)
        
        randombtn = Button(text='Random',font_size=30,background_color=BLUE)
        randombtn.bind(on_press=self.randomGrid)
        
        resetbtn = Button(text='Reset',font_size=30,background_color=BLUE)
        resetbtn.bind(on_press=self.resetGrid)
        
        impjson = Button(text='Import',font_size=30,background_color=BLUE)
        impjson.bind(on_press=self.importJson)
        
        exprtbtn = Button(text= 'Export',font_size=30,background_color=BLUE)
        exprtbtn.bind(on_press=self.exportJson)
        
        leavebtn = Button(text='Leave',background_color=GREY,font_size=35)
        leavebtn.bind(on_press=self.quit)
        
        linebtn.add_widget(self.pausebtn)
        linebtn.add_widget(randombtn)
        linebtn.add_widget(resetbtn)
        linebtn.add_widget(impjson)
        linebtn.add_widget(exprtbtn)
        linebtn.add_widget(leavebtn)
        box.add_widget(linebtn)
        box.add_widget(layout)
        
        return box

    Config.set('graphics','width','1200')
    Config.set('graphics','height','1000')

    def step(self,source):
        if(not self.on_pause):
            self.grille.stepCalculMatrix()
            self.updateGrille()

    def updateGrille(self):
        for i in range(30):
            for j in range(40):
                if(self.grille.getCell(i, j) == 1):
                    self.boutons[i][j].background_color = GREEN
                else:
                    self.boutons[i][j].background_color = BLACK

    def pause(self, source):
        self.on_pause = not(self.on_pause)
        if self.on_pause:
            self.pausebtn.text = "Play"
            self.pausebtn.background_color=GREEN
        else:
            self.pausebtn.text = "Pause"
            self.pausebtn.background_color=RED

    def randomGrid(self, source):
        self.grille = Grille(randomize=True)
        self.updateGrille()
        
    def resetGrid(self, source):
        self.grille = Grille()
        self.updateGrille()

    def quit(self, source):
        quit()

    def buttonPressed(self, i, j, source):  
        self.grille.changeCell(i, j)
        if(self.grille.getCell(i, j) == 1):
            source.background_color = GREEN
        else:
            source.background_color = BLACK

    def exportJson(self, source):
        a = self.grille.grille
        print(type(a))
        list_matrix = a.tolist()
        
        file_path ="save.json"     #save.json de base
        f= open(file_path, "w")
        json.dump(list_matrix, f, indent=4)
        
        for coords, value in np.ndenumerate(self):
            if value== 1: json.dump(coords,f)
        
        f.close()
    
    def importJson(self, source):
        file_path="plus.json"       #plus.json de base
        f = open(file_path,"r")
        b= f.read() 
        
        matrice = json.loads(b) 
        self.grille.grille = np.asarray(matrice) 
    
        f.close()
        self.updateGrille()


class Grille:

    def __init__(self, h=30, l=40, randomize=False):
        self.H = h
        self.L = l
        if(randomize):
            self.grille = np.random.randint(size=(self.H, self.L), low=2)
        else:
            self.grille = np.random.randint(size=(self.H, self.L), low=1)

    def stepCalculMatrix(self):
        new_grille = np.copy(self.grille)
        for i in range(self.H):
            for j in range(self.L):
                total = self.grille[i, (j-1) % self.L] + self.grille[i, (j+1) % self.L] + self.grille[(i-1) % self.H, j] + self.grille[(i+1) % self.H, j] + self.grille[(i-1) % self.H, (
                    j-1) % self.L] + self.grille[(i-1) % self.H, (j+1) % self.L] + self.grille[(i+1) % self.H, (j-1) % self.L] + self.grille[(i+1) % self.H, (j+1) % self.L]
                if self.grille[i, j] == 1:  
                    if total < 2 or total > 3:
                        new_grille[i, j] = 0
                else:
                    if total == 3:
                        new_grille[i, j] = 1
        self.grille = new_grille
        print(type(self.grille))  

    def changeCell(self, i, j): 
        self.grille[i, j] = (self.grille[i,j]+1) % 2  
                                                       
    def getCell(self, i, j):
        return self.grille[i, j]


MyApp().run()