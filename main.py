import keyboard
import threading
import time
import os

import wx
import wx.adv

# Definiere die Tastenbelegung für Deutsch zu Englisch.
# Dieses Dictionary übersetzt Zeichen von einem deutschen ins englische Tastaturlayout.
GERMAN_TO_ENGLISH = {
    'z': 'y',
    'y': 'z',
    'ß': '[',
    'ü': '{',
    'ö': ';',
    'ä': "'",
    '#': ']',
    '+': '}',
    '´': '"',
    '^': '6',
    '°': '`',
    '$': '4',
    '§': '1',
    '<': '\\',
    '>': '|',
    ' ': ' ',  # Leerzeichen bleibt Leerzeichen
}

def translate_char(char, layout="de"):
    """
    Übersetzt ein Zeichen vom deutschen ins englische Tastaturlayout, falls 'layout' auf 'en' gesetzt ist.
    """
    if layout == "en":
        if char.lower() in GERMAN_TO_ENGLISH:
            if char.isupper():
                return GERMAN_TO_ENGLISH[char.lower()].upper()
            else:
                return GERMAN_TO_ENGLISH[char.lower()]
        else:
            # Wenn das Zeichen nicht im Dictionary gefunden wird, wird es unverändert zurückgegeben.
            return char
    return char

def type_text(text, layout="de"):
    """
    Tippt den gegebenen Text unter Verwendung des angegebenen Tastaturlayouts.
    """
    time.sleep(1.0)  # Add a longer delay before typing (adjust as needed)

    for char in text:
        translated_char = translate_char(char, layout)
        keyboard.write(char)
        time.sleep(0.02)  # Füge eine kleine Verzögerung zwischen den Zeichen hinzu (anpassbar).

class TypingThread(threading.Thread):
    """
    Ein Thread zum Tippen des Textes, um die GUI nicht zu blockieren.
    """
    def __init__(self, text, layout):
        threading.Thread.__init__(self)
        self.text = text
        self.layout = layout

    def run(self):
        type_text(self.text, self.layout)

class InputFrame(wx.Frame):
    """
    Ein Fenster mit einem Textfeld zur Eingabe und einer Layout-Auswahl.
    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 300))

        self.layout_var = "de"  # Standardlayout ist Deutsch

        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)

        # Textfeld
        self.text_edit = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        layout.Add(self.text_edit, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Label für die Layout-Auswahl
        layout_label = wx.StaticText(panel, label="Wähle die Sprache im Zielfenster aus:")
        layout.Add(layout_label, flag=wx.LEFT | wx.TOP, border=5)

        # Radiobuttons für die Layout-Auswahl
        radio_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.german_radio = wx.RadioButton(panel, label="Deutsch", style=wx.RB_GROUP)
        self.english_radio = wx.RadioButton(panel, label="Englisch")
        self.german_radio.SetValue(True)  # Standardmäßig Deutsch auswählen
        radio_sizer.Add(self.german_radio, flag=wx.RIGHT, border=5)
        radio_sizer.Add(self.english_radio, flag=wx.RIGHT, border=5)
        layout.Add(radio_sizer, flag=wx.LEFT | wx.TOP, border=5)

        # Hinweis für den Benutzer
        hint_label = wx.StaticText(panel, label="Wechsle nach dem Klicken auf 'Tippen' sofort zum Zielanwendungsfenster!")
        layout.Add(hint_label, flag=wx.LEFT | wx.TOP, border=5)

        # Button zum Starten des Tippens
        self.type_button = wx.Button(panel, label="Tippen")
        layout.Add(self.type_button, flag=wx.EXPAND | wx.ALL, border=5)
        self.type_button.Bind(wx.EVT_BUTTON, self.on_type_button_clicked)

        panel.SetSizer(layout)

        # Setze das Fenster-Icon
        self.SetIcon(wx.Icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"), wx.BITMAP_TYPE_PNG))

        # Setze das Fenster auf "Always on Top"
        self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)

        self.Show(False) # Fenster erst anzeigen, wenn es vom Tray-Icon aufgerufen wird

        # Verhindere, dass sich die Anwendung beendet, wenn das Fenster geschlossen wird
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_type_button_clicked(self, event):
        """
        Wird aufgerufen, wenn der Button zum Tippen geklickt wird.
        """
        text = self.text_edit.GetValue()
        if self.german_radio.GetValue():
            layout = "de"
        else:
            layout = "en"

        # Starte das Tippen in einem separaten Thread, um die GUI nicht zu blockieren
        typing_thread = TypingThread(text, layout)
        typing_thread.start()

    def on_close(self, event):
        """
        Wird aufgerufen, wenn das Fenster geschlossen wird.
        """
        self.Show(False) # Fenster ausblenden
        event.Veto() # Verhindere, dass sich das Fenster schließt

class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Ein Tray-Icon mit wxPython.
    """
    def __init__(self, frame):
        self.frame = frame
        wx.adv.TaskBarIcon.__init__(self)

        # Setze das Icon
        icon = wx.Icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, "Text tippen")

        # Binde die Ereignisse
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.on_right_click) # Rechtsklick binden
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

def create_image():
    """
    Lädt ein Bild aus einer PNG-Datei im selben Pfad wie das Skript.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Pfad des Skripts
    icon_path = os.path.join(script_dir, "icon.png")  # Pfad zur Icon-Datei

    # Gib ein Dummy-Objekt zurück, da es nicht mehr benötigt wird
    return None

if __name__ == '__main__':
    app = wx.App()

    # Erstelle das Hauptfenster (aber zeige es noch nicht an)
    frame = InputFrame(None, "Text tippen")

    # Erstelle das Tray-Icon
    taskBarIcon = TaskBarIcon(frame)

    app.MainLoop()
