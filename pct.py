# pct.py

"""
Description: An example widget using flower_pbar
Author: David COBAC
Date Created: December 15, 2025
Date Modified: December 24, 2025
Version: 1.0
Python Version: 3.13
Dependencies:
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/qtile_alt_widgets
"""

import subprocess

from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base

from .flower_pbar import Flower_pbar


class Pct(base._Widget):

    @staticmethod
    def str2cairorgb(s):
        return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))

    defaults = [(f"button{n}", None, "") for n in range(1, 8)]
    defaults.extend([
        ("center_text", True, ""),
        ("cmd", "awk '/MemTotal/ {t=$2} /MemAvailable/ {a=$2} END"
         " {printf \"%.0f\\n\", ((t-a)/t)*100}' /proc/meminfo", ""),
        ("colormap", None, ""),
        ("colormap_rev", False, ""),
        ("colors", ["ffffff", "ff0000"], ""),
        ("execshell", "/usr/bin/bash", ""),
        ("fpbar_max", 100, ""),
        ("fpbar_min", 0, ""),
        ("fpbar_inradius", None, ""),
        ("fpbar_sct", 10, ""),
        ("hide_text", False, ""),
        ("rev", True, ""),
        ("text", "mem", ""),
        ("text_size", 10, ""),
        ("update_interval", 1, ""),
        ("ymargin", 2, "")
    ])

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self.niveau = 0
        self.draw_method = "fill"
        self._sgn = -1 if self.rev else 1
        self.fpbar_sct = max(2, self.fpbar_sct)
        #
        self.add_callbacks({f"Button{n}": lambda n=n: self._button_handle(n)
                            for n in range(1, 8)})

    def _button_handle(self, n):
        if n == 1:
            self.send_value()
        if bouton := getattr(self, f"button{n}", None):
            bouton(self)

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        #
        if self.center_text:
            self._out_r = 2/3 * self.bar.height - self.ymargin
        else:
            self._out_r = .5 * self.bar.height - self.ymargin
        # options for flower_pbar
        if self.fpbar_inradius:
            self._in_r = self.fpbar_inradius
        else:
            self._in_r = .35 * self.bar.height
        self._inter_r = (self._out_r - self._in_r) / 2
        self._angle_incr = 240 / self.fpbar_sct
        self._sector_size = self._angle_incr * .95
        self._angle_incr *= self._sgn
        self._sector_start = 90 - self._sgn*60 - self._angle_incr/2
        # length
        self.length = self.bar.height + 2*self.padding
        # length1 : text over width limit
        new_length_1 = 0
        # length2 : flower_pbar width > bar.height
        new_length_2 = 0
        if self.text and not self.hide_text:
            ctx = self.drawer.ctx
            ctx.select_font_face(self.font)
            ctx.set_font_size(self.text_size)
            _, self._yb, _, _, _, _ = ctx.text_extents("Qpyj")
            self._xb, _, self._w, self._h, _, _ = ctx.text_extents(self.text)
            if self._w + 2*self.padding >= self.bar.height:
                new_length_1 = round(self._w + 2*self.padding)
        if self.center_text:
            new_length_2 = round(2*self._out_r + 2 * self.padding)
        # the larger the better
        self.length = max(self.length, new_length_1, new_length_2)
        #
        self.timeout_add(self.update_interval, self._tick)

    def send_value(self):
        send_notification("Pct widget", f"{self.text} : {self.niveau}")

    def _tick(self):
        self._update()
        self._timer = self.timeout_add(self.update_interval, self._tick)

    def _update(self):
        res = subprocess.run(self.cmd,
                             capture_output=True,
                             text=True,
                             shell=True,
                             executable=self.execshell)
        self.niveau = float(res.stdout.strip())
        self.draw()

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        ctx.save()
        ctx.translate(self.length / 2, self._out_r + self.ymargin)
        # flower pbar
        Flower_pbar(self.niveau, self.fpbar_max, self.fpbar_min,
                    self.fpbar_sct, self._sector_size,
                    self._sector_start, -self._angle_incr, 1,
                    self._in_r, self._out_r, self._inter_r,
                    self.colors[0], self.colors[1],
                    self.colormap, self.colormap_rev).draw(ctx, self.draw_method)
        ctx.restore()
        # text
        if self.text and not self.hide_text:
            ctx.set_source_rgb(*self.str2cairorgb(self.colors[0]))
            ctx.select_font_face(self.font)
            ctx.set_font_size(self.text_size)
            xtext = (self.length - self._w) / 2
            if self.center_text:
                ytext = 2/3*self.bar.height - self._yb / 4  # - self.ymargin
            else:
                ytext = self.bar.height + self._yb / 4 - self.ymargin
            ctx.move_to(xtext, ytext)
            ctx.show_text(self.text)
        #
        self.draw_at_default_position()

    def finalize(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None
        base._Widget.finalize(self)
