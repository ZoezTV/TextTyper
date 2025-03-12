import os
import threading
import time

import keyboard
import wx
import wx.adv


def type_text(text, typing_speed=0.02):
    time.sleep(1.0)  # Füge eine längere Verzögerung vor dem Tippen hinzu (bei Bedarf anpassen)

    special_chars = {
        '!': '1',
        '"': '2',
        '§': '3',
        '$': '4',
        '%': '5',
        '&': '6',
        '/': '7',
        '(': '8',
        ')': '9',
        '=': '0',
        '?': 'ß',
        '*': '+',
        "'": '#',
        ';': ',',
        ':': '.',
        '_': '-'
    }

    alt_gr_chars = {
        '@': 'q',
        '€': 'e',
        '\\': 'ß',
        '{': '7',
        '[': '8',
        ']': '9',
        '}': '0',
        '~': '+'
    }

    for char in text:
        if char in special_chars:
            keyboard.press('shift')
            keyboard.press_and_release(special_chars[char])
            keyboard.release('shift')
        elif char in alt_gr_chars:
            keyboard.press('alt')
            keyboard.press_and_release(alt_gr_chars[char])
            keyboard.release('alt')
        elif char == '´':
            keyboard.press_and_release('´')
            keyboard.press_and_release('´')
            keyboard.press_and_release('backspace')
        elif char == '`':
            keyboard.press('shift')
            keyboard.press_and_release('´')
            keyboard.release('shift')
            keyboard.press_and_release('´')
            keyboard.press_and_release('backspace')
        elif char.isupper():
            keyboard.press('shift')
            keyboard.press_and_release(char.lower())
            keyboard.release('shift')
        else:
            keyboard.press_and_release(char)
        time.sleep(typing_speed)  # Verwende die Tippgeschwindigkeit aus der Konfiguration


class TypingThread(threading.Thread):
    """
    Ein Thread zum Tippen des Textes, um die GUI nicht zu blockieren.
    """
    def __init__(self, text, typing_speed):
        super().__init__()
        self.text = text
        self.typing_speed = typing_speed

    def run(self):
        type_text(self.text, self.typing_speed)


class InputFrame(wx.Frame):
    """
    Ein Fenster mit einem Textfeld zur Eingabe und einer Tippgeschwindigkeitskonfiguration.
    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(450, 350))

        self.typing_speed = 0.03  # Standard-Tippgeschwindigkeit

        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)

        # Textfeld
        self.text_edit = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        layout.Add(self.text_edit, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Tippgeschwindigkeitskonfiguration
        speed_label = wx.StaticText(panel, label="Tippgeschwindigkeit (Sekunden pro Zeichen):")
        layout.Add(speed_label, flag=wx.LEFT | wx.TOP, border=5)
        self.speed_ctrl = wx.SpinCtrlDouble(panel, value=str(self.typing_speed), min=0.01, max=1.0, inc=0.01)
        layout.Add(self.speed_ctrl, flag=wx.EXPAND | wx.ALL, border=5)

        # Hinweis für den Benutzer
        hint_label = wx.StaticText(panel, label="Wechsle nach dem Klicken auf 'Tippen' sofort zum Zielanwendungsfenster!")
        layout.Add(hint_label, flag=wx.LEFT | wx.TOP, border=5)

        # Button zum Starten des Tippens
        self.start_typing_button = wx.Button(panel, label="Tippen")
        layout.Add(self.start_typing_button, flag=wx.EXPAND | wx.ALL, border=5)
        self.start_typing_button.Bind(wx.EVT_BUTTON, self.on_type_button_clicked)

        panel.SetSizer(layout)

        # Setze das Fenster-Icon
        self.SetIcon(wx.Icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"), wx.BITMAP_TYPE_PNG))

        # Setze das Fenster auf "Always on Top"
        self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)

        self.Show(False)  # Fenster erst anzeigen, wenn es vom Tray-Icon aufgerufen wird

        # Verhindere, dass sich die Anwendung beendet, wenn das Fenster geschlossen wird
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_type_button_clicked(self, event):
        """
        Wird aufgerufen, wenn der Button zum Tippen geklickt wird.
        """
        text = self.text_edit.GetValue()
        self.typing_speed = self.speed_ctrl.GetValue()  # Hole die Tippgeschwindigkeit aus der Steuerung
        typing_thread = TypingThread(text, self.typing_speed)
        typing_thread.start()

    def on_close(self, event):
        """
        Wird aufgerufen, wenn das Fenster geschlossen wird.
        """
        self.Show(False)  # Fenster ausblenden
        event.Veto()  # Verhindere, dass sich das Fenster schließt


class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Ein Tray-Icon mit wxPython.
    """
    def __init__(self, frame):
        self.frame = frame
        super().__init__()

        # Setze das Icon
        icon = wx.Icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, "Text tippen")

        # Binde die Ereignisse
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.on_right_click)  # Rechtsklick binden
        self.Bind(wx.EVT_MENU, self.on_menu)

        # Erstelle das Menü
        self.menu = wx.Menu()
        self.menu_text_tippen = self.menu.Append(-1, "Text tippen")
        self.menu_beenden = self.menu.Append(-1, "Beenden")
        self.Bind(wx.EVT_MENU, self.on_menu, self.menu_text_tippen)
        self.Bind(wx.EVT_MENU, self.on_menu, self.menu_beenden)

    def on_left_click(self, event):
        """
        Wird aufgerufen, wenn auf das Tray-Icon geklickt wird.
        """
        self.frame.Show()
        self.frame.Raise()

    def on_right_click(self, event):
        """
        Wird aufgerufen, wenn auf das Tray-Icon rechtsgeklickt wird.
        """
        self.PopupMenu(self.menu)

    def on_menu(self, event):
        """
        Wird aufgerufen, wenn ein Menüpunkt ausgewählt wird.
        """
        item = event.GetId()
        if item == self.menu_text_tippen.GetId():
            self.frame.Show()
            self.frame.Raise()
        elif item == self.menu_beenden.GetId():
            self.RemoveIcon()
            wx.GetApp().ExitMainLoop()

if __name__ == '__main__':
    app = wx.App()

    # Erstelle das Hauptfenster (aber zeige es noch nicht an)
    frame = InputFrame(None, "Text tippen")

    # Erstelle das Tray-Icon
    taskBarIcon = TaskBarIcon(frame)

    app.MainLoop()
