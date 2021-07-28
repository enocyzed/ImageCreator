from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import pathlib
import time

from ImageCreator.core.make_template import select, to_dict, file_writer
from ImageCreator.core.image_create import safe_create
from ImageCreator.core import assets_directory


abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

config_dir = os.path.join(os.path.dirname(assets_directory), "CreateConfigurations")


def create(path_to_config=None, save_path=None, filename=None, return_image=False):
    if isinstance(path_to_config, str):
        if not os.path.exists(path_to_config):
            p = os.path.join(config_dir, path_to_config)
            if os.path.exists(p+".yml"):
                path_to_config = p+".yml"
            elif os.path.exists(p+".yaml"):
                path_to_config = p+".yaml"
            elif os.path.exists(p+".json"):
                path_to_config = p+".json"

    if save_path is None:
        save_path = os.path.join(config_dir, "created_images")
    if path_to_config is None:
        pathlist = []
        for f in os.listdir(config_dir):
            if f.endswith(".yaml") or f.endswith(".yml") or f.endswith(".json"):
                path = safe_create(os.path.join(config_dir, f), save_path=save_path, save_name=pathlib.Path(f).stem)
                pathlist.append(path)
        return pathlist
    if filename is None:
        filename = pathlib.Path(path_to_config).stem

    path = safe_create(path_to_config, save_path=save_path, save_name=filename, return_image=return_image)
    return path


def select_file():
    file_list = []
    for i in os.listdir(config_dir):
        if i.endswith(".json") or i.endswith(".yml") or i.endswith(".yaml"):
            file_list.append(i)

    print("All available configuration files:\n")
    for k, v in enumerate(file_list):
        print(f"{k}:    {v}")
    while True:
        try:
            num = input("\nPlease enter the number of your desired configuration (nothing=all): ")
            if num == "":
                return None, None
            num = int(num)
        except ValueError:
            print("It has to be a number!")
            continue
        if num not in range(len(file_list)):
            print("Number is not in range of file list!")
            continue
        else:
            break

    return os.path.join(config_dir, file_list[num]), pathlib.Path(file_list[num]).stem


def create_on_press():
    abs_path, filename = select_file()
    print("Process can be stopped with pressing CRTL + C")
    while True:
        try:
            input("Press enter for update... ")
            safe_create(abs_path, save_path=os.path.join(config_dir, "created_images"), save_name=filename)
        except KeyboardInterrupt:
            print("\n=== Create process ended ===\n")
            break


# TODO: implement create on watchdog
def create_on_modified():
    print("Listening for changes...")
    print("Process can be stopped with pressing CRTL + C")

    class MyHandler(FileSystemEventHandler):
        def on_modified(self, event):
            path = event.src_path
            if path.endswith(".yml") or path.endswith(".yaml") or path.endswith(".json"):
                safe_create(
                    event.src_path, save_path=os.path.join(config_dir, "created_images"),
                    save_name=pathlib.Path(event.src_path).stem
                )

            print(f"\n{pathlib.Path(event.src_path).stem} has been modified... ")

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=config_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.1)

    # TODO: make KeyboardInterrupt feature work
    except KeyboardInterrupt:
        observer.stop()
        exit(-1)


def create_template():
    json_ = to_dict(select())
    file_writer(json_, directory=config_dir)
