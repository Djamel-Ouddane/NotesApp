import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import json
import os

class NotesApp:
    def __init__(self, master):
        self.master = master
        self.filename = None
        self.dark_mode = self._load_theme_preference()
        self._setup_ui()
        self._apply_theme()
        
    def _setup_ui(self):
        """Initialize and configure the UI components"""
        # Configure the main window
        self.master.title("Notes App")
        self.master.geometry("800x600")
        
        # Configure text widget with scrollbar
        self._setup_text_area()
        
        # Configure menu
        self._setup_menu()
        
    def _setup_text_area(self):
        """Create and configure the text area with scrollbar"""
        # Create frame to hold text widget and scrollbar
        self.text_frame = tk.Frame(self.master)
        self.text_frame.pack(fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.text_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Configure text widget
        self.notes_text = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Arial", 11),
            insertbackground="black"  # Cursor color
        )
        self.notes_text.pack(side="left", fill="both", expand=True)
        
        # Connect scrollbar
        self.notes_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.notes_text.yview)
        
    def _setup_menu(self):
        """Create and configure the menu bar"""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_notes, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_notes_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit_app, accelerator="Ctrl+Q")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(
            label="Dark Mode",
            command=self.toggle_theme,
            accelerator="Ctrl+D",
            variable=tk.BooleanVar(value=self.dark_mode)
        )
        
        # Bind keyboard shortcuts
        self.master.bind("<Control-n>", lambda e: self.new_file())
        self.master.bind("<Control-o>", lambda e: self.open_file())
        self.master.bind("<Control-s>", lambda e: self.save_notes())
        self.master.bind("<Control-q>", lambda e: self.quit_app())
        self.master.bind("<Control-d>", lambda e: self.toggle_theme())
        
    def toggle_theme(self, event=None):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self._apply_theme()
        self._save_theme_preference()
        
    def _apply_theme(self):
        """Apply the current theme to all widgets"""
        if self.dark_mode:
            bg_color = "#2d2d2d"
            fg_color = "#ffffff"
            select_bg = "#404040"
            select_fg = "#ffffff"
            cursor_color = "#ffffff"
        else:
            bg_color = "#ffffff"
            fg_color = "#000000"
            select_bg = "#0078d7"
            select_fg = "#ffffff"
            cursor_color = "#000000"
            
        # Apply theme to main window and frame
        self.master.configure(bg=bg_color)
        self.text_frame.configure(bg=bg_color)
        
        # Apply theme to text widget
        self.notes_text.configure(
            bg=bg_color,
            fg=fg_color,
            selectbackground=select_bg,
            selectforeground=select_fg,
            insertbackground=cursor_color  # Cursor color
        )
        
    def _get_settings_path(self):
        """Get the path to the settings file"""
        return Path.home() / ".notes_app_settings.json"
        
    def _load_theme_preference(self):
        """Load the theme setting from a file; default to light mode if not found or error occurs."""
        settings_path = self._get_settings_path()
        if not settings_path.exists():
            # No settings file found, return default (light mode)
            return False
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            # Return the saved preference, or False if it's not set
            return settings.get('dark_mode', False)
        except (json.JSONDecodeError, OSError) as err:
            # If reading fails, print a warning and use default
            print(f"Warning: Failed to load theme settings ({err}), using default.")
            return False
        
    def _save_theme_preference(self):
        """Save the current theme setting to the settings file. Show an error if saving fails."""
        settings_path = self._get_settings_path()
        settings = {'dark_mode': self.dark_mode}
        try:
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)  # Pretty-print JSON for easy reading/editing
        except OSError as err:
            # Show a clear error message if saving doesn't work
            messagebox.showerror(
                "Save Error",
                f"Could not save theme preference:\n{err}"
            )
        
    def new_file(self):
        """Create a new empty note"""
        if self._check_save_needed():
            self.notes_text.delete("1.0", "end")
            self.filename = None
            self.master.title("Notes App")
            
    def open_file(self):
        """Open and load a text file"""
        if self._check_save_needed():
            filename = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        self.notes_text.delete("1.0", "end")
                        self.notes_text.insert("1.0", f.read())
                    self.filename = filename
                    self._update_title()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file: {str(e)}")
                    
    def save_notes(self, event=None):
        """Save the current notes to file"""
        if not self.filename:
            return self.save_notes_as()
        return self._save_file(self.filename)
    
    def save_notes_as(self):
        """Save the notes to a new file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            success = self._save_file(filename)
            if success:
                self.filename = filename
                self._update_title()
            return success
        return False
            
    def _save_file(self, filename):
        """Helper method to save content to a file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.notes_text.get("1.0", "end-1c"))
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
            return False
            
    def _check_save_needed(self):
        """Check if current notes need saving before proceeding"""
        if not self.notes_text.edit_modified():
            return True
            
        response = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Do you want to save your changes?"
        )
        
        if response is None:  # Cancel
            return False
        if response:  # Yes
            return self.save_notes()
        return True  # No
            
    def _update_title(self):
        """Update the window title with the current filename"""
        title = "Notes App"
        if self.filename:
            title += f" - {Path(self.filename).name}"
        self.master.title(title)
            
    def quit_app(self, event=None):
        """Quit the application after checking for unsaved changes"""
        if self._check_save_needed():
            self.master.quit()

def main():
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()