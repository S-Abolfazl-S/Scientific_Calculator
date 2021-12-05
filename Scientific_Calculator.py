from tkinter import *
import math
from tkinter import font

class Calculator:
    
    def __init__(self):
        self.mainScreen = Tk()
        self.mainScreen.title('Scientific Calculator')
        self.mainScreen.geometry("650x400")
        # this frame for display expressions
        disp_frame = Frame(self.mainScreen)
        disp_frame.pack(expand=TRUE, fill=BOTH) 
        disp_frame.config(bg='#fff')
        # total expression
        # total_expression saved expression 
        self.total_expression = ''
        # total_exp display expression
        self.total_exp = Label(disp_frame,font='Verdana 20',anchor=E,bg='white',bd=0)
        self.total_exp.pack(expand=TRUE,fill=BOTH,padx=5,pady=2) 
        # current expression 
        self.current_exp = Entry(disp_frame,font='Verdana 20',text='0',justify='right',bd=0,bg='#fff')
        self.current_exp.pack(expand=TRUE,fill=BOTH,padx=5,pady=2)
        self.current_exp.bind('<Key>',self.key_press) 
        self.current_exp.focus_set() 

        #  this dictionary created rows, any row incloud key=name button and value=function 
        btns = {
            1:{
                'round':None,
                'log':None,
                'sin':None,
                'cos':None,
                'tan':None,
            },
            2:{
                'CE':self.clear_entry,
                'C':self.clear,
                'DEL':self.delete,
                'Mod':None,
                '÷':self.press_op,
            },
            3:{
                'PI':self.btn_pi,
                7:self.press_num,
                8:self.press_num,
                9:self.press_num,
                '×':self.press_op,
            },
            4:{
                'E':self.btn_e,
                4:self.press_num,
                5:self.press_num,
                6:self.press_num,
                '-':self.press_op,
            },
            5:{
                'n!':None,
                1:self.press_num,
                2:self.press_num,
                3:self.press_num,
                '+':self.press_op,
            },
            6:{
                'x^y':None,
                '√':None,
                0:self.press_num,
                '.':None,
                '=':self.press_eq,
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
    
    # if pressed pi or E flag=true then if you press number deleted current_expression
    flag = False
    def btn_e(self,event):  
        self.flag = True
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,str(math.e))

    def btn_pi(self,event):  
        self.flag = True
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,str(math.pi))

    def btn_power(self,event):
        if len(self.current_exp.get())>0:
            result= math.power(int(self.current_exp.get()))
        pass

    def press_num(self,event):
        if self.flag==True:
            self.flag=False
            self.current_exp.delete(0,END)
        # print(event.widget['text']) 
        exp = (self.current_exp.get() + event.widget['text'])
        self.current_exp.delete(0,END)
        self.current_exp.insert(len(self.current_exp.get()),exp)
        
    def press_op(self,event): 
        # total_expression + current_expression + operator
        op = event.widget['text']
        exp = self.total_exp.cget('text')+(self.current_exp.get() + op) 
        self.total_exp.config(text=exp)
        match op:
            # change op ['×','÷'] to ['*','//']
            # assign new value to total expression
            case '×':self.total_expression += self.current_exp.get() + '*'
            case '÷':self.total_expression += self.current_exp.get() + '//' 
            case _: self.total_expression += self.current_exp.get() + op 
        self.current_exp.delete(0,END)
        

    def press_eq(self,event):
        exp = self.total_expression + self.current_exp.get()
        
        self.total_exp.config(text='')
        #
        self.total_expression = ''
        self.current_exp.delete(0,END)
        self.current_exp.insert(0,eval(exp))

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


