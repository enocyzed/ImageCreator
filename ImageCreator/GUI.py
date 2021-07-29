import os
import watchdog.events
import watchdog.observers
import yaml

from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import *

from PIL import Image, ImageTk

from ImageCreator.core.image_create import CreatePicture, create_picture, safe_create
from ImageCreator.core.utils import to_json
from ImageCreator.core import assets_directory
from ImageCreator.core.use import create
from ImageCreator.core.make_template import base_image, overlay_image, text, multiline_text

config_dir = os.path.join(os.path.dirname(assets_directory), "CreateConfigurations")
config_path = ""

root = Tk()
root.title("ImageCreator")
root.minsize(370, 250)

image = None


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, file_name):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=[file_name], ignore_directories=True, case_sensitive=False)
    def on_modified(self, event):
        print(">>> modified")
        try:
            refresh_image()
        except Exception as e:
            print(f"( {e} )")


def update_credentials():
    # Update credentials
    global image
    w, h = image.size
    file_size = w * h * 3
    unit = "B"
    if file_size >= 1000000000:
        file_size /= 1000000000
        unit = "GB"
    elif file_size >= 1000000:
        file_size /= 1000000
        unit = "MB"
    elif file_size >= 1000:
        file_size /= 1000
        unit = "KB"
    credentials = f"{os.path.basename(config_path)}   {w}x{h}   {file_size:.2f} {unit}"
    credentials_label.configure(text=credentials)


def add_overlay():
    if not config_path:
        f = filedialog.asksaveasfile(initialdir=config_dir, mode='w', defaultextension=".yaml")
        if not f: return
        yaml.dump(base_image, f, default_flow_style=False, indent=4, sort_keys=False)
        f.close()

        get_config_path(f.name)
        return


    image_synonyms = ["image", "img"]
    text_synonyms = ["text", "txt"]
    multiline_text_synonyms = ["multiline_text", "multiline", "multi", "mtxt"]

    configs = to_json(config_path)

    def rec_loop(dict_):
        for k, v in dict_.items():
            if isinstance(v, dict):
                if k == "overlays":
                    for k_, v_ in v.items():
                        if v_ in image_synonyms:
                            v[k_] = overlay_image
                        elif v_ in text_synonyms:
                            v[k_] = text
                        elif v_ in multiline_text_synonyms:
                            v[k_] = multiline_text

                rec_loop(v)


    rec_loop(configs)
    print(configs)

    with open(config_path, "w") as f:
        yaml.dump(configs, f, default_flow_style=False, indent=4, sort_keys=False)


def image_show(image_, max_width=500, max_height=500):
    root.minsize(max_width, max_height+60)
    root.geometry(f"{max_width+20}x{max_height+60}")
    opening = CreatePicture().resize_img(image_, max_width, max_height)
    im = ImageTk.PhotoImage(opening)
    image_label.configure(image=im)
    image_label.image = im
    return im


def refresh_image():
    global config_path
    global image
    image = create(config_path, return_image=True)
    image_show(image)


def toggle_stay_on_top():
    root.attributes('-topmost', on_top.get())
    root.update()



observer = None

def toggle_auto_refresh():
    global config_path
    global observer
    print(config_dir, os.path.basename(config_path))
    

    if auto_refresh_value.get():
        observer = watchdog.observers.Observer()
        event_handler = Handler(os.path.basename(config_path)) 
        observer.schedule(event_handler, path=config_dir, recursive=False)

        observer.start()

    else:
        observer.stop()
        observer.join()
        observer = None


def get_config_path(path_=None):
    global config_path
    if path_:
        config_path = path_
    else:
        config_path = filedialog.askopenfilename(initialdir=config_dir, title="Select a File", filetypes=(
            ("Configuration Files", "*.yml *.yaml *.json"), ("All Files", "*.*")))
    if not config_path: return
    add_overlay_button.configure(text="Add Overlay")
    refresh_image()
    update_credentials()



on_top = BooleanVar()
auto_refresh_value = BooleanVar()

options_frame = ttk.Frame(root)
credentials_label = ttk.Label(root)
stay_on_top = ttk.Checkbutton(options_frame, variable=on_top, command=toggle_stay_on_top, text="Stay on top")
auto_refresh = ttk.Checkbutton(options_frame, variable=auto_refresh_value, command=toggle_auto_refresh, text="Auto refresh")
get_path_button = ttk.Button(options_frame, command=get_config_path, text="Select file")
refresh_image_button = ttk.Button(options_frame, command=lambda: refresh_image(), text="Refresh")
add_overlay_button = ttk.Button(options_frame, command=lambda: add_overlay(), text="Add File")

image_label = ttk.Label(root)


options_frame.place(anchor=N, relx=0.5)

credentials_label.place(anchor=S, rely=1, relx=0.5)
get_path_button.grid(row=0, column=1, padx=5, rowspan=2)
stay_on_top.grid(row=0, column=2, padx=5, sticky="W")
auto_refresh.grid(row=1, column=2, padx=5, sticky="W")
refresh_image_button.grid(row=0, column=3, padx=5, rowspan=2)
add_overlay_button.grid(row=0, column=4, padx=5, rowspan=2)
image_label.place(anchor=S, relx=0.5, rely=1, y=-15)


root.mainloop()