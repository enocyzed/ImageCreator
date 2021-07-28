import os
import sys
import time


# When the package is a pip package, this can be removed
import sys
import pathlib
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
sys.path.append(os.path.dirname(dname))
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
#

def make_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)


def get_fonts():
    with open(os.path.join(assets_directory, "fonts", "_fonts.py"), 'w') as file:
        for root, dirs, files in os.walk(os.path.join(assets_directory, "fonts")):
            for filename in files:
                if filename.endswith(".ttf") or filename.endswith(".otf"):
                    new_root = root.replace(".", "")
                    fullpath = os.path.join(assets_directory, "fonts", new_root, filename)
                    new_filename = filename[:-4].replace('-', '_').replace(' ', '_').replace('.', '_')
                    line = f"{new_filename} = r'{fullpath}'\n"
                    file.write(line)


abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

make_dir("Assets")
make_dir("Assets/fonts")
make_dir("Assets/plugins")
make_dir("CreateConfigurations")
make_dir("CreateConfigurations/created_images")

assets_directory = os.path.abspath("Assets")

get_fonts()
