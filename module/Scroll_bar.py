from math import *
from tkinter import * 
''' how to use:
frame = (Scroll_bar()).create_frame(self.window) 
new_root no needed to pack for display, you must only added widget's
'''
class Scroll_bar: 
    ''' 
        create_frame get root, the root is anything: window/Frame
        self target the root
        this method return a frame for add widgets: Button/Label
    ''' 
    def __init__(self,state_width=False,state_height=False): 
        self.max_width_flag = state_width
        self.max_height_flag = state_height
        
    def create_frame(self,root):  
        self.root = root
        # Create A Canvas
        # Canvas width = 0 to be resized less than 400
        self.my_canvas = Canvas(root,width=250,height=0,bg='#fff') 
        # Add A Scrollbar To The Canvas
        self.v_scrollbar = Scrollbar(root,orient='vertical',command=self.my_canvas.yview) 
        self.h_scrollbar = Scrollbar(root,orient='horizontal',command=self.my_canvas.xview) 
        # config position
        self.v_scrollbar.pack(side=RIGHT,fill=Y)
        self.h_scrollbar.pack(side=BOTTOM,fill=X)
        self.my_canvas.pack(side=LEFT,fill=BOTH,expand=1) 
        # h_scrollbar.config(command=self.my_canvas.xview)
        # Configure The Canvas 
        self.my_canvas['yscrollcommand'] = self.v_scrollbar.set 
        self.my_canvas['xscrollcommand'] = self.h_scrollbar.set
        self.my_canvas.bind('<Configure>',self.on_canvas_configure) 
        self.my_canvas.bind_all("<MouseWheel>",self.on_yview_scroll)
        self.my_canvas.bind_all("<Shift-MouseWheel>",self.on_xview_scroll) 
        # Create ANOTHER Frame  INSIDE The Canvas
        new_root = Frame(self.my_canvas) 
        # Add that New frame to a window in the canvas
        self.frame_id = self.my_canvas.create_window((0,0),window=new_root,anchor="nw",width=1300,height=3000) 
        
        return new_root

    def on_canvas_configure(self, event): 
        # print(f'{event.width} {event.height}') 
        # canvas resize and frame resize 
        # when frame dimensions change pass the area to the canvas scroll region 
        self.my_canvas['scrollregion'] = self.my_canvas.bbox("all")
        # makes frame width match canvas width
        self.my_canvas.itemconfig(self.frame_id) 

    def on_yview_scroll(self,event): 
        try:
            self.my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass
    def on_xview_scroll(self,event):  
        try:
            self.my_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass
