Windows_Mode = False

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from random import choice
from requests import get
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.base import EventLoop
from threading import Thread
from time import sleep


if (Windows_Mode):
    Window.size = (380, 768)
    Window.top = 0
    Window.left = 986

UI = '''
MDScreenManager:

    MDScreen:

        name : "home"

        MDBoxLayout:

            orientation : "vertical"
            spacing : "0dp"
            padding : "0dp"
            # md_bg_color : [1, 0, 0, 1]

            MDTopAppBar:

                id : home_screen_top_app_bar
                title : "Tic Tac Toe"
                right_action_items : [["refresh", lambda x : app.refresh()]]
                # left_action_items : [["menu", lambda x : app.debug()]]
                md_bg_color : app.theme_color
                elevation : 3

            MDBoxLayout:

                orientation : "vertical"
                spacing : "0dp"
                padding : "0dp"
                size_hint : (1, 0.4)
                # md_bg_color : [1, 0, 0, 1]

                MDLabel:
                    id : player_text
                    text : "You : " + app.player
                    halign : "center"
                    font_size : "20sp"

            MDBoxLayout:
                orientation : "vertical"
                spacing : "0dp"
                padding : "1dp"
                # md_bg_color : [0, 1, 0, 1]

                MDGridLayout:

                    rows : 3
                    cols : 3
                    spacing : "5dp"
                    padding : "10dp"
                    # md_bg_color : [0.2, 0.2, 0, 1]

                    MDCard:
                        id : btn_00
                        md_bg_color : app.box_color
                        on_release : app.btn_00()
                        border : 5

                        MDLabel:
                            id : text_00
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_01
                        md_bg_color : app.box_color
                        on_release : app.btn_01()

                        MDLabel:
                            id : text_01
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_02
                        md_bg_color : app.box_color
                        on_release : app.btn_02()

                        MDLabel:
                            id : text_02
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_10
                        md_bg_color : app.box_color
                        on_release : app.btn_10()

                        MDLabel:
                            id : text_10
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_11
                        md_bg_color : app.box_color
                        on_release : app.btn_11()

                        MDLabel:
                            id : text_11
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_12
                        md_bg_color : app.box_color
                        on_release : app.btn_12()

                        MDLabel:
                            id : text_12
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_20
                        md_bg_color : app.box_color
                        on_release : app.btn_20()

                        MDLabel:
                            id : text_20
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_21
                        md_bg_color : app.box_color
                        on_release : app.btn_21()

                        MDLabel:
                            id : text_21
                            halign : "center"
                            font_size : app.o_x_size
                    
                    MDCard:
                        id : btn_22
                        md_bg_color : app.box_color
                        on_release : app.btn_22()

                        MDLabel:
                            id : text_22
                            halign : "center"
                            font_size : app.o_x_size
            
            MDBoxLayout:
                orientation : "horizontal"
                spacing : "0dp"
                padding : "1dp"
                size_hint : (1, 0.4)
                # md_bg_color : [0, 0, 1, 1]

                MDBoxLayout:
                    orientation : "vertical"
                    spacing : "0dp"
                    padding : "20dp"
                    # md_bg_color : [0.1, 0.2, 0, 1]

                    MDLabel:
                        id : player_x_text
                        text : "Player X"
                        halign : "center"
                        bold : True
                        font_size : "24sp"

                MDBoxLayout:
                    orientation : "vertical"
                    spacing : "0dp"
                    padding : "20dp"
                    # md_bg_color : [0, 0.1, 0.2, 1]

                    MDLabel:
                        id : player_o_text
                        text : "Player O"
                        halign : "center"
                        font_size : "16sp"
                
'''

class App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_color = [123/255, 2/255, 144/255, 255/255]
        self.dt = 0.2
        self.dialog_opener_dt = 0.2
        self.moves = 0
        self.draw_memory = True
        self.refresh_memory = False
        self.config_dict = {"win_dialog" : False, "lose_dialog" : False, "draw_dialog" : False}
        self.dialog_opener_schedule = Clock.schedule_interval(self.dialog_opener, self.dialog_opener_dt)

        self.o_x_size = "72sp"
        self.box_color = [0.9, 0.9, 0.9, 1]

        self.host = "amoghthusoo.pythonanywhere.com"
        #self.host = "192.168.137.1:8000"
        r = get(f"http://{self.host}/tic_tac_toe/synchronize/_").json()
        
        if(r["val"] == None):
            
            toss = choice(["X", "O"])
            get(f"http://{self.host}/tic_tac_toe/synchronize/{toss}")
            self.player = toss
            
            if(toss == "X"):
                self.turn = True
                self.opponent = "O"
            else:
                self.turn = False
                self.opponent = "X"
                # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                Thread(target=self.get_fun, daemon=True).start()

        else:
            if(r["val"] == "X"):
                self.player = "O"
                self.opponent = "X"
                self.turn = False
                # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                Thread(target=self.get_fun, daemon=True).start()
            else:
                self.player = "X"
                self.opponent = "O"
                self.turn = True

        self.self_state = [[False for _ in range(3)] for _ in range(3)]
        self.opponent_state = [[False for _ in range(3)] for _ in range(3)]
        
        if(self.player == "O" and Windows_Mode):
            Window.left = 0

    def btn_00(self):
        
        if(self.turn and not self.self_state[0][0]):
            
            self.root.ids.text_00.text = self.player
            self.self_state[0][0] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/00")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/00")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

            
    
    def btn_01(self):
        if(self.turn and not self.self_state[0][1]):
            
            self.root.ids.text_01.text = self.player
            self.self_state[0][1] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/01")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/01")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

            
    
    def btn_02(self):
        if(self.turn and not self.self_state[0][2]):
            
            self.root.ids.text_02.text = self.player
            self.self_state[0][2] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/02")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/02")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()
    
    def btn_10(self):
        if(self.turn and not self.self_state[1][0]):
            
            self.root.ids.text_10.text = self.player
            self.self_state[1][0] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/10")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/10")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

    def btn_11(self):
        if(self.turn and not self.self_state[1][1]):
            
            self.root.ids.text_11.text = self.player
            self.self_state[1][1] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/11")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/11")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

            
    
    def btn_12(self):
        if(self.turn and not self.self_state[1][2]):
            
            self.root.ids.text_12.text = self.player
            self.self_state[1][2] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/12")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/12")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

    def btn_20(self):
        if(self.turn and not self.self_state[2][0]):
            
            self.root.ids.text_20.text = self.player
            self.self_state[2][0] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/20")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/20")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

            
    def btn_21(self):
        if(self.turn and not self.self_state[2][1]):
            
            self.root.ids.text_21.text = self.player
            self.self_state[2][1] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/21")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/21")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

            
    
    def btn_22(self):
        if(self.turn and not self.self_state[2][2]):
            
            self.root.ids.text_22.text = self.player
            self.self_state[2][2] = True
            self.turn = False
            self.moves += 1
            self.negate_bold()
            self.check_winner()
            self.check_draw()

            def send_to_server():

                if(self.player == "X"):
                    get(f"http://{self.host}/tic_tac_toe/put_X/22")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()
                else:
                    get(f"http://{self.host}/tic_tac_toe/put_O/22")
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target=self.get_fun, daemon=True).start()

                
                raise Exception
            
            Thread(target=send_to_server, daemon=True).start()

            
    def get_fun(self):
        
        while(True):
            if(self.player == "X"):
                r = get(f"http://{self.host}/tic_tac_toe/get_O").json()
            else:
                r = get(f"http://{self.host}/tic_tac_toe/get_X").json()

            if(r["val"] != None):

                if(r["val"] == "00"):
                    self.root.ids.text_00.text = self.opponent
                
                elif(r["val"] == "01"):
                    self.root.ids.text_01.text = self.opponent
                
                elif(r["val"] == "02"):
                    self.root.ids.text_02.text = self.opponent
                
                elif(r["val"] == "10"):
                    self.root.ids.text_10.text = self.opponent
                
                elif(r["val"] == "11"):
                    self.root.ids.text_11.text = self.opponent
                
                elif(r["val"] == "12"):
                    self.root.ids.text_12.text = self.opponent
                
                elif(r["val"] == "20"):
                    self.root.ids.text_20.text = self.opponent
                
                elif(r["val"] == "21"):
                    self.root.ids.text_21.text = self.opponent
                
                elif(r["val"] == "22"):
                    self.root.ids.text_22.text = self.opponent
                
                self.opponent_state[int(r["val"][0])][int(r["val"][1])] = True
                self.turn = True
                self.moves += 1
                self.negate_bold()
                self.check_winner()
                self.check_draw()
                
                raise Exception

            sleep(self.dt)
        

    def negate_bold(self):
        
        if(self.root.ids.player_x_text.bold):
            self.root.ids.player_x_text.bold = False
            self.root.ids.player_x_text.font_size = "16sp"
            
            self.root.ids.player_o_text.bold = True
            self.root.ids.player_o_text.font_size = "24sp"
        else:
            self.root.ids.player_x_text.bold = True
            self.root.ids.player_x_text.font_size = "24sp"
            
            self.root.ids.player_o_text.bold = False
            self.root.ids.player_o_text.font_size = "16sp"

    def check_winner(self):
        
        if(
            (self.self_state[0][0] == True and self.self_state[0][1] == True and self.self_state[0][2] == True) or
            (self.self_state[1][0] == True and self.self_state[1][1] == True and self.self_state[1][2] == True) or
            (self.self_state[2][0] == True and self.self_state[2][1] == True and self.self_state[2][2] == True) or
            (self.self_state[0][0] == True and self.self_state[1][0] == True and self.self_state[2][0] == True) or
            (self.self_state[0][1] == True and self.self_state[1][1] == True and self.self_state[2][1] == True) or
            (self.self_state[0][2] == True and self.self_state[1][2] == True and self.self_state[2][2] == True) or
            (self.self_state[0][0] == True and self.self_state[1][1] == True and self.self_state[2][2] == True) or
            (self.self_state[0][2] == True and self.self_state[1][1] == True and self.self_state[2][0] == True)
        ):
            self.draw_memory = False
            self.config_dict["win_dialog"] = True
            
            self.refresh_memory = True
            self.disable_cards()

        elif(
            (self.opponent_state[0][0] == True and self.opponent_state[0][1] == True and self.opponent_state[0][2] == True) or
            (self.opponent_state[1][0] == True and self.opponent_state[1][1] == True and self.opponent_state[1][2] == True) or
            (self.opponent_state[2][0] == True and self.opponent_state[2][1] == True and self.opponent_state[2][2] == True) or
            (self.opponent_state[0][0] == True and self.opponent_state[1][0] == True and self.opponent_state[2][0] == True) or
            (self.opponent_state[0][1] == True and self.opponent_state[1][1] == True and self.opponent_state[2][1] == True) or
            (self.opponent_state[0][2] == True and self.opponent_state[1][2] == True and self.opponent_state[2][2] == True) or
            (self.opponent_state[0][0] == True and self.opponent_state[1][1] == True and self.opponent_state[2][2] == True) or
            (self.opponent_state[0][2] == True and self.opponent_state[1][1] == True and self.opponent_state[2][0] == True)
        ):
            self.draw_memory = False
            self.config_dict["lose_dialog"] = True
            
            self.refresh_memory = True
            self.disable_cards()

    def check_draw(self):

        if(self.moves >= 9 and self.draw_memory):
            self.config_dict["draw_dialog"] = True
            
            self.refresh_memory = True
            self.disable_cards()

    def reset(self, reference):

        self.config_dict["win_dialog"] = False
        self.config_dict["lose_dialog"] = False
        self.config_dict["draw_dialog"] = False
        
        self.moves = 0
        self.draw_memory = True
        self.self_state = [[False for _ in range(3)] for _ in range(3)]
        self.opponent_state = [[False for _ in range(3)] for _ in range(3)]

        def server_tasks():
     
            r = get(f"http://{self.host}/tic_tac_toe/synchronize/_").json()
            
        
            if(r["val"] == None):
                
                toss = choice(["X", "O"])

                
                get(f"http://{self.host}/tic_tac_toe/synchronize/{toss}")

                self.player = toss
                
                if(toss == "X"):
                    self.turn = True
                    self.opponent = "O"
                else:
                    self.turn = False
                    self.opponent = "X"
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target = self.get_fun, daemon=True).start()

            else:
                if(r["val"] == "X"):
                    self.player = "O"
                    self.opponent = "X"
                    self.turn = False
                    # self.get_fun_schedule = Clock.schedule_interval(self.get_fun, self.dt)
                    Thread(target = self.get_fun, daemon=True).start()

                else:
                    self.player = "X"
                    self.opponent = "O"
                    self.turn = True

            self.root.ids.player_text.text = "You : " + self.player

            raise Exception
        
        Thread(target = server_tasks, daemon=True).start()

        self.root.ids.text_00.text = ""
        self.root.ids.text_01.text = ""
        self.root.ids.text_02.text = ""
        self.root.ids.text_10.text = ""
        self.root.ids.text_11.text = ""
        self.root.ids.text_12.text = ""
        self.root.ids.text_20.text = ""
        self.root.ids.text_21.text = ""
        self.root.ids.text_22.text = ""

        self.root.ids.player_x_text.bold = True
        self.root.ids.player_x_text.font_size = "24sp"

        self.root.ids.player_o_text.bold = False
        self.root.ids.player_o_text.font_size = "16sp"
        

        self.refresh_memory = False
        self.enable_cards()

        self.dialog.dismiss()

    def refresh(self):

        if(self.refresh_memory):
            self.reset("_")
            self.refresh_memory = False

    def on_start(self):
        # self.fps_monitor_start()
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        
        if key == 27:
            get(f"http://{self.host}/tic_tac_toe/reset")
            self.stop()
        
        # return True

    def disable_cards(self):
        self.root.ids.btn_00.disabled = True
        self.root.ids.btn_01.disabled = True
        self.root.ids.btn_02.disabled = True
        self.root.ids.btn_10.disabled = True
        self.root.ids.btn_11.disabled = True
        self.root.ids.btn_12.disabled = True
        self.root.ids.btn_20.disabled = True
        self.root.ids.btn_21.disabled = True
        self.root.ids.btn_22.disabled = True

    def enable_cards(self):
        self.root.ids.btn_00.disabled = False
        self.root.ids.btn_01.disabled = False
        self.root.ids.btn_02.disabled = False
        self.root.ids.btn_10.disabled = False
        self.root.ids.btn_11.disabled = False
        self.root.ids.btn_12.disabled = False
        self.root.ids.btn_20.disabled = False
        self.root.ids.btn_21.disabled = False
        self.root.ids.btn_22.disabled = False

    def dialog_opener(self, dt):
        
        if(self.config_dict["win_dialog"]):
            self.config_dict["win_dialog"] = False
            self.dialog = MDDialog(
                title = "Congratulations!",
                text = "You Won!",
                size_hint = (0.9, 0.2),
                buttons=[
                    MDRaisedButton(
                        text = "New Game",
                        md_bg_color = self.theme_color,
                        on_release = self.reset
                    ), 
                    MDRaisedButton(
                        text = "Back",
                        md_bg_color = self.theme_color,
                        on_release = self.close_dialog
                    )
                ],
            )
            self.dialog.open()
        
        elif(self.config_dict["lose_dialog"]):
            self.config_dict["lose_dialog"] = False
            self.dialog = MDDialog(
                title = "Oops...",
                text = "You lost!",
                size_hint = (0.9, 0.2),
                buttons=[
                    MDRaisedButton(
                        text = "New Game",
                        md_bg_color = self.theme_color,
                        on_release = self.reset
                    ),
                    MDRaisedButton(
                        text = "Back",
                        md_bg_color = self.theme_color,
                        on_release = self.close_dialog
                    )
                ],
            )
            self.dialog.open()
        elif(self.config_dict["draw_dialog"]):

            self.config_dict["draw_dialog"] = False
            self.dialog = MDDialog(
                title = "Oops...",
                text = "Draw!",
                size_hint = (0.9, 0.2),
                buttons=[
                    MDRaisedButton(
                        text = "New Game",
                        md_bg_color = self.theme_color,
                        on_release = self.reset
                    ),
                    MDRaisedButton(
                        text = "Back",
                        md_bg_color = self.theme_color,
                        on_release = self.close_dialog
                    )
                ],
            )
            self.dialog.open()


    def close_dialog(self, reference):
        self.dialog.dismiss()

    def close(self):
        self.stop()

    def debug(self):
        print(self.player)
        print(self.self_state)
        print(self.opponent_state)
        print(self.config_dict)

    def build(self):
        self.app = Builder.load_string(UI)
        return self.app
    
if(__name__ == "__main__"):
    app = App()
    app.run()
