import json
import string
import yaml
import os


# TODO: create better base templates
base_image = {
             "path": None,
             "size": {"width": 1080, "height": 1080, "keep_aspect_ratio": True},
             "crop": {"x": 0, "y": 0, "width": 1080, "height": 1080, "to_square": False},
             "color": "#554477",
             "enhance": {"brightness": 1.0, "color": 1.0, "contrast": 1.0, "sharpness": 1.0},
             "opacity": 1.0,
             "overlays": {}
         }

overlay_image = {"type": "image", "location": {"posx": 0, "posy": 0, "anchor_center": True},
         "params": {
             "path": "t2.jpg",
             "size": {"width": 400, "height": 400, "keep_aspect_ratio": True},
             "crop": {"x": 0, "y": 0, "width": 400, "height": 400, "to_square": False},
             "color": "#554477",
             "enhance": {"brightness": 1.0, "color": 1.0, "contrast": 1.0, "sharpness": 1.0},
             "opacity": 1.0,
             "overlays": {}
         }}

text = {"type": "text", "location": {"posx": 0, "posy": -80, "anchor_center": True},
        "params": {
            "message": "Lorem ipsum",
            "size": 40,
            "font": "Anton_Regular",
            "color": "#000000"
        }
        }

multiline_text = {"type": "multiline_text", "location": {"posx": 50, "posy": 80, "anchor_center": True},
                  "params": {
                      "message": "Lorem ipsum dolor sit amet consectetur adipisicing elit.",
                      "box_width": 300,
                      "box_height": 300,
                      "size": 40,
                      "font": "Anton_Regular",
                      "color": "#000000",
                      "spacing": 10,
                      "align": "left"
                  }
                  }

global rec

rec = 0


# TODO: make structure better
# TODO: make items deletable
def select():
    global rec
    indent = ""
    overlays = []
    for i in range(rec):
        indent += " ---- "
    rec += 1
    print("\n" + "depth: " + str(rec))
    while True:
        print(indent + "i = image ; t = text ; m = multiline text ; n = none")
        inp = input(indent + "Select overlay: ")
        type_ = inp.lower()
        if type_ == "i":
            overlays.append(select())
        elif type_ in ["t", "m"]:
            overlays.append(type_)
        elif type_ == "n":
            print("")
            break
        else:
            print(indent + "Invalid input\n")

    return overlays


def to_dict(user_selection):
    def iterator(data):
        i = 0
        overlay_data = {}
        for ind in data:
            i += 1
            if isinstance(ind, list):
                sth = overlay_image
                overlay_data[str(i)] = sth
                overlay_data[str(i)]["params"]["overlays"] = json.loads(iterator(ind))

            elif ind == "t":
                sth = text
                overlay_data[str(i)] = sth
            elif ind == "m":
                sth = multiline_text
                overlay_data[str(i)] = sth

        ret = json.dumps(overlay_data, indent=4)
        return ret

    overlays = json.loads(iterator(user_selection))
    base_image["overlays"] = overlays
    return base_image


def file_writer(data, directory=""):
    while True:
        name_inp = input("Choose a filename: ")
        for l in name_inp:
            if l not in "-_.()" + string.ascii_letters + string.digits:
                print("Invalid input\n")
                continue
        break

    while True:
        format_inp = input("Choose a format (y=yaml, j=json): ").lower()
        if format_inp == "y" or format_inp == "yaml" or format_inp == "yml":
            filename = name_inp + ".yaml"

            while True:
                flow = input("Choose flow style (Enter=deafult , n=none , f=full)")
                if flow == "":
                    style = None
                    break
                elif flow == "n":
                    style = False
                    break
                elif flow == "f":
                    style = True
                    break
                else:
                    print("Invalid input\n")

            with open(os.path.join(directory, filename), "w") as f:
                f.write(yaml.dump(data, default_flow_style=style, indent=4, sort_keys=False))
            break

        elif format_inp == "j" or format_inp == "json":
            filename = name_inp + ".json"

            with open(filename, "w") as f:
                f.write(json.dumps(data, indent=4))
            break

        else:
            print("Invalid input\n")
