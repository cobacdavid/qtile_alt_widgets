# ghcw.py

"""
Description: A Github contribution widget for Qtile
Author: David COBAC
Date Created: December 6, 2025
Date Modified: December 13, 2025
Version: 1.1
Python Version: 3.13
Dependencies: aiohttp, libqtile
License: GNU GPL Version 3
"""

import asyncio
import webbrowser
from datetime import datetime, timedelta

import aiohttp
from libqtile.log_utils import logger
from libqtile.widget import base

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


class Contrib_day:
    def __init__(self, x, y, dim, couleur):
        self.x = x
        self.y = y
        self.dim = dim
        self.couleur = couleur

    def draw(self, ctx):
        ctx.save()
        ctx.translate(self.x, self.y)
        ctx.rectangle(0, 0, self.dim, self.dim)
        ctx.set_source_rgb(*self.couleur)
        ctx.fill()
        ctx.restore()


class Ghcw(base._Widget, base.MarginMixin):
    defaults = [
        ("idgithub", "cobacdavid", ""),
        ("gap", None, ""),
        ("nweeks", 52, ""),
        ("colors",
         [(.1, .1, .1)] + [(0, .2*i, 0) for i in range(1, 6)],
         "")
    ]

    def __init__(self, token, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self.token = token
        #
        if not self.token:
            logger.warning("You must provide a valid Github Token.")
            exit
        # async task to API
        self._tab_donnees = None
        asyncio.create_task(self.async_init())
        self.add_callbacks({"Button1": self.to_user_webpage})

    def to_user_webpage(self):
        url = f"https://github.com/{self.idgithub}"
        webbrowser.open(url)

    async def async_init(self):
        """Partie asynchrone de l'init."""
        data = await self.fetch_contribs()
        self._tab_donnees = data
        # draw widget and update bar
        self.draw()
        self.bar.draw()

    async def fetch_contribs(self):
        today = datetime.today()
        past = today - timedelta(days=7 * self.nweeks)
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.github.com/graphql",
                                    json={"query": QUERY,
                                          "variables":
                                          {'login': self.idgithub,
                                           'from': past.isoformat(),
                                           'to': today.isoformat()}},
                                    headers={"Authorization":
                                             f"Bearer {self.token}",
                                             "Content-Type":
                                             "application/json"}
                                    ) as resp:
                res = await resp.json()

        tab_donnees = []
        weeks = (res["data"]["user"]["contributionsCollection"]
                 ["contributionCalendar"]["weeks"])
        for w in weeks:
            for day in w["contributionDays"]:
                tab_donnees.append((day["date"], day["contributionCount"]))
        # append empty days to align week
        missing = 6 - today.weekday()
        for k in range(missing):
            tab_donnees.append(((today + timedelta(days=k+1)).isoformat()[:10],
                                0)
                               )
        return tab_donnees[-7 * self.nweeks:]

    def draw(self):
        if self._tab_donnees is None:
            # no data
            self.drawer.clear(self.background or self.bar.background)
            self.length = 0
            self.draw_at_default_position()
            return

        # no gap is provided, search for the "best" gap value
        if self.gap is None:
            # process to improve
            sol = (float('inf'), None)
            for g in range(1, 10):
                reste = self.bar.height - 8 * g
                if reste % 7 == 0 and reste // 7 > 1:
                    sol = (0, g)
                    break
                elif reste < sol[0] and reste // 7 > 1:
                    sol = (reste, g)
            self.gap = sol[1] or 0
            logger.warning("Considering your bar height, "
                           f"widget ghcw gap's choice is {self.gap}"
                           "\nYou can force a different value "
                           "using 'gap' option.")

        self.dim = (self.bar.height - 8 * self.gap) // 7
        step = self.dim + self.gap
        lgth = self.nweeks*step + self.gap
        hght = 7*self.dim + 8*self.gap

        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        ctx.translate(0, (self.bar.height - hght) / 2)

        for col in range(self.nweeks):
            for lig in range(7):
                intensity = self._tab_donnees[col * 7 + lig][1]
                couleur = self.colors[min(5, int(intensity))]
                Contrib_day(col*step,
                            self.gap + lig*step,
                            self.dim, couleur).draw(ctx)

        self.length = lgth
        self.draw_at_default_position()
