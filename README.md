# My Qtile Widgets

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/barre.gif?raw=true" width=100% />

## License

[GNU/GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)


## Scripts

- [Layout colored icons](#layout-images)
- [click coords](#click-coords)


### Layout images

The script `layout_img.py` contains the `path_color_layout`
function that takes as single argument an hexcolor-like string like
`"FF0000"` and returns a path that may be used as custom layout
icon dir. in `CurrentLayout` official widget.

Currently, the script uses `/tmp` to create colored icons.

For example, two icons using `"4989BC"` color:

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/layout-matrix.png?raw=true" width=40px /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/layout-monadtall.png?raw=true" width=40px />


If an error occured during process, the script returns default directory of qtile
resources, so the widget remains white colored.

#### Usage

In your `config.py` file:

```python
from widgets.layout_img import path_color_layout  # line to customize...
...
layout_icons_dir = path_color_layout("FF0000")
...
mywidgets = [
	...
	widget.CurrentLayout(mode='icon',
                         scale=.9,
                         custom_icon_paths=[layout_icons_dir]),
	...
	]
...
```


### Click Coords

This module contains a class you should use to access `(x,y)` coordinates in your widget.

#### Usage

In your new own widget file:

```python
from .click_coords import Click_coords_mixin

class My_new_widget(Click_coords_mixin, base._Widget):
    ...
    def __init__(self, *args, **config):
        super().__init__(length=0, **config)
        # 
        self.set_click_handler(self.on_click)
        # now whatever you want in your widget
        ...

    def on_click(self, x, y):
        # whatever you want to do using x and y
        ...

```


## Widgets

- [Github contrib. widget](#github-contribution-widget)
- [Matrix](#matrix)
- [Tixynet](#tixynet)
- [Clock](#clock)
- [Volume](#volume)
- [Pct](#pct)
- [Xeyes](#xeyes)

These widgets access to some default variables set in `widget_defaults` variable, as `font`, `fontsize`, `padding` and `foreground`. Please, pay attention to set these default variables if you wish to use widgets defined in this page.

## Github Contribution Widget

Default options example (use `gap=1` option if needed):

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/ghcw.png?raw=true" width=50% />

Image with 2 years and `ice` colormap  with reversed colors:

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/ghcw2.png?raw=true" width=100% />


### Install

The `Ghcw` widget needs `click_coords.py` file and the `ghcw.py` file.

Install them using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).

You will also need the  `aiohttp` and `colormaps` libraries : `pip install aiohttp colormaps`.

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

 - `colors`: a five hex RGB colors string tab using `"000000"` for black and `"ffffff"` for white. Default is `None` as default config uses a `theme` default.
 - `empty_cell_color` : RGB color string for 0 contrib. Useful to set according to qtile bar background. Default is `None` as default config uses a `theme` default.
 - `gap`: distance in pixel between two squares. Default is `None`, in this case `gap` is calculated. Best visual results with small values as `1`.
 - `idgithub`: the Github username you want to access. Default is `'cobacdavid'`.
 - `nweeks`: number of weeks i.e. columns to display. Default is 52 (a full year).
 - `revcolors`: boolean value to reverse colors order. Default is `False`.
 - `theme`: a color palette to use. Default is `'ghcw_gho'`, github usual palette. You can use a colormap name form [colormaps libray](https://pratiman-91.github.io/colormaps/).

If you use a predefined theme, `colors` option will be ignored but `empty_cell_color` will replace the first RGB color of the theme palette.


### Interaction

 - Left click sends a notification on the day you click on for example: `Sun 11 Jan 26: 2 contributions`.
 - Middle click on the widget opens the username github page.
 - Right click switch current theme with embeded themes: `ghcw_lgt`, `ghcw_drk`, `ghcw_gho`, `ghcw_ghd`, `ghcw_bdx`, `ghcw_red` and `ghcw_blu`.

## Matrix

The widget offers a 10x10 square pixels matrix. According to a value in [0-100] interval, the widgets lights up pixels.

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/matrix.png?raw=true" width=10% />

Pixels are chosen randomly. For example, with a battery charge: 100% lights up every pixel, while 50% lights up half of the pixels.

The value comes from a shell command or a Python function.

### Install

The `Matrix` widget is in the `matrix.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import matrix  # if you put matrix.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    matrix.Matrix(inmargin=0, cmd=r"cat /sys/class/power_supply/BAT0/capacity"),
    ...
]
...
```

### Options

 - `ìnmargin` (int): margin all around the square. Default is `2` (pixels) ;
 - `update_interval` (int): delay in seconds between two refreshs of the widget. Default is `300` (seconds=5 minutes) ;
 - `cmd` (str): shell command to execute to get the value. The command has to return a number between 0 and 100. Default is `r"echo $(( RANDOM % 101 ))"`. Note: The string resulting will be stripped if it contains unwanted blank spaces. So don't worry about extra spaces...
 - `execshell` (str): path to shell to be used. Default is `"/usr/bin/bash"`.
 - `pyfunc` (function): a Python function returning a number between 0 and 100. Default is `None`.

If `pyfunc` is not `None`, the shell command will be ignored.

### Interaction
No interaction.

## Tixynet

The widget offers a tixy experience (https://tixy.land/) associated with net UP or DOWN. Animation continues if UP else animation stops.

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/tixynet.gif?raw=true" width=30% />


### Install

The `Tixynet` widget is in the `tixynet.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import tixynet  # if you put tixynet.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    tixynet.Tixynet(iface="enp3s0"),
    ...
]
...
```

### Options

 - `iface` (str): network interface. Default is `"eth0"`.
 - `iface_interval` (int): delay in seconds between two net UP check. Default is `5`.
 - `colors` (list[str, str]): colors array, first element for positive color, second  d for negative. Default is `["ffffff", "ff0000"]`.
 - `force_step` (float): Forces fake time `t` step. Can be useful using great `update_interval` to get a slow animation. Default is `None`.
 - `ìnmargin` (int): margin all around the widget. Default is `2` (pixels) ;
 - `pyfunc` (function): a Python function returning a number between -1 and 1. Default is `"lambda t,i,x,y: math.sin(y/8+t)"`.
 - `update_interval` (int): delay in seconds between two refreshs of the widget. This controls the  `t` parameter.  Default is `1` (refresh every second).
 - `w` and `h` control number of cells, respectively in width and height. Default values are respectively `20` and `10`. 


### Interaction
No interaction.

## Clock

An alternative clock with 4 available layouts. 

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/clock0.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/clock1.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/clock2.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/clock3.png?raw=true" width=10% />


### Install

The `Clock` widget is in the `clock.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import clock  # if you put clock.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    clock.Clock(),
    ...
]
...
```

### Options

 - `fmts` (list[str, str]): two usual time string formats. Default is `["%d/%m", "%H:%M"]`.
 - `gapy` (int): vertical space between the two displays in pixels, uisng state 0 or 1. Default is `2` pixels.
 - `state` (int): 0, 1, 2 or 3. Default is `0`.
    - `0`: 1st format above 2nd
    - `1`: 2nd format above 1st
    - `2`: 1st format only
    - `3`: 2nd format only

### Interaction

Left and right click change `state`.

## Volume

An alternative volume with 2 available layouts. 

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/volume1.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/volume2.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/volume3.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/volume4.png?raw=true" width=10px />


### Install

The `Volume` widget is in the `volume.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import volume  # if you put volume.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    volume.Volume(),
    ...
]
...
```

### Options

 - `bar_bg` (str): color of bar background. Default is `"cccccc"`.
 - `bar_length` (int): for `"h"` orientation only. Widget length. Default is `40` pixels.
 - `bar_width` (int): bar thickness. Default is `10`.
 - `cellgap` (int|float): space between two cells. Default is `1`. Ignored no `ncells` option.
 - `execshell` (str): shell to use to execute `amixer` commands. Default is `"/usr/bin/bash"`.
 - `ncells` (int): number of cells to draw. Default is `None`. If not `None`, the volume bar is drawn using cells.
 - `orient` (str): `"h"` or `"v"` for horizontal or vertical mode. Default is `v`.
 - `step` (int): when increasing or decreasing volume with `amixer`, amount of volume measure. Default is `1000`.
 - `ymargin` (int): y margin in pixels. Default is `2`.

### Interaction

Left click toggle mute mode, volume bar is no more filled but outlined. Using wheel increases or decreases volume.


## Pct

An alternative versatile percentage widget.

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/pct.png?raw=true" width=30% /> 


### Install

The `Pct` widget is available with  `pct.py` and `flower_pbar.py` files. You also need the `colormaps` libraries : `pip install colormaps`.

Install them using a `git clone` command or just in copying the files in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import pct  # if you put pct.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    pct.Pct(),
    ...
]
...
```

Below a complete example of a `volume` control widget using `Pct`:

```python
def volume_exec(cmd):
    import subprocess
    subprocess.run(cmd, text=True, shell=True, executable="/usr/bin/bash")


def mute(obj):
    volume_exec("amixer set Master mute")
    obj.draw_method = "stroke"


def unmute(obj):
    volume_exec("amixer set Master unmute")
    obj.draw_method = "fill"


def inc_v(obj):
    volume_exec("amixer set Master 5%+")


def dec_v(obj):
    volume_exec("amixer set Master 5%-")


...
pct.Pct(cmd="amixer get Master "
        "| awk -F'[][]' 'END{print $2}' | tr -d '%'",
        colors=[flower_active, flower_inactive],
        text="vol",
        nsectors=20,
        update_interval=.2,
        button1=mute,
        button3=unmute,
        button4=inc_v,
        button5=dec_v)
...
```

### Options
 - `button[1-7]` (str): optional python callback functions for interactive use. Default is `None`.
 - `center_text` (bool): it displays the progressbar and the text centered. Default is `True`.
 - `cmd` (str): command to execute to get the value to represent. Default is `"awk '/MemTotal/ {t=$2} /MemAvailable/ {a=$2} END {printf \"%.0f\\n\", ((t-a)/t)*100}' /proc/meminfo"`, it returns RAM memory currently used.
 - `colormap` (str): colormap from `colormaps` lib. Default is `None`.
 - `colormap_rev` (bool): boolean to reverse colormap. Default is `False`.
 - `colors` (list[str, str]): colors array, first element for positive color, second  d for negative. Default is `["ffffff", "ff0000"]`.
 - `execshell` (str): shell to use to execute `amixer` commands. Default is `"/usr/bin/bash"`.
 - `inradius` (float): if given respect inner radius in pixels. Default is `None`, in this case, the value is 10% of bar height.
 - `hide_text`(bool): do not show the text. Default is `False`.
 - `max` (float): max of values. Default is `100`.
 - `min` (float): min of values. Default is `0`.
 - `nsectors` (int): number of sectors to use. Default is `10`, min is `2`.
 - `rev` (bool): clockwise (`False`) or not (`True`). Default is `True`.
 - `text` (str): the text to display. Default is `"mem"`.
 - `text_size` (int): Fontsize to use. Default is `10`.
 - `update_interval` (int): delay in seconds between two refreshs of the widget. If set to `0`, no updates will occur, unless using `button[1-7]` (at least one) with a callback function. Default is `1` (refresh every second).
 - `ymargin` (int): y margin in pixels. Default is `2`.

### Interaction

Left click (`button1`) sends a notification of current value. You can bind options `button[1-7]` to python functions.

## Xeyes

A [xeyes](https://fr.wikipedia.org/wiki/Xeyes)-like widget.

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/img/xeyes.png?raw=true" width=10% />


### Install

The `Xeyes` widget is in the `xeyes.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import xeyes  # if you put volume.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    xeyes.Xeyes(),
    ...
]
...
```

### Options

 - `eye_color` (str): color of eye. Default is `"ffffff"` (white).
 - `eye_radius` (int): eye radius. Default is `10` pixels.
 - `gap` (int): space between eyes. Default is `3` pixels.
 - `padding` (int): horizontal space with widget's edge. Default is `0` pixel.
 - `pupil_radius` (str): pupil radius. Default is `3` pixels.
 - `pupil_color` (str): color of pupil. Default is `"000000"` (black).
 - `update_interval` (float): delay between two refreshs. Default is `0.04` (25 fps).

### Interaction
None
