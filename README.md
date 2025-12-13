# My Qtile Widgets

## License

[GNU/GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Github Contribution Widget

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/ghcw.png?raw=true" width=50% />

### Install

The `Ghcw` widget is in the `ghcw.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).

You will need the  `aiohttp` library : `pip install aiohttp`.

You have to get a **token** from the official github site. It's an easy task (via *settings* and *developer settings* menus), I recommand to create a new token for just that widget purpose. You'll need a classic token and the `read:user` permission.

### Usage
For example, in your `config.py` :

```python
frow widgets import ghcw  # if you put ghcw.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    ghcw.Ghcw("YOUR GITHUB TOKEN", idgithub="torvalds"),
    ...
]
...
```
### Options

Unlike original Github diagram, **the week begins on Monday**.

Currently 6 options:

 - `colors`: a five RGB colors tab using `(0, 0, 0)` for black and `(1, 1, 1)` for white, thus `(.5, .5, .5)` is midgrey. Default is `None` as default config uses a `theme` default.
 - `empty_cell_color`: RGB color for 0 contrib. Useful to set according to qtile bar background. Default is `None` as default config uses a `theme` default.
 - `gap`: distance in pixel between two squares. Default is `None` (and recommanded), in this case `gap` is calculated.
 - `idgithub`: the Github username you want to access. Default is `'cobacdavid'`.
 - `nweeks`: number of weeks i.e. columns to display. Default is 52 (a full year).
 - `theme`: a predefined color palette to use. Default is `'gh'`, github usual palette.

If you use a predefined theme, `colors` option will be ignored but `empty_cell_color` will replace the first RGB color of the theme palette.


### Interaction

 - Left click on the widget opens the username github page.
 - Right click sends a notification on existing themes names.
