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
    def create_frame(self,root): 
        # Create A Canvas
        # Canvas width = 0 to be resized less than 400
        self.my_canvas = Canvas(root,width=0,height=0,bg='#fff') 
        self.my_canvas.pack(side=LEFT,fill=BOTH,expand=1) 
        # Add A Scrollbar To The Canvas
        v_scrollbar = Scrollbar(root,orient='vertical',command=self.my_canvas.yview) 
        v_scrollbar.pack(side=RIGHT,fill=Y)
        h_scrollbar = Scrollbar(self.my_canvas,orient='horizontal',command=self.my_canvas.xview) 
        h_scrollbar.pack(side=BOTTOM,fill=X)
        # h_scrollbar.config(command=self.my_canvas.xview)
        # Configure The Canvas 
        self.my_canvas.configure(yscrollcommand=v_scrollbar.set) 
        self.my_canvas.configure(xscrollcommand=h_scrollbar.set) 
        self.my_canvas.bind('<Configure>',self.on_canvas_configure)
        self.my_canvas.bind_all("<MouseWheel>", lambda event: self.my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")) 
        self.my_canvas.bind_all("<Shift-MouseWheel>", lambda event: self.my_canvas.xview_scroll(int(-1*(event.delta/120)), "units")) 
        # Create ANOTHER Frame  INSIDE The Canvas
        new_root = Frame(self.my_canvas) 
        # Add that New frame to a window in the canvas
        self.frame_id = self.my_canvas.create_window((0,0),window=new_root,anchor="nw") 
        
        return new_root

    def on_canvas_configure(self, event):
        # canvas resize and frame resize 
        # when frame dimensions change pass the area to the canvas scroll region
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        # makes frame width match canvas width
        self.my_canvas.itemconfig(self.frame_id, width=event.width)