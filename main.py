from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivy.lang.builder import Builder
from morning import Morning
from night import Night
from database import MongoDB

database = [
    "lucas",
    "admin"
]

class LoginScreen(Screen):
    pass
class MenuScreen(Screen):
    pass
class MorningScreen(Screen):
    pass
class EveningScreen(Screen):
    pass
class ToDoScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(MorningScreen(name="morning"))
sm.add_widget(EveningScreen(name="evening"))
sm.add_widget(ToDoScreen(name="todo"))

class MyApp(MDApp):
    def build(self):
        screen = Builder.load_file('ui.kv')
        self.theme_cls.theme_style = "Dark"
        return screen

    def login_button_pressed(self):
        self.username = self.root.get_screen("login").username.text
        if self.username in database:
            self.root.current = "menu"
        else:
            self.login_error_dialog(self.username)

    def login_error_dialog(self, username):
        if username == "":
            string_error = "Please enter a username"
        else:
            string_error = self.username + " does not exist"
        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Login Failed", text=string_error,
                                buttons=[close_button])

        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def morning_button_pressed(self):
        morn = Morning()
        container = self.root.get_screen("morning").ids.container
        todolist = morn.db.get_todo_list()
        for todo in todolist:
            for task, detail in todo.items():
                item = TwoLineListItem(text=task, secondary_text=detail)
                container.add_widget(item)
        self.root.current = "morning"

    def evening_button_pressed(self):
        self.root.current = "evening"

    def submit_data_button_pressed(self):
        slider_data = self.root.get_screen("evening").slider_data
        switch_data = self.root.get_screen("evening").switch_data
        meditation = switch_data[0]
        ifast = switch_data[1]
        new_data = []

        # set first object in list to weight and adjust number
        new_data.append(round(50 + (slider_data[0] * 10), 1))
        # go through the rest of the slider objects and add the values to list
        for i in range(1, len(slider_data)):
            new_data.append(int(slider_data[i]))

        # append all the switches status to list
        for switch in switch_data:
            new_data.append(switch.active)

        night = Night(new_data)
        print(new_data)

        self.root.current = "menu"

    def add_task_button_pressed(self):
        self.task = self.root.get_screen("todo").task.text
        self.details = self.root.get_screen("todo").details.text
        if self.task == "":
            close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Enter a Task", text="Please enter a task",
                                buttons=[close_button])
            self.dialog.open()
        else:
            db = MongoDB()
            db.connect_to_localhost()
            db.add_data("todo_collection", {self.task:self.details})
            self.root.current = "menu"

MyApp().run()