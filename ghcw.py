# ghcw.py

"""
Description: A Github contribution widget for Qtile
Author: David COBAC
Date Created: December 6, 2025
Date Modified: December 22, 2025
Version: 1.3
Python Version: 3.13
Dependencies: aiohttp, colormaps
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/qtile_alt_widgets
"""

import asyncio
import webbrowser
from datetime import datetime, timedelta

import aiohttp
import colormaps as cmaps
from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base


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


class Ghcw(base._Widget):
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

    THEMES = {'ghcw_lgt': [[1 - (.25*i)**.5]*3 for i in range(5)],
              'ghcw_drk': [[(.25*i)**.5]*3 for i in range(5)],
              'ghcw_gho': [(.9, .9, .9),
                           (.77, .89, .55),
                           (.48, .79, .44),
                           (.14, .60, .23),
                           (.1, .38, .15)],
              'ghcw_ghd': [(.09, .11, .13),
                           (0, .22, .13),
                           (0, .37, .18),
                           (.06, .60, .24),
                           (.15, .84, .27)],
              'ghcw_bdx': [(.97, .91, .88),
                           (.58, .48, .44),
                           (.43, .20, .11),
                           (.20, .21, .18),
                           (.13, .03, .04)],
              'ghcw_red': [(.95, .82, .68),
                           (.93, .62, .53),
                           (.94, .23, .24),
                           (.63, .05, .09),
                           (.21, .02, .03)],
              'ghcw_blu': [(.85, .90, .95),
                           (.16, .42, .63),
                           (.67, .78, .66),
                           (.48, .61, .39),
                           (.33, .37, .25)],
              }

    defaults = [
        ("colors", None, ""),
        ("empty_cell_color", None, ""),
        ("gap", None, ""),
        ("idgithub", "cobacdavid", ""),
        ("revcolors", False, ""),
        ("nweeks", 52, ""),
        ("theme", "ghcw_gho", "")
    ]

    @staticmethod
    def cmp2theme(cmap_name):
        col = getattr(cmaps, cmap_name).discrete(5)
        return [tuple(map(float, col(i)))[:-1] for i in range(5)]

    @staticmethod
    def str2cairorgb(s):
        return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))

    def __init__(self, token, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self.token = token
        self.ghcw_themes = list(self.THEMES.keys())
        self.ghcw_themes_i = 0
        #
        if not self.token:
            logger.warning("You must provide a valid Github Token.")
            exit
        self.add_callbacks({"Button1": self.to_user_webpage,
                            "Button3": self.switch_theme})

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        # async task to API
        self._tab_donnees = None
        asyncio.create_task(self.async_init())

    def to_user_webpage(self):
        url = f"https://github.com/{self.idgithub}"
        webbrowser.open(url)

    def switch_theme(self):
        self.theme = self.ghcw_themes[self.ghcw_themes_i]
        self.ghcw_themes_i = (self.ghcw_themes_i + 1) % len(self.ghcw_themes)
        self.draw()

    async def async_init(self):
        """Partie asynchrone de l'init."""
        data = await self.fetch_contribs()
        self._tab_donnees = data
        # let qtile decides
        self.bar.draw()

    async def fetch_contribs(self):
        today = datetime.today()
        past = today - timedelta(days=7 * self.nweeks)
        # begin from past
        n_req = self.nweeks // 52 + (0 if self.nweeks % 52 == 0 else 1)
        from_date = past
        to_date = from_date + timedelta(days=7 * ((self.nweeks % 52) or 52))
        weeks = list()
        for n in range(n_req):
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.github.com/graphql",
                                        json={"query": self.QUERY,
                                              "variables":
                                              {'login': self.idgithub,
                                               'from': from_date.isoformat(),
                                               'to': to_date.isoformat()}},
                                        headers={"Authorization":
                                                 f"Bearer {self.token}",
                                                 "Content-Type":
                                                 "application/json"}
                                        ) as resp:
                    res = await resp.json()
                    weeks.extend(res["data"]["user"]["contributionsCollection"]
                                 ["contributionCalendar"]["weeks"])
            from_date = to_date + timedelta(days=1)
            to_date = from_date + timedelta(days=7*52 - 1)
        #
        tab_donnees = []
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
        lgth = self.nweeks*step - self.gap
        hght = 7*self.dim + 8*self.gap

        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        ctx.translate(self.padding, (self.bar.height - hght) / 2)

        if not self.colors:
            if self.theme in self.THEMES:
                colors = self.THEMES[self.theme]
            else:
                try:
                    colors = self.cmp2theme(self.theme)
                except:
                    logger.warning(f"Error with {self.theme} theme, "
                                   "switch to default theme")
                    colors = self.THEMES[Ghcw.defaults[6][1]]
        else:
            colors = list(map(self.str2cairorgb, self.colors))

        if self.revcolors:
            colors = colors[::-1]

        if self.empty_cell_color:
            colors[0] = self.str2cairorgb(self.empty_cell_color)

        for col in range(self.nweeks):
            for lig in range(7):
                intensity = self._tab_donnees[col * 7 + lig][1]
                icolor = min(4, int(intensity))
                couleur = colors[icolor]
                Contrib_day(col*step,
                            self.gap + lig*step,
                            self.dim, couleur).draw(ctx)

        self.length = lgth + 2*self.padding
        self.draw_at_default_position()
