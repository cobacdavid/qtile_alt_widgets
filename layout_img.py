# layout_img.py

"""
Description: Script to get layout colored icons
Author: David COBAC
Date Created: January 04, 2026
Date Modified: January 04, 2026
Version: 1.0
Python Version: 3.13
Dependencies:
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/qtile_alt_widgets
"""

import os
import re

import libqtile.resources
from PIL import Image


def est_couleur_valide(col):
    return bool(re.fullmatch(r"[0-9a-fA-F]{6}", col))


def path_color_layout(col):
    res_dir = os.path.dirname(libqtile.resources.__file__)
    input_dir = os.path.join(res_dir, "layout-icons")
    #
    if not est_couleur_valide(col):
        return input_dir
    #
    output_dir = os.path.join("/tmp", "layout-img", col)
    os.makedirs(output_dir, exist_ok=True)
    #
    r, g, b = [int(col[i:i+2], 16) for i in (0, 2, 4)]
    #
    for name in os.listdir(input_dir):
        if not name.lower().endswith(".png"):
            continue
        #
        img = Image.open(os.path.join(input_dir, name)).convert("RGBA")
        _, _, _, alpha = img.split()
        #
        col_img = Image.merge("RGBA", (
            Image.new("L", img.size, r),
            Image.new("L", img.size, g),
            Image.new("L", img.size, b),
            alpha
        ))
        #
        try:
            col_img.save(os.path.join(output_dir, name))
        except OSError:
            return input_dir
        #
    return output_dir

if __name__ == "__main__":
    assert (path_color_layout("FF0000")
            == os.path.join("/tmp", "layout-img", "FF0000"))
    assert (path_color_layout("FF000")
            == os.path.join(os.path.dirname(libqtile.resources.__file__),
                            "layout-icons"))
