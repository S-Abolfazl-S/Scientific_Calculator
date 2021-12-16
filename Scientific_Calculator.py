from tkinter import *
import math
from module.Scroll_bar import *

class Calculator:
    
    def __init__(self):
        self.mainScreen = Tk()
        self.mainScreen.title('Scientific Calculator')
        self.mainScreen.geometry("400x350")
        self.mainScreen.minsize(width=400, height=350) 
        self.mainScreen.iconphoto(False, PhotoImage(file = "icon.png"))
        
        self.main_frame = Frame(self.mainScreen)
        self.main_frame.pack(fill=BOTH,expand=1,side=LEFT) 
        # self.create_frame_history()
        # 
        # this frame for display expressions
        exp_frame = Frame(self.main_frame)
        exp_frame.pack(expand=TRUE, fill=BOTH) 
        exp_frame.config(bg='#fff')
        # total expression
        # total_expression saved expression 
        f_history_button = Frame(exp_frame,bg='#fff')
        f_history_button.pack(side=TOP,fill=X)
        self.icon = PhotoImage(file='./icon/history_icon.png') 
        self.btn_history = Button(f_history_button,image=self.icon,text='history',relief='flat',bg='#fff',font='arial 13') 
        self.btn_history['command']=self.toggle_frame
        self.btn_history.pack(side=RIGHT)
        
        self.total_expression = ''
        # total_exp display expression
        self.total_exp = Label(exp_frame,font='Verdana 20',anchor=E,bg='white',bd=0)
        self.total_exp.pack(expand=TRUE,fill=BOTH,padx=5,pady=2) 
        # current expression 
        self.current_exp = Entry(exp_frame,font='Verdana 20',text='0',justify='right',bd=0,bg='#fff')
        self.current_exp.pack(expand=TRUE,fill=BOTH,padx=5,pady=2)
        self.current_exp.bind('<Key>',self.key_press) 
        self.current_exp.focus_set() 

        
        #  this dictionary created rows, any row incloud key=name button and value=function of button
        btns = { 
            1:{
                'log10':self.btn_logarithm10, 
                'sin':self.btn_sin,
                'cos':self.btn_cos,
                'tan':self.btn_tan,
                'mod':self.press_op,
            },
            2:{
                '√':self.press_op,
                'ce':self.clear_entry,
                'c':self.clear,
                'del':self.delete,
                '÷':self.press_op, 
            },
            3:{
                'x^y':self.press_op, 
                7:self.press_num,
                8:self.press_num,
                9:self.press_num,
                '×':self.press_op,
            },
            4:{
                'pi':self.btn_pi,
                4:self.press_num,
                5:self.press_num,
                6:self.press_num,
                '-':self.press_op,
            }, 
            5:{
                'n!':self.btn_factorial,
                1:self.press_num,
                2:self.press_num,
                3:self.press_num,
                '+':self.press_op,
            },
            6:{ 
                '(':self.press_num,
                ')':self.press_op,
                0:self.press_num,
                '.':self.press_num,
                '=':self.press_eq,
            },
        } 

        # create buttons
        # for any 5 btn created 1 row inserted
        for row in btns.values():
            btn_row = Frame(self.main_frame)
            btn_row.pack(expand=TRUE, fill=BOTH) 
            for b,f in row.items(): 
                self.create_btn(btn=Button(btn_row),txt=str(b),event=f) 

    def create_btn(self,btn,txt,event):
        self.buttons = {}
        btn.config(text=txt)
        btn.config(bd=0,relief='flat',width=5,bg='white',font='Verdana 15') 
        btn.bind('<ButtonPress-1>',event)
        self.buttons[f"btn_{txt}"] = btn 
        self.buttons[f"btn_{txt}"].pack(side=LEFT, expand=TRUE, fill=BOTH)
    

    def create_frame_history(self):
        self.exp_history={
            '2^3':'2**3',
            '2÷3':'2//3',
            '(2+2)^2':'(2+2)**2',
            '(2+2)^3':'(2+2)**3',
            1:1,
            2:2,
            3:3,
            4:4,
            5:5,
            6:6,
            7:7,
            8:8

        }
        self.history_buttons={}
        self.btn_nth=0
        # parent frame used for deleted frame_history
        self.parent_frame = Frame(self.mainScreen,width=20)
        self.parent_frame.pack(fill=BOTH,expand=1,side=RIGHT)
        self.frame_history = (Scroll_bar()).create_frame(self.parent_frame)
        self.frame_history.config(bg='#fff',width=20,highlightthickness=1,highlightbackground="#eee") 
        self.frame_history['bg']='#fff' 
        for key in self.exp_history.keys():
            self.history_buttons[self.btn_nth] = Button(self.frame_history,text=key,font=('segeo',12),width=10,height=3,bg='#fff',anchor=NW,relief='groove')
            self.history_buttons[self.btn_nth].pack(fill=X)
            self.history_buttons[self.btn_nth].bind('<ButtonPress-1>',self.h_btn_handler)
            self.btn_nth+=1

    def add_history(self):
        # exp:result
        # self.total_exp:display
        # self.total_expression
        # self.current_exp

        # create btn and text add to btn - parent: frame_history 
        self.history_buttons[self.btn_nth] = Button(self.frame_history,text=input_txt[0],font=('segeo',12),width=10,height=5,bg='#fff',relief='groove')
        self.history_buttons[self.btn_nth].pack(fill=X)
        self.history_buttons[self.btn_nth].bind('<ButtonPress-1>',self.h_btn_handler)
        self.btn_nth+=1
        # text add to exp_history 
        # self.exp_history[input_txt] = ''
        pass

    def h_btn_handler(self,event): 
        # this event for click buttons in frame_history
        self.current_exp.delete(0,END) 
        self.current_exp.insert(0,self.exp_history[event.widget['text']]) 
        del self.exp_history[event.widget['text']]
        print(self.exp_history.keys())
        event.widget.pack_forget()

    toggle_frame_history = 0
    win_width=0
    win_height=0
    def toggle_frame(self): 
        if self.toggle_frame_history==1: 
            self.toggle_frame_history=0
            self.win_width = self.mainScreen.winfo_width()-200
            self.win_height = self.mainScreen.winfo_height()-50
            self.mainScreen.geometry(f'{self.win_width}x{self.win_height}') 
            self.parent_frame.destroy()
        else:
            self.toggle_frame_history=1
            self.win_width = self.mainScreen.winfo_width()+200
            self.win_height = self.mainScreen.winfo_height()+50
            self.mainScreen.geometry(f'{self.win_width}x{self.win_height}')
            self.create_frame_history()

    flag = False 
    # if pressed pi flag=true then if you press number deleted current_expression
    def btn_pi(self,event):  
        self.flag = True
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,str(math.pi)) 

    def btn_sin(self,event): 
        exp = float(self.current_exp.get())
        self.current_exp.delete(0,END)
        exp = math.sin(math.radians(exp)) if not exp in [180.0,360.0,0.0] else 0 
        self.current_exp.insert(0,exp) 

    def btn_cos(self,event): 
        exp = float(self.current_exp.get())
        self.current_exp.delete(0,END)
        exp = math.cos(math.radians(exp)) if not exp in [90.0,270.0] else 0 
        self.current_exp.insert(0,exp) 

    def btn_tan(self,event): 
        exp = float(self.current_exp.get())
        self.current_exp.delete(0,END)
        # exp = math.tan(math.radians(exp)) if not exp in [90.0,270.0] else 'invalid input' 
        match exp:
            case 270.0:exp='invalid input'
            case 90.0:exp='invalid input'
            case 360.0:exp=0
            case 180.0:exp=0
            case 0.0:exp=0
            case _ : exp = math.tan(math.radians(exp))

        self.current_exp.insert(0,exp) 
        pass

    def btn_logarithm10(self,event): 
        exp = self.current_exp.get()
        self.current_exp.delete(0,END)
        exp = math.log10(float(exp)) 
        self.current_exp.insert(0,exp) 

    def btn_factorial(self,event):
        # define: n*fact(n-1) 
        try:
            exp = self.current_exp.get()
            self.current_exp.delete(0,END)
            # check number is decimal or integer
            if '.' in exp:
                self.current_exp.insert(0,math.gamma(float(exp) + 1))
            else:
                self.current_exp.insert(0,math.factorial(int(exp)))
        except:
            self.current_exp.insert(0,exp) 

    def press_num(self,event):
        if self.flag==True:
            self.flag=False
            self.current_exp.delete(0,END)  
        exp = self.current_exp.get()
        self.current_exp.delete(0,END) 
        try: exp = exp[1:] if exp[0].isalpha() else exp 
        except: pass 
        exp = (exp + event.widget['text'])
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,exp)
        
    def press_op(self,event): 
        # total_expression + current_expression + operator
        op = event.widget['text']
        # + - , * / // % **
        match op:
            # change op ['×','÷'] to ['*','//']
            # assign new value to total expression
            case '×':self.total_expression += self.current_exp.get() + '*'
            case '÷':self.total_expression += self.current_exp.get() + '/' 
            case 'mod':self.total_expression += self.current_exp.get() + '%' 
            case 'x^y':
                self.total_expression += self.current_exp.get() + '**' 
                op = '^'
            case '√':
                self.total_expression += self.current_exp.get() + '**(1/'
                self.parantes = True 
                op = 'root'  
            case _: self.total_expression += self.current_exp.get() + op 

        exp = self.total_exp.cget('text')+(self.current_exp.get() + op) 
        self.total_exp.config(text=exp)
        self.current_exp.delete(0,END) 

    parantes = False
    def press_eq(self,event):
        # If the current expression is null, do not run the commands
        if not self.current_exp.get() == '' or not self.total_expression:
            exp = self.total_expression + self.current_exp.get() + (')' if self.parantes else '')
            self.parantes = False
            self.total_exp.config(text='')
            #
            self.total_expression = ''
            self.current_exp.delete(0,END)
            self.current_exp.insert(0,eval(exp))

    def key_press(self,event): 
        # if keyPressed is alpha then removed then number inserted
        try:
            if event.char.isalpha():  
                # limited user for write letter
                self.current_exp.delete(0,END)
            elif event.char.isdigit() and self.current_exp.get()[0].isalpha():
                exp = self.current_exp.get()[1:]
                self.current_exp.delete(0,END) 
                self.current_exp.insert(0,exp[1] + event.char) 
        except:
            pass 
    
    def clear(self,event):
        self.current_exp.delete(0,END)
        self.total_exp.config(text='')
        self.total_expression = ''

    def clear_entry(self,event):
        self.current_exp.delete(0,END)

    def delete(self,event): 
        exp = self.current_exp.get()
        self.current_exp.delete(0,END)
        self.current_exp.insert(len(exp)-1,exp[:len(exp)-1])
    
    def run(self): 
        self.mainScreen.mainloop()

calc = Calculator()
calc.run()


