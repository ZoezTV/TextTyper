# TextTyper

TextTyper ist eine einfache Anwendung zur Automatisierung von Tippaufgaben. Sie ermöglicht es Benutzern, Text einzugeben und automatisch in ein beliebiges Anwendungsfenster zu tippen, indem Tastatureingaben simuliert werden. Dies kann besonders nützlich für sich wiederholende Tippaufgaben oder Demonstrationen sein.

## Funktionen

- Unterstützt deutsches Tastaturlayout.
- Konfigurierbare Tippgeschwindigkeit.
- Handhabt Sonderzeichen und Tastenkombinationen, einschließlich Shift und AltGr.
- Läuft im Hintergrund mit einem System-Tray-Icon für einfachen Zugriff.

## Installation

1. **Repository klonen:**
   ```bash
   git clone <repository-url>
   cd TextTyper
   ```

2. **Erforderliche Abhängigkeiten installieren:**
   Stellen Sie sicher, dass Python installiert ist, und führen Sie dann aus:
   ```bash
   pip install -r requirements.txt
   ```

3. **Anwendung starten:**
   ```bash
   python main.py
   ```

4. **Alternativ:**
   - Eine ausführbare `.exe`-Datei, die mit PyInstaller erstellt wurde, ist als Release verfügbar. Diese kann direkt ausgeführt werden, ohne dass Python installiert sein muss.

## Verwendung

1. **Anwendung öffnen:**
   - Die Anwendung startet minimiert im System-Tray. Klicken Sie auf das Tray-Icon, um das Hauptfenster zu öffnen.

2. **Text eingeben:**
   - Geben Sie den Text ein oder fügen Sie ihn in das Textfeld ein, den Sie automatisieren möchten.

3. **Tippgeschwindigkeit einstellen:**
   - Passen Sie die Tippgeschwindigkeit mit der bereitgestellten Steuerung an, um die Verzögerung zwischen den Tastenanschlägen festzulegen.

4. **Tippen starten:**
   - Klicken Sie auf die Schaltfläche "Tippen" und wechseln Sie sofort zum Zielanwendungsfenster, in dem der Text getippt werden soll.

## Tastaturlayout

- Die Anwendung ist für das deutsche Tastaturlayout konfiguriert.
- Sonderzeichen und Tastenkombinationen werden unterstützt, einschließlich:
  - Shift + Zahlentasten für Sonderzeichen wie `!`, `"`, `§` usw.
  - AltGr-Kombinationen für Zeichen wie `@`, `€` und `\\`.

## Danksagungen

- [wxPython](https://wxpython.org/) für das GUI-Framework.
- [keyboard](https://pypi.org/project/keyboard/) für die Simulation von Tastatureingaben. 