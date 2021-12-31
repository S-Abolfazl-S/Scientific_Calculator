''' 
    Scientific Calculator
    Programmer: S-Abolfazl-S
''' 
from tkinter import *
import math
from math import *
from module.Scroll_bar import Scroll_bar
from module.data_base import DataBase
from datetime import datetime

class Calculator:

    def __init__(self):
        self.mainScreen = Tk()
        self.mainScreen.title('Scientific Calculator')
        self.mainScreen.geometry("400x400")
        self.mainScreen.minsize(width=400, height=400)
        self.mainScreen.iconphoto(False, PhotoImage(file=r"icon\main_icon.png"))
        self.main_frame = Frame(self.mainScreen)
        self.main_frame.pack(fill=BOTH, expand=1, side=LEFT)
        # display_frame for display total_exp and current_exp , history button
        display_frame = Frame(self.main_frame)
        display_frame.pack(expand=TRUE, fill=BOTH)
        display_frame.config(bg='#fff') 
        # connect to history database
        self.history_db = DataBase()
        # add button for display history
        f_history_button = Frame(display_frame, bg='#fff')
        f_history_button.pack(side=TOP, fill=X)
        self.icon = PhotoImage(file=r'.\icon\history_icon.png')
        self.btn_history = Button(f_history_button, image=self.icon, text='history', relief='flat', bg='#fff', font='arial 13')
        self.btn_history['command'] = self.toggle_history
        self.btn_history.pack(side=RIGHT) 
        # total expression
        self.total_exp = Label(display_frame, font='Verdana 20', anchor=E, bg='white', bd=0)
        self.total_exp.pack(expand=TRUE, fill=BOTH, padx=5, pady=2)
        # current expression
        self.current_exp = Entry(display_frame, font='Verdana 20', text='0', justify='right', bd=0, bg='#fff')
        self.current_exp.pack(expand=TRUE, fill=BOTH, padx=5, pady=2)
        self.current_exp.bind('<Key>', self.key_press)
        self.current_exp.focus_set()

        #  this dictionary created rows, any row incloud key=name button and value=function of button

        collection_btns = {
            1: {
                'log': self.on_click_action,
                'sin': self.on_click_action,
                'cos': self.on_click_action,
                'tan': self.on_click_action,
                'mod': self.on_click_action,
            },
            2: {
                '√': self.on_click_action,
                'CE': self.clear_entry,
                'C': self.clear,
                'Del': self.delete,
                '÷': self.on_click_action,
            },
            3: {
                'x^y': self.on_click_action,
                7: self.on_click_number,
                8: self.on_click_number,
                9: self.on_click_number,
                '×': self.on_click_action,
            },
            4: {
                'pi': self.btn_pi,
                4: self.on_click_number,
                5: self.on_click_number,
                6: self.on_click_number,
                '-': self.on_click_action,
            },
            5: {
                'n!': self.on_click_action,
                1: self.on_click_number,
                2: self.on_click_number,
                3: self.on_click_number,
                '+': self.on_click_action,
            },
            6: {
                '(': self.on_click_action,
                ')': self.on_click_action,
                0: self.on_click_number,
                '.': self.on_click_number,
                '=': self.press_eq,
            },
        }
        # Object's of Button in this dictionary saved
        self.obj_buttons = {}
        # create buttons
        # for any 5 btn , created a row
        for row in collection_btns.values():
            btn_row = Frame(self.main_frame)
            btn_row.pack(expand=TRUE, fill=BOTH)
            for btn_name, func in row.items():
                self.create_btn(btn=Button(btn_row), txt=str(btn_name), event=func)

    def create_btn(self, btn, txt, event):
        btn.config(text=txt, bd=0, relief='groove', width=5, bg='#fff', font=('verdana', 15))
        btn.bind('<ButtonPress-1>', event)
        btn.bind('<Enter>', self.on_Enter_Mouse)
        btn.bind('<Leave>', self.on_Leave_Mouse)
        self.obj_buttons[f"btn_{txt}"] = btn
        self.obj_buttons[f"btn_{txt}"].pack(side=LEFT, expand=TRUE, fill=BOTH) 

    def create_frame_history(self):
        # parent frame used for deleted frame_history
        self.parent_history = Frame(self.mainScreen)
        self.parent_history.pack(side=RIGHT, fill=BOTH, expand=1) 
        self.frame_history = (Scroll_bar()).create_frame(self.parent_history)
        self.frame_history.config(bg='#fff', width=20) 
        
        exp_list = self.history_db.get_all_exppression()
        for item in exp_list:
            self.add_history(item[0], item[1],item[2])

    def add_history(self, input_exp, input_result,dateAndTime):
        _frame = Frame(self.frame_history, bg='#000', bd=0, highlightthickness=0)
        _frame.pack(fill=X)
        # add Date & Time
        _dateTime = Text(_frame, state=NORMAL, wrap=WORD, width=0, height=0, font='verdana 15')
        _dateTime.insert(INSERT, f'{dateAndTime}')
        _dateTime['state'] = 'disabled'
        _dateTime['bg'] = '#ff0'
        _dateTime['fg'] = '#000'
        _dateTime.pack(side=TOP, fill=BOTH, expand=1)
        _dateTime.bind('<ButtonPress-1>', self.on_click_frame_in_history)
        # added exp
        _exp = Text(_frame, state=NORMAL, wrap=WORD, width=0, height=2, font='verdana 15')
        _exp.insert(INSERT, f'{input_exp}')
        _exp['state'] = 'disabled'
        _exp.pack(side=TOP, fill=BOTH, expand=1)
        # add result
        _result = Text(_frame, state=NORMAL, wrap=WORD, width=0, height=2, font='verdana 15')
        _result.insert(INSERT, f'{input_result}')
        _result['state'] = 'disabled'
        _result.pack(side=BOTTOM, fill=BOTH, expand=1,pady=1) 

    def on_click_frame_in_history(self, event):
        # if you clicked the frame this event runing and expression added to total_exp and frame deleted
        try:
            parent = event.widget.nametowidget(event.widget.winfo_parent()) 
            self.current_exp.delete(0, END)
            _dateAndTime = parent.winfo_children()[0].get(0.0, END).strip()
            _exp = parent.winfo_children()[1].get(0.0, END).strip()
            _result = parent.winfo_children()[2].get(0.0, END).strip()
            self.total_exp['text'] = _exp
            self.history_db.delete_exppression(_exp,_result,_dateAndTime)
            parent.destroy()
            # if clicked on last exp, closed history
            exp_list = self.history_db.get_all_exppression()
            if len(exp_list) == 0:
                self.toggle_history()
        except:
            pass

    flag_history = 0

    def toggle_history(self):
        exp_list = self.history_db.get_all_exppression()
        if len(exp_list) > 0 or self.flag_history == 1:
            _width = self.mainScreen.winfo_width()
            _height = self.mainScreen.winfo_height()
            if self.flag_history == 1:
                self.flag_history = 0
                _width -= 200
                self.mainScreen.geometry(f'{_width}x{_height}')
                self.mainScreen.minsize(width=400, height=400)
                self.parent_history.destroy()
            else:
                _width += 200
                self.flag_history = 1
                self.mainScreen.geometry(f'{_width}x{_height}')
                self.mainScreen.minsize(width=600, height=400)
                self.create_frame_history()

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    num_flag = False
    # if pressed pi flag=true then if you press number deleted current_expression
    def btn_pi(self, event):
        self.num_flag = True
        self.current_exp.delete(0, END)
        self.current_exp.insert(0, str(math.pi))

    def _sin(self, num):
        return math.sin(math.radians(num)) if not num in [180.0, 360.0, 0.0] else 0

    def _cos(self, num):
        return math.cos(math.radians(num)) if not num in [90.0, 270.0] else 0

    def _tan(self, num):
        _num = {
            270.0: 'invalid input',
            90.0: 'invalid input',
            360.0: 0,
            180.0: 0,
            0.0: 0
        }
        return math.tan(math.radians(num)) if num not in _num else _num[num]

    def _fact(self, num):
        # define: n*fact(n-1)
        # check number is decimal or integer
        try:
            return math.gamma(float(num) + 1) if isinstance(num, float) else math.factorial(int(num))
        except:
            pass

    def on_click_number(self, event):
        if self.num_flag == True:
            self.num_flag = False
            self.current_exp.delete(0, END)
        exp = self.current_exp.get()
        self.current_exp.delete(0, END)
        try:
            exp = exp[1:] if exp[0].isalpha() else exp
        except:
            pass
        exp = (exp + event.widget['text'])
        self.current_exp.delete(0, END)
        self.current_exp.insert(0, exp)

    def on_Enter_Mouse(self, event):
        event.widget['bg'] = "#%02x%02x%02x" % (235, 235, 235)

    def on_Leave_Mouse(self, event):
        event.widget['bg'] = "#%02x%02x%02x" % (255, 255, 255)

    def exp_converter(self, exp: str):
        for i in [['×', '*'], ['÷', '/'], ['^', '**'], ['root(', '**(1/'], ['mod', '%'], ['sin(', 'self._sin('], ['cos(', 'self._cos('], ['tan(', 'self._tan('], ['fact(', 'self._fact(']]:
            if i[0] in exp:
                exp = exp.replace(i[0], i[1])
        return exp

    # action modes:
    # 2: sin(),cos(),tan(),fact(),log() : before action is operator
    # 1: root  : before action is digit
    action_mode = 0
    # old_action for change action
    old_action = ''

    def on_click_action(self, event):
        # total_exp + current_exp + action      or      total_exp + action + current_exp
        # action is operator / function
        
        # get variables
        input_action    = event.widget['text'].strip()
        current_exp     = self.current_exp.get().strip()
        total_exp       = self.total_exp.cget('text').strip()
        old_action_mode = self.action_mode  

        action_dict = {
            # action : [ action , seperator_numbers, parantes_count, action_mode],
            'log':  ['log(', ',', 1, 2],
            'sin':  ['sin(', '', 1, 2],
            'cos':  ['cos(', '', 1, 2],
            'tan':  ['tan(', '', 1, 2],
            'n!':   ['fact(', '', 1, 2],
            '√':    ['root(', '', 1, 1],
            'x^y':  ['^', '', 0, 0],
            '(':    ['(', '', 1, 0],
            ')':    [')', '', -1, 0],
        }

        # get values of action_dict
        action_list = action_dict.get(input_action)
            
        # added function to before old_function
        try: 
            if old_action_mode > 0 and action_list[3] > 0:
                total_exp = total_exp[::-1]
                self.old_action = self.old_action[::-1]
                
                index = total_exp.index(self.old_action)+len(self.old_action)  # len old exp
                current_exp = total_exp[:index]  # get old exp
                total_exp = total_exp[index:]  # cut

                total_exp = total_exp[::-1]
                current_exp = current_exp[::-1]
                self.old_action = self.old_action[::-1]
                if not self.hasNumbers(current_exp):
                    current_exp+='0'
        except: pass

        # parantes control for any function ex: log() , 25root(2)...
        if self.action_mode > 0: 
            try:
                if total_exp[-1] == '(' or current_exp == '' and total_exp[-1] == ',':
                    current_exp += '0' 
            except: pass
            current_exp += ')'
            self.parantes_counter = self.parantes_counter-1 if self.parantes_counter > 0 else 0
            self.action_mode = 0 
        

        # get values of action_list
        if action_list != None:
            input_action = action_list[0]
            current_exp = current_exp if self.hasNumbers(current_exp) or self.hasNumbers(total_exp) else ('0' if input_action not in ['(',')'] else '')
            # add zero for log(0, if before is (...)= (...)×log(0,
            if len(total_exp)>0:
                current_exp += '0' if current_exp == '' and total_exp[-1] == ')' and input_action == 'log(' else ''
            current_exp += action_list[1]
            self.parantes_counter = self.parantes_counter + action_list[2]
            self.action_mode = action_list[3] 

            # parantes control
            if self.parantes_counter < 0:
                self.parantes_counter = 0 
                input_action = '' if input_action == ')' else input_action 

        # change operator
        if self.old_action in ['+','-','×','÷','mod','^'] and current_exp == '' and input_action not in ['(', ')']:
            if input_action in ['+', '-', '×', '÷', 'mod', '^'] or action_list[3] == 1:
                    total_exp = total_exp[:len(total_exp)-len(self.old_action)]

        # zero and mull added 
        operators = ['+', '-', '×', '÷', 'mod', '^', '(']
        # add zero before operator: zero + op
        if total_exp == '' and current_exp == '' and input_action in operators[:len(operators)-1]:
            current_exp+='0'
        # add zero after parantes and before operator:  ( + 0 + op
        if len(total_exp) > 0 and current_exp == '' and total_exp[-1] == '(' and input_action in operators[:len(operators)-1]:
            current_exp+= '0'
        # ( + 0 + ) or (0 op 0) 
        if len(total_exp)>0: 
            if (total_exp[-1] in operators or total_exp[-1:-4:-1][::-1] == 'mod') and input_action == ')' and current_exp == '':
                current_exp+='0' 
        # add mull before parantes: (--)×( or func(--)×( or...
        if (old_action_mode > 0 or current_exp != '' or total_exp != '') and (not self.old_action in operators or (total_exp+current_exp)[-1].isdigit()):
            if input_action == '(':
                current_exp += '×'
            elif total_exp != '' and self.action_mode == 2:
                total_exp += '×'
            
        # final result
        exp=''
        if self.action_mode == 2: 
            exp = total_exp + input_action + current_exp
        else: 
            exp = total_exp + current_exp + input_action 
        
        self.total_exp.config(text=exp)
        self.current_exp.delete(0, END)
        self.old_action = input_action
        
    parantes_counter = 0

    def press_eq(self, event):
        current_exp = self.current_exp.get()
        total_exp = self.total_exp.cget('text') + current_exp
        # added parantes 
        if self.parantes_counter > 0:
            if total_exp[-1] in [',','(']:
                total_exp += '0'
            for i in range(self.parantes_counter): 
                total_exp += ')' 
                self.parantes_counter -= 1
                self.action_mode = 0 
        print(total_exp)
        #
        final_exp = total_exp
        total_exp = self.exp_converter(total_exp)
        self.current_exp.delete(0, END)
        self.total_exp.config(text='')
        try:
            result = eval(total_exp)
            self.current_exp.insert(0, result)
            # save in history 
            dt_now = datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
            self.history_db.insert_exppression(final_exp, result, dt_now)
            if self.flag_history == 1:
                self.add_history(final_exp, result,dt_now)
        except:
            self.current_exp.insert(0, '')
        finally:
            self.parantes_counter = 0
            self.action_mode = 0
            self.old_action = '' 

    def key_press(self, event):
        # if keyPressed is alpha then removed then number inserted
        try:
            if event.char.isalpha():
                # limited user for write letter
                self.current_exp.delete(0, END)
            elif event.char.isdigit() and self.current_exp.get()[0].isalpha():
                exp = self.current_exp.get()[1:]
                self.current_exp.delete(0, END)
                self.current_exp.insert(0, exp[1] + event.char)
        except:
            pass

    def clear(self, event):
        self.current_exp.delete(0, END)
        self.total_exp.config(text='') 
        self.parantes_counter = 0
        self.action_mode = 0
        self.old_action = ''

    def clear_entry(self, event):
        self.current_exp.delete(0, END)

    def delete(self, event):
        exp = self.current_exp.get()
        self.current_exp.delete(0, END)
        self.current_exp.insert(len(exp)-1, exp[:len(exp)-1])

    def run(self):
        self.mainScreen.mainloop()
        self.history_db.close_connection()

if __name__=="__main__":
    (Calculator()).run()
