# volume.py

"""
Description: volume widget
Author: David COBAC
Date Created: December 22, 2025
Date Modified: December 22, 2025
Version: 1.0
Python Version: 3.13
Dependencies:
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/my_qtile_widgets
"""

import subprocess

from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base


def str2cairorgb(s):
    return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))


class Rect:
    def __init__(self, w, h, pct, cols, orient):
        self.w = w
        self.h = h
        self.pct = pct
        self.cols = cols
        self.orient = orient

    def draw(self, ctx, mth):
        if self.orient == "h":
            ctx.save()
            ctx.set_source_rgb(*str2cairorgb(self.cols[0]))
            ctx.rectangle(0, 0, self.w, self.h)
            mth()
            ctx.set_source_rgb(*str2cairorgb(self.cols[1]))
            ctx.rectangle(0, 0, self.w * self.pct, self.h)
            mth()
            ctx.restore()
        elif self.orient == "v":
            ctx.save()
            ctx.set_source_rgb(*str2cairorgb(self.cols[0]))
            ctx.rectangle(0, 0, self.w, self.h)
            mth()
            ctx.set_source_rgb(*str2cairorgb(self.cols[1]))
            ctx.rectangle(0, 0, self.w, self.pct * self.h)
            mth()
            ctx.restore()


class Cell:
    def __init__(self, w, h, pct, cols, orient, ncells, gap):
        self.w = w
        self.h = h
        self.pct = pct
        self.ncells = ncells
        self.cols = cols
        self.orient = orient
        self.gap = gap
        if self.orient == "v":
            # self.h < 0
            self.dim_cell = ((abs(self.h) - (self.ncells - 1)*self.gap)
                             / self.ncells)
        elif self.orient == "h":
            self.dim_cell = ((self.w - (self.ncells - 1)*self.gap)
                             / self.ncells)

    def draw(self, ctx, mth):
        n_vol = round(self.pct * self.ncells)
        if self.orient == "h":
            ctx.save()
            # volume
            ctx.set_source_rgb(*str2cairorgb(self.cols[1]))
            for i in range(n_vol):
                ctx.rectangle(i*(self.dim_cell + self.gap), 0,
                              self.dim_cell, self.h)
                mth()
            # fond
            ctx.set_source_rgb(*str2cairorgb(self.cols[0]))
            for i in range(n_vol, self.ncells):
                ctx.rectangle(i*(self.dim_cell + self.gap), 0,
                              self.dim_cell, self.h)
                mth()
            ctx.restore()
        elif self.orient == "v":
            ctx.save()
            
            # volume
            ctx.set_source_rgb(*str2cairorgb(self.cols[1]))
            for i in range(n_vol):
                ctx.rectangle(0, -i*(self.dim_cell + self.gap),
                              self.w, -self.dim_cell)
                mth()
            # fond
            ctx.set_source_rgb(*str2cairorgb(self.cols[0]))
            for i in range(n_vol, self.ncells):
                ctx.rectangle(0, -i*(self.dim_cell + self.gap),
                              self.w, -self.dim_cell)
                mth()
            ctx.restore()


class Volume(base._Widget):
    defaults = [
        ("bar_bg", "cccccc", "bar background"),
        ("bar_length", 40, "bar length ~= widget length"),
        ("bar_width", 10, "bar thickness"),
        ("cellgap", 1, "gap between cells"),
        ("execshell", "/usr/bin/bash", "shell to execute amixer commands"),
        ("ncells", None, "number of cells"),
        ("orient", "v", "orientation v or h"),
        ("step", 1000, "step to inc or dec volume"),
        ("ymargin", 2, "y margin"),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self.mute = False
        self.sv_vol = None
        self.cmd_get = "amixer get Master |grep Left:|cut -d ' ' -f6"
        self.cmd_get_max = "amixer get Master |grep Limits|cut -d ' ' -f7"
        self.cmd_set = "amixer set Master {}"
        res = subprocess.run(self.cmd_get_max,
                             capture_output=True,
                             text=True,
                             shell=True,
                             executable=self.execshell)
        self.max_vol = 1 if not res.stdout.strip() else int(res.stdout.strip())
        self.add_callbacks({"Button1": self.toggle_mute,
                            "Button4": self.inc_volume,
                            "Button5": self.dec_volume})

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        if self.orient == "h":
            self.length = self.bar_length + 2*self.padding
            self.xpos = self.padding
            self.ypos = (self.bar.height - self.bar_width) / 2
            self.dim_barre_totale = self.bar_length
        elif self.orient == "v":
            self.length = self.bar_width + 2*self.padding
            self.xpos = self.padding
            self.ypos = self.bar.height - self.ymargin
            self.dim_barre_totale = self.bar.height - 2*self.ymargin

    def get_volume(self):
        res = subprocess.run(self.cmd_get,
                             capture_output=True,
                             text=True,
                             shell=True,
                             executable=self.execshell)
        return 0 if not res.stdout.strip() else int(res.stdout.strip())

    def toggle_mute(self):
        if self.mute:
            new_vol = self.sv_vol
        else:
            self.sv_vol = self.get_volume()
            new_vol = 0
        res = subprocess.run(self.cmd_set.format(new_vol),
                             capture_output=True,
                             text=True,
                             shell=True,
                             executable=self.execshell)
        self.mute = not self.mute
        self.bar.draw()

    def inc_volume(self):
        self._change_volume(self.step)
        self.bar.draw()

    def dec_volume(self):
        self._change_volume(-self.step)
        self.bar.draw()

    def _change_volume(self, inc):
        cvol = self.get_volume()
        res = subprocess.run(self.cmd_set.format(cvol + inc),
                             capture_output=True,
                             text=True,
                             shell=True,
                             executable=self.execshell)
        if res.stderr != "":
            logger.warning(res)

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        if self.mute:
            vol = self.sv_vol
        else:
            vol = self.get_volume()
        #
        ctx.save()
        ctx.translate(self.xpos, self.ypos)
        ctx.set_line_width(1)
        
        if self.orient == "h":
            L = self.dim_barre_totale
            l = self.bar_width
        elif self.orient == "v":
            L = self.bar_width
            l = -self.dim_barre_totale
        #
        if self.ncells is not None:
            obj = Cell(L, l, vol/self.max_vol, [self.bar_bg, self.foreground],
                       self.orient, self.ncells, self.cellgap)
        else:
            obj = Rect(L, l, vol/self.max_vol, [self.bar_bg, self.foreground],
                       self.orient)
        if self.mute:
            obj.draw(ctx, ctx.stroke)
        else:
            obj.draw(ctx, ctx.fill)
        #
        ctx.restore()
        self.draw_at_default_position()
