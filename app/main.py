import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty

from pymongo import MongoClient, errors

# global variables for MongoDB host (default port is 27017)
DOMAIN = 'localhost:'
PORT = 27017

# connect to MongoDB
try:
    client = MongoClient(host = [str(DOMAIN) + str(PORT)], serverSelectionTimeoutMS = 3000)
    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])

except errors.ServerSelectionTimeoutError as err:
    # set the client and db names to 'None' and [] if exception
    client = None
    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)

class MainScreen(Screen):
    pass

class NewRecpScreen(Screen):
    pass

class ViewRecpScreen(Screen):
    pass

class CreBasketScreen(Screen):
    pass

class ViewBasketScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass



class MyBasketApp(App):
    def build(self):
        self.title = 'My Basket App'
        return self.root
    
if __name__ == '__main__':
    MyBasketApp().run()

