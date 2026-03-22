from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests


class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # שדות קלט
        self.username = TextInput(hint_text="Username")
        self.interests = TextInput(hint_text="Interests (comma separated)")

        # כפתורים
        btn_register = Button(text="Register")
        btn_register.bind(on_press=self.send_data)

        btn_load = Button(text="Load Users")
        btn_load.bind(on_press=self.load_users)

        btn_match = Button(text="Find Match")
        btn_match.bind(on_press=self.find_match)

        # תצוגה
        self.users_label = Label(text="Users will appear here")

        # הוספה למסך
        layout.add_widget(self.username)
        layout.add_widget(self.interests)
        layout.add_widget(btn_register)
        layout.add_widget(btn_load)
        layout.add_widget(btn_match)
        layout.add_widget(self.users_label)

        return layout

    def send_data(self, instance):
        data = {
            "username": self.username.text,
            "interests": self.interests.text.split(",")
        }

        try:
            requests.post("http://127.0.0.1:5000/register", json=data)
            self.users_label.text = "User registered!"
        except:
            self.users_label.text = "Error connecting to server"

    def load_users(self, instance):
        try:
            res = requests.get("http://127.0.0.1:5000/users")
            users = res.json()

            text = ""
            for u in users:
                text += f"{u['username']} - {u['interests']}\n"

            self.users_label.text = text if text else "No users yet"
        except:
            self.users_label.text = "Error loading users"

    def find_match(self, instance):
        try:
            res = requests.get("http://127.0.0.1:5000/users")
            users = res.json()

            my_interests = set(self.interests.text.split(","))

            matches = []

            for u in users:
                other_interests = set(u["interests"])
                if my_interests & other_interests and u["username"] != self.username.text:
                    matches.append(u["username"])

            if matches:
                self.users_label.text = "Matches:\n" + "\n".join(matches)
            else:
                self.users_label.text = "No matches found"
        except:
            self.users_label.text = "Error finding matches"


MainApp().run()