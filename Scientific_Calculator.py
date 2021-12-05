from tkinter import *
import math
from tkinter import font

class Calculator:
    
    def __init__(self):
        self.mainScreen = Tk()
        self.mainScreen.title('Scientific Calculator')
        self.mainScreen.geometry("650x400")
        disp_frame = Frame(self.mainScreen)
        disp_frame.pack(expand=TRUE, fill=BOTH) 
        
        # total expression
        self.total_expression = ''
        self.total_exp = Label(disp_frame,font='Verdana 20',anchor=E,bg='white',bd=0)
        self.total_exp.pack(expand=TRUE,fill=BOTH)
        
        # current expression 
        self.current_exp = Entry(disp_frame,font='Verdana 20',text='0',justify='right',bd=0)
        self.current_exp.pack(expand=TRUE,fill=BOTH)
        self.current_exp.bind('<Key>',self.key_press) 
        self.current_exp.focus_set()

        # btns = [
        #     ['round','log','sin','cos','tan'],
        #     ['CE','C','del','mod','÷'],
        #     ['PI',7,8,9,'×'],
        #     ['E',4,5,6,'-'], 
        #     ['n!',1,2,3,'+'], 
        #     ['x^y','√',0,'.','='], 
        # ] 
        btns = {
            1:{
                'round':None,
                'log':None,
                'sin':None,
                'cos':None,
                'tan':None,
            },
            2:{
                'CE':None,
                'C':self.clear,
                'DEL':None,
                'Mod':None,
                '÷':None,
            },
            3:{
                'PI':self.btn_pi,
                7:None,
                8:None,
                9:None,
                '×':None,
            },
            4:{
                'E':self.btn_e,
                4:None,
                5:None,
                6:None,
                '-':None,
            },
            5:{
                'n!':None,
                1:None,
                2:None,
                3:None,
                '+':None,
            },
            6:{
                'x^y':None,
                '√':None,
                0:None,
                '.':None,
                '=':None,
            },
        } 

        for row in btns.values():
            btn_row = Frame(self.mainScreen)
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

    def btn_e(self,event):  
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,str(math.e))

    def btn_pi(self,event):  
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,str(math.pi))

    def press_num(self,event): 
        # print(event.widget['text']) 
        exp = (self.current_exp.get() + event.widget['text'])
        self.current_exp.delete(0,END)
        self.current_exp.insert(len(self.current_exp.get()),exp)
        
    def press_op(self,event): 
        # print(event.widget['text'])
        # print(self.current_exp.get())
        self.total_expression += self.current_exp.get()+event.widget['text']
        self.total_exp.config(text=self.total_expression)
        self.current_exp.delete(0,END)

    def key_press(self,event): 
        # if keyPressed is alpha then removed then number inserted
        try:
            if event.char.isalpha():  
                self.current_exp.delete(0,END)
            elif event.char.isdigit() and self.current_exp.get()[0].isalpha():
                exp = self.current_exp.get()[1:]
                self.current_exp.delete(0,1)
                self.current_exp.insert(len(exp),exp[1] +event.char) 
        except:
            pass 
    
    def clear(self,event):
        self.current_exp.delete(0,END)
        self.total_exp.config(text='')

    def clear_entry(self,event):
        self.current_exp.delete(0,END)

    def delete(self,event):
        pass
    
    def run(self): 
        self.mainScreen.mainloop()

calc = Calculator()
calc.run()


