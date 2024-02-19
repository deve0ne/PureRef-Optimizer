import argparse
import customtkinter as ctk
from tkinter import filedialog
import PureRef_optimizer

def gui_process_pureref_file(input_file, max_dimension, colors, progress_bar, app):
    args = argparse.Namespace(
        input_file=input_file,
        max_dimension=int(max_dimension),
        colors=int(colors),
        processes=6
    )

    # Define a callback function that updates the progress bar
    def progress_callback(progress_fraction):
        update_progress_bar(progress_bar, progress_fraction, app)

    # Pass the callback function to the process_pureref_file function
    PureRef_optimizer.process_pureref_file(args, progress_callback=progress_callback)

def update_progress_bar(progress_bar, value, app):
    progress_bar.set(value)
    # This ensures the GUI updates in real-time
    app.update_idletasks()

def select_file(label):
    file_path = filedialog.askopenfilename()
    if file_path:
        label.set(file_path)
        
def start_optimization(progress_bar, file_label, max_dimension, colors, app):
    input_file = file_label.get()
    if input_file:
        progress_bar.set(0.0)
        gui_process_pureref_file(input_file, max_dimension.get(), colors.get(), progress_bar, app)
        progress_bar.set(1.0)

def create_gui():
    app = ctk.CTk()
    app.title('PureRef Optimizer')
    app.geometry('400x300')

    ctk.set_appearance_mode("Dark")  # Set the theme to Dark

    file_label = ctk.StringVar(value="Drag and drop or select a PureRef file")
    ctk.CTkLabel(app, textvariable=file_label).pack(pady=10)

    ctk.CTkButton(app, text="Select File", command=lambda: select_file(file_label)).pack(pady=10)

    max_dimension = ctk.CTkSlider(app, from_=512, to=4096, number_of_steps=3)
    max_dimension.set(2048)
    max_dimension.pack(pady=10)

    colors = ctk.CTkSlider(app, from_=128, to=512, number_of_steps=2)
    colors.set(256)
    colors.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(app)
    progress_bar.pack(pady=10)

    ctk.CTkButton(app, text="Optimize", command=lambda: start_optimization(progress_bar, file_label, max_dimension, colors, app)).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    create_gui()