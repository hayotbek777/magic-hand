import tkinter as tk
from tkinter import filedialog, messagebox
import random, math, json, time

W,H=1100,700
COLORS=['#50baff','#f1a45d','#9d7af7','#58dba1','#f37d96','#e0cf78']
class Universe:
 def __init__(self,root):
  self.root=root; root.title('PROJECT OMNIVERSE — Virtual Universe V1'); root.geometry('1100x760'); root.configure(bg='#090d1b')
  self.canvas=tk.Canvas(root,width=W,height=H-65,bg='#050917',highlightthickness=0); self.canvas.pack(fill='both',expand=True)
  bar=tk.Frame(root,bg='#121b30');bar.pack(fill='x')
  buttons=[('🌍 Planet','planet'),('🧬 Life','life'),('☄ Meteor','meteor'),('⏩ Speed','speed'),('⏸ Pause','pause'),('💾 Save','save'),('📂 Load','load'),('🗑 Reset','reset')]
  for label,action in buttons:
   tk.Button(bar,text=label,command=lambda a=action:self.action(a),bg='#253653',fg='white',activebackground='#44618d',activeforeground='white',relief='flat',padx=10,pady=12,font=('Segoe UI',10)).pack(side='left',padx=3,pady=5)
  self.info=tk.Label(bar,text='',bg='#121b30',fg='#b8d6ff',font=('Segoe UI',10));self.info.pack(side='right',padx=12)
  self.stars=[(random.random(),random.random(),random.choice([1,1,1,2]),random.choice(['#53617b','#8190af','#d5e5ff'])) for _ in range(200)]
  self.planets=[];self.selected=None;self.speed=1;self.paused=False;self.year=0;self.last=time.monotonic();self.acc=0
  self.add_planet();self.add_planet();self.loop()
 def add_planet(self):
  i=len(self.planets); self.planets.append({'name':f'Planet-{i+1}','orbit':95+i*57,'angle':random.random()*math.tau,'radius':random.randint(10,18),'color':COLORS[i%len(COLORS)],'life':False,'population':0,'tech':0,'damage':0})
  self.selected=len(self.planets)-1
 def action(self,a):
  if a=='planet':
   if len(self.planets)>=7:messagebox.showinfo('Orbit limit','V1 supports up to 7 planets.');return
   self.add_planet()
  elif a=='life':
   if self.selected is not None:
    p=self.planets[self.selected];p['life']=True;p['population']=max(p['population'],100)
  elif a=='meteor':
   if self.selected is not None:
    p=self.planets[self.selected];p['population']=int(p['population']*.55);p['damage']=40
  elif a=='speed':self.speed={1:10,10:100,100:1}[self.speed]
  elif a=='pause':self.paused=not self.paused
  elif a=='reset':self.planets=[];self.selected=None;self.year=0;self.add_planet()
  elif a=='save':
   path=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('Universe JSON','*.json')]);
   if path:
    with open(path,'w',encoding='utf8') as f:json.dump({'year':self.year,'planets':self.planets},f,indent=2)
  elif a=='load':
   path=filedialog.askopenfilename(filetypes=[('Universe JSON','*.json')]);
   if path:
    try:
     with open(path,encoding='utf8') as f:d=json.load(f)
     assert isinstance(d['planets'],list) and len(d['planets'])<=7
     self.planets=d['planets'];self.year=float(d['year']);self.selected=0 if self.planets else None
    except (ValueError,KeyError,TypeError,AssertionError, OSError) as e:messagebox.showerror('Load failed',str(e))
 def loop(self):
  now=time.monotonic();dt=min(now-self.last,.1);self.last=now
  if not self.paused:
   self.year+=dt*self.speed*2
   for p in self.planets:
    p['angle']+=dt*self.speed*.3*(95/max(p['orbit'],1))**.7
    if p['life']:
     p['population']=min(1_000_000_000,int(p['population']*(1+dt*self.speed*.012))+1)
     p['tech']=min(10,p['tech']+dt*self.speed*.008)
    p['damage']=max(0,p['damage']-dt*20)
  self.draw();self.root.after(33,self.loop)
 def draw(self):
  c=self.canvas;c.delete('all');w=max(c.winfo_width(),700);h=max(c.winfo_height(),450);cx=w*.48;cy=h*.51
  for x,y,r,col in self.stars:c.create_oval(x*w,y*h,x*w+r,y*h+r,fill=col,outline='')
  for r in (42,34,26):c.create_oval(cx-r,cy-r,cx+r,cy+r,fill=['#523009','#ac5d13','#ffca51'][[42,34,26].index(r)],outline='')
  c.create_text(cx,cy+55,text='SOL',fill='#ffd989',font=('Segoe UI',11,'bold'))
  for i,p in enumerate(self.planets):
   r=p['orbit'];c.create_oval(cx-r,cy-r,cx+r,cy+r,outline='#22344e',dash=(3,5))
   x=cx+math.cos(p['angle'])*r;y=cy+math.sin(p['angle'])*r*.72
   pr=p['radius'];c.create_oval(x-pr,y-pr,x+pr,y+pr,fill=p['color'],outline='#fff7c8' if i==self.selected else '#172d45',width=3 if i==self.selected else 1,tags=(f'planet{i}',))
   if p['life']:c.create_oval(x-3,y-3,x+3,y+3,fill='#c9ff7c',outline='')
   if p['damage']>0:c.create_oval(x-pr-5,y-pr-5,x+pr+5,y+pr+5,outline='#ff5e4b',width=2)
   c.create_text(x,y+pr+14,text=p['name'],fill='#cad9f3',font=('Segoe UI',9),tags=(f'planet{i}',))
  c.create_text(18,16,anchor='nw',text='OMNIVERSE  /  UNIVERSE SIMULATOR',fill='#a7d7ff',font=('Segoe UI',16,'bold'))
  c.create_text(18,48,anchor='nw',text='Click a planet to select it. Add life, send a meteor, or speed up time.',fill='#7d94b9',font=('Segoe UI',10))
  if self.selected is not None and self.selected<len(self.planets):
   p=self.planets[self.selected];lines=[p['name'],'Life: '+('YES' if p['life'] else 'NO'),f"Population: {p['population']:,}",f"Civilization: Level {int(p['tech'])}/10",'Meteor impact: '+('RECENT' if p['damage'] else 'NONE')]
   xx=w-250;c.create_rectangle(xx-15,20,w-15,175,fill='#101c32',outline='#2a4262')
   for j,line in enumerate(lines):c.create_text(xx,35+j*27,anchor='nw',text=line,fill='#e2edff' if j==0 else '#a3bbdd',font=('Segoe UI',12 if j==0 else 10,'bold' if j==0 else 'normal'))
  self.info.config(text=f'Year {int(self.year):,}   |   {len(self.planets)} planets   |   {self.speed}x'+('   PAUSED' if self.paused else ''))
  c.bind('<Button-1>',self.click)
 def click(self,event):
  w=max(self.canvas.winfo_width(),700);h=max(self.canvas.winfo_height(),450);cx=w*.48;cy=h*.51
  for i,p in enumerate(self.planets):
   x=cx+math.cos(p['angle'])*p['orbit'];y=cy+math.sin(p['angle'])*p['orbit']*.72
   if math.hypot(event.x-x,event.y-y)<p['radius']+15:self.selected=i;break
if __name__=='__main__':
 root=tk.Tk();Universe(root);root.mainloop()
