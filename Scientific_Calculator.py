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
import string
from time import sleep
from threading import Thread


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
        display_frame.pack(fill=X)
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
        self.total_exp = Label(display_frame, width=15, font='verdana 20', anchor=E, bg='white', bd=0)
        self.total_exp.pack(expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.total_exp.bind('<ButtonPress-1>',self.showText)
        # current expression
        self.current_exp = StringVar(display_frame, value='0') 
        self.current_exp_widget = Label(display_frame, width=15, font='verdana 20', textvariable=self.current_exp, anchor=E, bd=0, bg='#fff')
        self.current_exp_widget.pack(expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.current_exp_widget.bind('<ButtonPress-1>',self.showText)
        self.mainScreen.bind('<KeyRelease>', self.on_key_release)
        self.mainScreen.bind('<KeyPress>', self.on_key_press) 
        # the dictionary created columns
        # keys is number of column and value is dictionary of buttons
        collection_btns = {
            0: {
                'log': self.on_click_action,
                '√': self.on_click_action,
                'x^y': self.on_click_action,
                'pi': self.btn_pi,
                'n!': self.on_click_action,
                '(': self.on_click_action,
            },
            1: {
                'sin': self.on_click_action,
                'CE': self.clear_entry,
                7: self.on_click_number,
                4: self.on_click_number,
                1: self.on_click_number,
                ')': self.on_click_action,
            },
            2: {
                'cos': self.on_click_action,
                'C': self.clear,
                8: self.on_click_number,
                5: self.on_click_number,
                2: self.on_click_number,
                0: self.on_click_number,
            },
            3: {
                'tan': self.on_click_action,
                'Del': self.delete,
                9: self.on_click_number,
                6: self.on_click_number,
                3: self.on_click_number,
                '.': self.on_click_number,
            },
            4: {
                'mod': self.on_click_action,
                '÷': self.on_click_action,
                '×': self.on_click_action,
                '-': self.on_click_action,
                '+': self.on_click_action,
                '=': self.on_press_equal,
            }
        }
        # The buttons is stored in this dictionary example:
        # self.obj_buttons['=']['bg'] = '#0ff'
        self.obj_buttons = {}

        # create table for manage columns 
        self.table = {} 
        # main:frame used for solving problem responsive of columns 
        main = Frame(self.main_frame)
        main.pack(fill=BOTH,expand=1) 
        # create columns 
        for col_index,btns in collection_btns.items():
            self.table[col_index] = Frame(main)
            self.table[col_index].pack(side=LEFT, expand=1, fill=BOTH)
            # create buttons and inserted in the columns
            for btn_name, func in btns.items(): 
                self.create_btn(btn=Button(self.table[col_index]), txt=str(btn_name), event=func) 
        
    def create_btn(self, btn, txt, event): 
        btn.config(text=txt, bd=0, relief='groove', width=5, bg='#fff', font=('verdana',15),cursor="hand2")
        if not txt.isdigit():
            btn['bg'] = '#ffd' 
        btn.bind('<ButtonPress-1>', event)
        btn.bind('<Enter>', self.on_Enter_Mouse)
        btn.bind('<Leave>', self.on_Leave_Mouse)
        self.obj_buttons[txt] = btn
        self.obj_buttons[txt].pack(fill=BOTH,expand=1) 

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
        _dateTime['bg'] = '#ffd'
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
            _dateAndTime = parent.winfo_children()[0].get(0.0, END).strip()
            _exp = parent.winfo_children()[1].get(0.0, END).strip()
            _result = parent.winfo_children()[2].get(0.0, END).strip()
            self.current_exp.set("")
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
                _width -= 400
                self.mainScreen.geometry(f'{_width}x{_height}')
                self.mainScreen.minsize(width=400, height=400)
                self.parent_history.destroy()
            else:
                _width += 400
                self.flag_history = 1
                self.mainScreen.geometry(f'{_width}x{_height}')
                self.mainScreen.minsize(width=800, height=400)
                self.create_frame_history()

    def hasNumber(self, inputString):
        return any(char.isdigit() for char in inputString)

    num_flag = False
    # if pressed pi flag=true then if you press any digits, deleted current_expression
    def btn_pi(self, event):
        self.num_flag = True 
        self.current_exp.set(math.pi)

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
            self.current_exp.set('')
        exp = self.current_exp.get()
        if len(exp) == 1 and exp[0] == '0' and event.widget['text']!='0':
            exp = '' 
        try: 
            exp = exp[1:] if exp[0].isalpha() else exp
        except: pass
        exp = (exp + event.widget['text']) 
        self.current_exp.set(exp)

    def on_Enter_Mouse(self, event): 
        self.set_color(event.widget['text'],'mouse_enter')

    def on_Leave_Mouse(self, event): 
        self.set_color(event.widget['text'], 'mouse_leave')

    def showText(self,event): 
        contentBox = Toplevel(self.mainScreen,width=0,height=0)
        contentBox.geometry('400x300')
        contentBox.title("") 
        contentBox.iconphoto(False, PhotoImage(file=r"icon\main_icon.png"))
        textBox = Text(contentBox,font='segeo 20',bd=0,relief=FLAT)
        textBox.insert(END,event.widget['text'])
        textBox.pack(fill=BOTH,expand=1) 
        def rightClick(e):
            def rClick_Copy(e):
                e.widget.event_generate('<Control-c>')
            try:
                e.widget.focus()
                rmenu = Menu(None, tearoff=0, takefocus=0,bg="#fff",font='segoe 14')
                rmenu.add_command(label='Copy', command=lambda e=e: rClick_Copy(e))
                rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
            except:
                pass
        textBox.bind('<Button-3>',rightClick)
        contentBox.mainloop()

    def set_color(self, button, event_type):
        if event_type == 'mouse_enter':
            self.BG_COLOR = self.obj_buttons[button]['bg']
            self.FG_COLOR = self.obj_buttons[button]['fg']
            if button in '=+-÷×':
                self.obj_buttons[button]['bg'] = "#15b"
                self.obj_buttons[button]['fg'] = "#fff"
            else:
                self.obj_buttons[button]['bg'] = "#dfdfdf" 
            
        elif event_type == 'mouse_leave':
            self.obj_buttons[button]['bg'] = self.BG_COLOR
            self.obj_buttons[button]['fg'] = self.FG_COLOR    

    _actions = []
    def actions_converter(self, exp: str): 
        for i in self._actions:
            if i[0] in exp:
                exp = exp.replace(i[0], i[1])
        return exp

    # action modes:
    # 2: sin(),cos(),tan(),fact(),log() : before action is operator
    # 1: root  : before action is digit
    action_mode = 0
    prev_action_mode = 0
    # prev_action for change action
    prev_action = ''

    def on_action(self,input_action, current_exp, total_exp,event_type):
        _action = input_action
        _input = current_exp
        parantes_flag = False
        actions_dict = {
            # action : [ action, seperator, parantes_count, action_mode, main_shape],
            # log by module math is calculated
            'log':  ['log(',    ',',    1,      2,      ''],
            'sin':  ['sin(',    '',     1,      2,      'self._sin('],
            'cos':  ['cos(',    '',     1,      2,      'self._cos('],
            'tan':  ['tan(',    '',     1,      2,      'self._tan('],
            'n!':   ['fact(',   '',     1,      2,      'self._fact('],
            '√':    ['root(',   '',     1,      1,      '**(1/'],
            'x^y':  ['^',       '',     0,      0,      '**'],
            '^':    ['^',       '',     0,      0,      '**'],
            '(':    ['(',       '',     1,      0,      ''],
            ')':    [')',       '',     -1,     0,      ''],
            '×':    ['×',       '',     0,      0,      '*'],
            '*':    ['×',       '',     0,      0,      '*'],
            '÷':    ['÷',       '',     0,      0,      '/'],
            '/':    ['÷',       '',     0,      0,      '/'],
            'mod':  ['mod',     '',     0,      0,      '%'],
            '%':    ['mod',     '',     0,      0,      '%'],
            '+':    ['+',       '',     0,      0,      ''],
            '-':    ['-',       '',     0,      0,      ''],
        }
        # get values of actions_dict
        action_list = actions_dict.get(input_action)
        
        
        # get values of action_list
        if action_list != None:
            input_action = action_list[0]
            current_exp += action_list[1]
            self.parantes_counter = self.parantes_counter + action_list[2]
            self.action_mode = action_list[3]

            # added action to _actions:list for convert action to function or operator
            if action_list[-1] != '' and [action_list[0], action_list[-1]] not in self._actions:
                self._actions.append([action_list[0], action_list[-1]]) 

            # limited parantes
            if self.parantes_counter < 0 and input_action == ')':
                self.parantes_counter = 0
                input_action = ''
                parantes_flag = True 

        # added new_function to before old_function sample: old=tan(), new:sin() => sin(tan())
        try:
            ce, te = self.nested_functions(current_exp, total_exp, action_list[0], _input)
            if ce != None and te != None:
                current_exp = ce
                total_exp = te
        except:
            pass

        # parantes control for any function ex: log() , 25root(2)...
        if self.prev_action_mode > 0 and self.parantes_counter > 0 and input_action != ')':
            current_exp += ')'
            self.prev_action_mode = 0
            self.parantes_counter -= 1

        # change operator
        operators = ['+', '-', '×', '÷', 'mod', '^']
        if self.prev_action in operators and input_action in operators and current_exp in ['0', '']: 
            total_exp = total_exp[:len(total_exp)-len(self.prev_action)] 
            current_exp = '' 
        
    
        # insert mul between parenthesis or digit and parenthes ex: ()×() , 2×()
        current_exp, total_exp = self.insert_mul(current_exp, total_exp, input_action) 

        exp = ''
        if parantes_flag:
            exp = total_exp
        elif input_action == ')' and (total_exp[-1] == ')' or total_exp[-1].isdigit()):
            exp = total_exp + input_action
        elif total_exp != '' and total_exp[-1] != '(' and current_exp == '0':
            exp = total_exp + input_action
        elif self.action_mode == 2:
            exp = total_exp + input_action + current_exp
        else:
            exp = total_exp + current_exp + input_action 
        
        # This action will be saved for later edits
        self.prev_action = input_action
        self.prev_action_mode = self.action_mode
        if self.action_mode == 2:
            self.func_counter += 1

        return exp

    def on_click_action(self, event):
        # this method for add a action to expresion
        # action is operator or function 
        exp = self.on_action(
                        event.widget['text'],
                        self.current_exp.get(),
                        self.total_exp.cget('text'),'mouse') 
                        
        self.total_exp['text'] = exp
        self.current_exp.set('0') 
        
    func_counter = 0
    def nested_functions(self,current_exp,total_exp,action,_input): 
        # added function to before old_function 
        try:
            if self.prev_action_mode > 0 and self.action_mode == 2:
                # fix log() seperator
                if action == 'log(' and self.prev_action in ['sin(','cos(','tan(','fact(','log(']: 
                    total_exp+=')' 
                    self.parantes_counter -= 1 if self.parantes_counter-1>=0 else 0
                    if _input == '0': 
                        total_exp += ',10' 
                    else:
                        total_exp += ',' + _input

                total_exp = total_exp[::-1]
                self.prev_action = self.prev_action[::-1]
                index = total_exp.index(self.prev_action)+len(self.prev_action)  # len old exp
                # 
                if self.func_counter>0:
                    # controlled if new_func == old_func - sample:
                    # currect: sin(tan(tan())) , incurrect: tan(sin(tan()))
                    index += len(self.prev_action)
                    self.func_counter -= 1 if self.func_counter-1 >= 0 else 0

                # 25root() -> get 25
                if self.prev_action_mode == 1:
                    for i in range(index, len(total_exp)):
                        if total_exp[i].isdigit():
                            index += 1 
                    
                current_exp = total_exp[:index] # get old exp
                total_exp = total_exp[index:]  # cut
                total_exp = total_exp[::-1]
                current_exp = current_exp[::-1]
                self.prev_action = self.prev_action[::-1]        
        except: pass
        return current_exp, total_exp

    def insert_mul(self, current_exp, total_exp, action):  
        operators = ['+', '-', '×', '÷','mod', 'd', '^', '('] 
        if (current_exp == '0' and action == '('):
            current_exp = '' 
        
        if (not current_exp in ['', '0']) or total_exp != '' or self.prev_action_mode > 0:
            if (not self.prev_action in operators or (total_exp+current_exp)[-1].isdigit()):
                if action == '(' and ( not current_exp in ['','0']):
                    current_exp += '×'
                elif self.action_mode == 2 and len(total_exp)>0 and total_exp[-1] == ')':
                    total_exp += '×' 
        
        return current_exp, total_exp 

    parantes_counter = 0

    def on_press_equal(self, event): 
        current_exp = self.current_exp.get()
        total_exp   = self.total_exp.cget('text')
        
        if current_exp == '0' and total_exp == '': 
            return None
        
        elif total_exp != '' and total_exp[-1] in (string.digits+')'):
            # fix problem added digit from current to end total when hasn't input action
            current_exp = ''

        total_exp   += current_exp
        
        # added parantes 
        if self.parantes_counter > 0:
            if total_exp[-1] in [',','(']:
                total_exp += '0'
            for i in range(self.parantes_counter): 
                total_exp += ')' 
                self.parantes_counter -= 1
                self.action_mode = 0 
        # 
        final_exp = total_exp
        total_exp = self.actions_converter(total_exp) 
        self.current_exp.set('')
        self.total_exp.config(text='')
        try: 
            result = eval(total_exp) 
            self.current_exp.set(result) 
            # save in history 
            dt_now = datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
            self.history_db.insert_exppression(final_exp, result, dt_now)
            if self.flag_history == 1:
                self.add_history(final_exp, result,dt_now)
        except: 
            self.current_exp.set('0')
        finally:
            self.parantes_counter = 0
            self.action_mode = 0
            self.prev_action = '' 
            self.operator_list = [] 

    # history of keys pressed 
    # for return the buttons to default color
    key_history = [] 
    def on_key_press(self, event): 
        try: 
            if event.keycode == 16 or (event.char not in '+-*/%^.()=' and event.char in string.punctuation): 
                # exited if pressed shift key
                # exited if key is symbol
                return None 

            keyChar = event.char
            match event.char:
                case '*':
                            keyChar = '×'
                case '/':
                            keyChar = '÷'
                case '%':
                            keyChar = 'mod' 
                case '^':
                            keyChar = 'x^y' 
            match event.keysym:
                case 'BackSpace':
                            keyChar = 'Del'
                            self.delete(event)
                case 'Escape':
                            self.clear(event) 
                            keyChar = 'C'
                case 'Delete':
                            self.clear_entry(event) 
                            keyChar = 'CE'
                case 'Return':
                            self.on_press_equal(event)
                            keyChar = '='
                case 'equal':
                            self.on_press_equal(event) 

            self.key_history.append(keyChar)
            if keyChar in '=+-÷×' or keyChar in ['mod','x^y']:
                self.obj_buttons[keyChar]['bg'] = "#15b"
                self.obj_buttons[keyChar]['fg'] = "#fff"
            else:
                self.obj_buttons[keyChar]['bg'] = "#dfdfdf"

            # run timer after press key for set default color 
            def countDown(): 
                sleep(0.1)
                keyChar = self.key_history.pop(0)
                if self.obj_buttons.get(keyChar) != None:
                    self.obj_buttons.get(keyChar)['bg'] = '#fff' if keyChar.isdigit() else '#ffd'
                    self.obj_buttons.get(keyChar)['fg'] = '#000' 
            countDown_thread = Thread(target=countDown)
            countDown_thread.start()
        except:
            pass 

    
    def on_key_release(self, event):
        # after key press this method checked key if invalid not insert in current_exp;
        
        try: 
            # key validation
            if event.keycode in [8,13,16,27,32,46] or event.char.isalpha() or (event.char not in '+-*/%^.()' and event.char in string.punctuation):
                # exited if Key is ENTER,SHIFT,ESC,BACKSPACE,DELETE,SPACE
                # exited if key is SYMBOL
                # exited if key is ALPHABET Or LETTER
                return None 

            inputChar = event.char 
            current_exp = self.current_exp.get() 
            total_exp = self.total_exp.cget('text') 
            
            if inputChar in '+-*/%^()': 
                match inputChar:
                    case '*':   # *
                                inputChar = '×' 
                    case '/':   # /
                                inputChar = '÷'
                    case '%':    # %
                                inputChar = 'mod' 
                exp = self.on_action(inputChar, current_exp, total_exp, 'key')
                self.total_exp['text'] = exp if exp != '0' else ''
                self.current_exp.set('0')
                self.prev_action = inputChar
                self.prev_action_mode = self.action_mode
                if self.action_mode == 2:
                    self.func_counter += 1
            elif inputChar.isdigit():
                if current_exp == '0':
                    self.current_exp.set(inputChar)
                else:
                    self.current_exp.set(current_exp+inputChar)
            elif current_exp.count('.') == 0:
                self.current_exp.set(current_exp+inputChar)
                
            
        except:
            pass

    def clear(self, event): 
        self.current_exp.set('0')
        self.total_exp.config(text='') 
        # values
        self.parantes_counter = 0
        self.action_mode = 0
        self.prev_action_mode = 0
        self.prev_action = ''
        self._actions = []

    def clear_entry(self, event):
        self.current_exp.set('0') 

    def delete(self, event): 
        exp = self.current_exp.get()[:-1] 
        self.current_exp.set(exp if exp != '' else '0')
    
    def run(self):
        self.mainScreen.mainloop()
        self.history_db.close_connection()

if __name__=="__main__":
    (Calculator()).run()
