
I write a lot of notes and I wanted a really simple notes app with limited fluff, so I made this one.

📝 My Simple Notes App
Hey! This is just a simple little notes app I built using Python and Tkinter. I wanted something minimal where I could quickly jot down stuff, save it, and not get distracted by a bunch of extra features I don’t use. It’s got just enough to be useful and not enough to get annoying.
Had to do some reading online as tkinter was unfamiliar.

✨ Features
Basic editing: New, Open, Save, Save As / the usual suspects.

Dark mode toggle (because I have myopia and bright shit stings *hisses in goblin*).

Keyboard shortcuts:

Ctrl + N → New file

Ctrl + O → Open file

Ctrl + S → Save

Ctrl + Q → Quit

Ctrl + D → Toggle dark mode

💡 How it works
It's built with Tkinter and uses a Text widget inside a resizable window. I added a menu bar for the main file operation and a little View menu with a toggle for dark mode. When you switch between light and dark themes, the app saves your preference in a simple JSON file in your home directory (~/.notes_app_settings.json), so it'll remember it next time you open it.

The app also tries to be polite (if you have unsaved changes and try to quit or open another file, it’ll ask if you want to save first.)

🛠 How to run it
Make sure you’ve got Python 3 installed, then just run it with:

bash
Copy
Edit
python notes_app.py
(Or whatever you named the file.)

No dependencies beyond the standard library.

🗂 File Handling
Files are saved as plain .txt. Nothing fancy, just readable text. You can open and save anything, although I kept the default to .txt because it's universal.

🌗 Dark Mode
Dark mode is super basic but effective, it just changes the background and text colors of the window and text area. You can toggle it with Ctrl+D or through the menu. Your preference is saved, so it sticks around after you close the app.

⚠️ Limitations
This is super minimal on purpose:

No rich text formatting

No auto-save (yet)

Only one note at a time

Doesn’t remember file history or recent files

Maybe I'll add more stuff later, but for now, it does what I need.
