from tkinter import *
import math

class Calculator:
    
    def __init__(self):
        self.mainScreen = Tk()
        self.mainScreen.title('Scientific Calculator')
        self.mainScreen.geometry("400x350")
        self.mainScreen.minsize(width=400, height=350) 
        self.mainScreen.iconbitmap(default=None)
        # icon 
        self.mainScreen.iconphoto(False, PhotoImage(file = "icon.png"))
        # 
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
        # print(event.widget['text']) 
        exp = (self.current_exp.get() + event.widget['text'])
        self.current_exp.delete(0,END)
        self.current_exp.insert(len(self.current_exp.get()),exp)
        
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
        if not self.current_exp.get() == '' or self.total_expression:
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


