# matrix.py

"""
Description: A generic widget to display numbers [0-100]
Author: David COBAC
Date Created: December 17, 2025
Date Modified: December 17, 2025
Version: 1.0
Python Version: 3.13
Dependencies: libqtile
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/my_qtile_widgets
"""

import random
import subprocess

from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base


def str2cairorgb(s):
    return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))


class Carre:
    def __init__(self, x, y, dim):
        self.x = x
        self.y = y
        self.dim = dim
        self._couleur = None

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self, c):
        self._couleur = c

    def draw(self, ctx):
        ctx.save()
        ctx.translate(self.x, self.y)
        ctx.rectangle(0, 0, self.dim, self.dim)
        ctx.set_source_rgb(*self.couleur)
        ctx.fill()
        ctx.restore()


class Matrix(base._Widget):
    defaults = [("inmargin", 2, "inner margin"),
                ("update_interval", 300, "300s"),
                ("cmd", r"echo $(( RANDOM % 101 ))", "shell command to execute"),
                ("execshell", "/usr/bin/bash", "shell to use"),
                ("pyfunc", None, "python function returning a number [0-100]")]

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        self.length = self.bar.height
        self.dim = (self.bar.height - 2*self.inmargin) / 10
        self.value = None
        self.sqarray = [[Carre(col*self.dim, lig*self.dim, self.dim-1)
                         for col in range(10)] for lig in range(10)]
        self.flatsqarray = sum(self.sqarray, [])
        random.shuffle(self.flatsqarray)
        self._update()
        self.timeout_add(self.update_interval, self._tick)

    def _tick(self):
        self._update()
        self.timeout_add(self.update_interval, self._tick)

    def _update(self):
        if self.pyfunc is None:
            res = subprocess.run(self.cmd,
                                 shell=True,
                                 capture_output=True,
                                 executable=self.execshell,
                                 text=True)
            self.value = res.stdout.strip()
        else:
            self.value = self.pyfunc()
        # logger.warning(self.value)
        self.bar.draw()

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        if self.value is not None:
            ctx = self.drawer.ctx
            ctx.translate(self.inmargin, self.inmargin)
            for i in range(int(self.value)):
                self.flatsqarray[i].couleur = str2cairorgb(self.foreground)
                self.flatsqarray[i].draw(ctx)
        self.draw_at_default_position()
