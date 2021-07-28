import os
import traceback
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
import time
import sys

from ImageCreator.core.utils import *
from ImageCreator.core import assets_directory

sys.path.append(assets_directory)

from Assets.fonts._fonts import *


class CreatePicture:
    def __init__(self, attrs=None):
        self.picture = None
        self.attrs = attrs

    def open_image(self, path_):
        pic = Image.open(path_)
        rgba_pic = pic.convert('RGBA')
        self.picture = rgba_pic
        return rgba_pic

    def set_background(self, background_picture=None, color=None, size=None):
        bgp = background_picture
        if bgp is None:
            self.picture = Image.new('RGBA', size, color)
        elif size is None:
            self.picture = bgp
        elif color is None:
            self.picture = bgp.resize(size, Image.ANTIALIAS)
        return self.picture

    def crop_(self, width=0, height=0, x=0, y=0, pic=None, to_square=False):
        if pic is None:
            im = self.picture
        else:
            im = pic

        if width == 0 or width is None:
            width = im.size[0]
        if height == 0 or height is None:
            height = im.size[1]

        if not to_square:
            cropped_image = im.crop((x, y, width, height))
        else:
            if width > height:
                crop = int((width - height) / 2)
                cropped_image = im.crop((crop + x, 0 + y, width - crop + x, height + y))  # (x, y, width, height)
            elif width < height:
                crop = int((height - width) / 2)
                cropped_image = im.crop((0 + x, crop + y, width + x, height - crop + y))
            else:
                cropped_image = im

        self.picture = cropped_image
        return cropped_image

    def overlay_images(self, bgi=None, fgi=None, posx=0, posy=0, anchor_center=True):
        if isinstance(fgi, str):
            overlay_ = Image.open(fgi)
            overlay = overlay_.convert('RGBA')
        else:
            overlay = fgi.convert('RGBA')

        if bgi is None:
            bg = self.picture
        else:
            if isinstance(bgi, str):
                bgi = Image.open(bgi)
            bg = bgi.convert("RGBA")

        comp_img = Image.new('RGBA', bg.size, (0, 0, 0, 0))

        if anchor_center:
            position = ((comp_img.width - overlay.width) // 2 + posx, (comp_img.height - overlay.height) // 2 + posy)
        else:
            position = (posx, posy)

        comp_img.paste(bg, (0, 0))  # ((comp_img.width - bg.width) // 2, (comp_img.height - bg.height) // 2))
        comp_img.paste(overlay, position, mask=overlay)

        if bgi is None:
            self.picture = comp_img

        return comp_img

    def resize_img(self, im=None, width=None, height=None, keep_aspect_ratio=True):
        if im is None:
            image = self.picture
        elif isinstance(im, str):
            image = Image.open(im)
        else:
            image = im

        width = width
        height = height

        if keep_aspect_ratio and width and height:
            w, h = image.size
            if w < h:
                height = None
            else:
                width = None

        if (width is None) and (height is None):
            output_img = image
        elif height is None:
            wpercent = (width / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            output_img = image.resize((width, hsize), Image.ANTIALIAS)
        elif width is None:
            hpercent = (height / float(image.size[1]))
            wsize = int((float(image.size[0]) * float(hpercent)))
            output_img = image.resize((wsize, height), Image.ANTIALIAS)

        elif keep_aspect_ratio:
            image.thumbnail((width, height))
            output_img = image
        else:
            output_img = image.resize((width, height), Image.ANTIALIAS)

        if im is None:
            self.picture = output_img
        return output_img

    def add_text(
            self, message, size, font=None, posx=0, posy=0, color=(255, 255, 255, 255),
            image=None, anchor_center=True, **kwargs
    ):
        if image is None:
            txt_image = self.picture
        else:
            txt_image = image

        if message is None:
            return

        if isinstance(color, dict):
            rgba_tuple = (color.get("r", 255), color.get("g", 255), color.get("b", 255), color.get("a", 255))
            color = rgba_tuple

        if isinstance(font, str):
            if not font.endswith(".ttf"):
                font = eval(font)

        txt = Image.new("RGBA", txt_image.size, (255, 255, 255, 0))
        size_ = size
        while True:
            if font is None:
                fnt = ImageFont.load_default()
            elif font.endswith(".ttf"):
                fnt = ImageFont.truetype(font, size_)
            elif font.endswith(".otf"):
                fnt = ImageFont.truetype(font, size_)
            else:
                fnt = ImageFont.load_default()

            d = ImageDraw.Draw(txt)

            wi, he = (txt_image.size[0], txt_image.size[1])
            w, h = d.textsize(message, font=fnt)

            if w > 1050:
                size_ = size_ - 5   # higher = faster but more inaccurate ; lower = slower but more accurate
            else:
                break

        if anchor_center:
            d.text(((wi - w) / 2 + posx, (he - h) / 2 + posy), message, font=fnt, fill=color, **kwargs)
        else:
            d.text((posx, posy), message, font=fnt, fill=color, **kwargs)
        img_with_text = Image.alpha_composite(txt_image, txt)

        if image is None:
            self.picture = img_with_text
        return img_with_text

    def add_multiline_text(
            self, message, box_width, box_height=5000, size=30, font=None, posx=0, posy=0,
            color=(255, 255, 255), image=None, spacing=10, align="left", anchor_center=True, **kwargs
    ):
        if image is None:
            txt_image = self.picture
        else:
            txt_image = image

        if isinstance(color, dict):
            rgba_tuple = (color.get("r", 255), color.get("g", 255), color.get("b", 255), color.get("a", 255))
            color = rgba_tuple

        if isinstance(font, str):
            if not font.endswith(".ttf"):
                font = eval(font)

        txt = Image.new("RGBA", txt_image.size, (255, 255, 255, 0))
        size_ = size
        while True:
            if font is None:
                fnt = ImageFont.load_default()
            elif font.endswith(".ttf"):
                fnt = ImageFont.truetype(font, size_)
            elif font.endswith(".otf"):
                fnt = ImageFont.truetype(font, size_)
            else:
                fnt = ImageFont.load_default()

            d = ImageDraw.Draw(txt)

            word_list = message.split(' ')
            size_list = []
            bias = 0
            for i in word_list:
                w, h = d.textsize(i + ' ', font=fnt)
                size_list.append(w)

            if ':' in message:
                for i in range(len(word_list)):
                    if ':' in word_list[i]:
                        word_list[i + 1] = '\n' + word_list[i + 1]
                        bias = i

            colon_pos = bias
            for i in range(colon_pos, len(word_list)):
                if sum(size_list[bias:i + 1]) > box_width:
                    word_list[i] = '\n' + word_list[i]
                    bias = i
            formatted_text = ' '.join(word_list)

            wid, hei = d.multiline_textsize(formatted_text, font=fnt, spacing=spacing)
            if hei > box_height or wid > box_width:
                size_ -= 5  # higher = faster but more inaccurate ; lower = slower but more accurate
            else:
                break

        w, h = d.multiline_textsize(formatted_text, font=fnt, spacing=spacing)
        wi, he = (txt_image.size[0], txt_image.size[1])
        if anchor_center:
            d.multiline_text(((wi - w) / 2 + posx, (he - h) / 2 + posy), formatted_text, font=fnt, fill=color,
                             spacing=spacing, align=align, **kwargs)
        else:
            d.multiline_text((posx, posy), formatted_text, font=fnt, fill=color,
                             spacing=spacing, align=align, **kwargs)

        img_with_text = Image.alpha_composite(txt_image, txt)

        if image is None:
            self.picture = img_with_text
        return img_with_text

    def enhancer(self, image=None, brightness=1.0, color=1.0, contrast=1.0, sharpness=1.0):
        if image is None:
            img = self.picture
        elif isinstance(image, str):
            img = Image.open(image)
        else:
            img = image
        if brightness != 1.0:
            img = ImageEnhance.Brightness(img).enhance(brightness)  # 0.0 = black image ; 1.0 = original image
        if color != 1.0:
            img = ImageEnhance.Color(img).enhance(color)  # 0.0 = black and white image ; 1.0 = original image
        if contrast != 1.0:
            img = ImageEnhance.Contrast(img).enhance(contrast)  # 0.0 = solid grey image ; 1.0 = original image
        if sharpness != 1.0:
            img = ImageEnhance.Sharpness(img).enhance(sharpness)  # 0.0 = blurred ; 2.0 = sharpened

        if image is None:
            self.picture = img
        return img


example_params = {
    "path": "t1.jpg",
    "size": {"width": 1080, "height": 1080, "keep_aspect_ratio": True},
    "crop": {"x": 200, "y": 200, "width": 0, "height": 0, "to_square": True},
    "color": "#554477",
    "enhance": {"brightness": 1.0, "color": 1.0, "contrast": 1.0, "sharpness": 1.0},
    "opacity": 1.0,
    "overlays": {
        "1": {"type": "image", "location": {"posx": -300, "posy": -200, "anchor_center": True},
              "params": {
                  # "path": "t2.jpg",
                  "size": {"width": 200, "height": 200, "keep_aspect_ratio": True},
                  "crop": {"x": 0, "y": 0, "width": 60, "height": 70, "to_square": False},
                  "color": "#554477",
                  "enhance": {"brightness": 1.0, "color": 1.0, "contrast": 1.0, "sharpness": 1.0},
                  "opacity": 0.7
              }
              },
        "2": {"type": "text", "location": {"posx": 0, "posy": 0, "anchor_center": True},
              "params": {
                  "message": {"plugin": "get_timestamp", "kwargs": {"number": 400}},
                  "size": 70,
                  "font": "Anton_Regular",
                  "color": "#ffffff"
              }
              },
        "3": {"type": "multiline_text", "location": {"posx": 0, "posy": 100, "anchor_center": True},
              "params": {
                  "message": "Lorem ipsum dolor",
                  "box_width": 300,
                  "box_height": 300,
                  "size": 40,
                  "font": "Anton_Regular",
                  "color": "#eeee77",
                  "spacing": 10,
                  "align": "left"
              }
              }
    }
}


def create_picture(parameters, save_path=None, save_name=None, return_image=False):

    if isinstance(parameters, str):
        if os.path.exists(parameters):
            parameters = to_json(parameters)

    def image_handler(parameters_):

        img_dict = dict_iterator(parameters_, os.path.join(assets_directory, 'plugins'))

        create = CreatePicture(img_dict)

        path_ = img_dict.get("path", None)
        size_ = img_dict.get("size", None)
        crop_ = img_dict.get("crop", None)
        color_ = img_dict.get("color", None)
        enhance_ = img_dict.get("enhance", None)
        opacity_ = img_dict.get("opacity", None)
        overlays_ = img_dict.get("overlays", None)

        if path_ is not None:
            try:
                create.open_image(path_)
            except FileNotFoundError:
                filepath = os.path.join(assets_directory, path_)
                create.open_image(filepath)
            if size_ is not None: create.resize_img(**size_)
            # Color of image
            if color_ is not None: create.overlay_images(
                fgi=Image.new("RGBA", create.picture.size, color_))
        elif size_ is not None:
            size = (size_.get("width", 1), size_.get("height", 1))
            create.set_background(color=color_, size=size)

        if crop_ is not None:
            create.crop_(**crop_)

        if opacity_ is not None:
            create.picture.putalpha(int(255 * float(opacity_)))

        if enhance_ is not None:
            create.enhancer(**enhance_)

        if overlays_ is not None:
            overlay_items = overlays_.items()
            for index, overlay in overlay_items:
                if isinstance(overlay, str): continue
                overlay_type = overlay.get("type", None)
                if overlay_type == "image":
                    create.overlay_images(
                        fgi=image_handler(overlay["params"]), **overlay["location"])
                elif overlay_type == "text":
                    if overlay.get("box_width") or overlay.get("box_height") or overlay.get("spacing") or overlay.get("align"):
                        # if true text is multiline
                        params_ = {}
                        for i, v in overlay["params"].items():
                            params_[i] = v
                        create.add_multiline_text(**params_, **overlay["location"])
                    else:
                        params_ = {}
                        for i, v in overlay["params"].items():
                            params_[i] = v
                        create.add_text(**params_, **overlay["location"])
                elif overlay_type == "multiline_text":
                    params_ = {}
                    for i, v in overlay["params"].items():
                        params_[i] = v
                    create.add_multiline_text(**params_, **overlay["location"])
        return create.picture

    img_done = image_handler(parameters)
    if save_name:
        if save_name.endswith(".png"):
            name = save_name
        else:
            name = save_name + ".png"
    else:
        name = str(time.time()).split(".")[0] + ".png"

    if save_path is not None:
        try:
            path = os.path.join(save_path, name)
            with open(path, "w"):
                img_done.save(path, "PNG")
        except Exception as e:
            print(e)

    if return_image: return img_done
    else: return path



def safe_create(parameters, save_path=None, save_name=None, return_image=False):
    try:
        path = create_picture(parameters, save_path, save_name, return_image)
        return path
    except KeyboardInterrupt:
        exit(-1)
    except Exception as e:
        traceback.print_exc()
        print(e)
