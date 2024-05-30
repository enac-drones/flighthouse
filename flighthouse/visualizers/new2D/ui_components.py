from __future__ import annotations
from typing import Any, Literal
from matplotlib.axes import Axes

# from gui.gui_sim import InteractivePlot
import matplotlib.pyplot as plt
from matplotlib.typing import ColorType
from numpy.typing import ArrayLike
from .observer_utils import Observable
from matplotlib.widgets import Slider


class Buttons(Observable):
    def __init__(self, ax: plt.Axes):
        super().__init__()
        self.ax = ax
        self.fig = ax.figure
        self.buttons: dict[str, dict[str, plt.Axes | str | function]] = {
            "play": {
                "axis": self.fig.add_axes([0.01, 0.01, 0.20, 0.05]),
                "label": "Pause",
                "callback": self.on_run,
            },
            "reset": {
                "axis": self.fig.add_axes([0.22, 0.01, 0.1, 0.05]),
                "label": "Reset",
                "callback": self.on_reset,
            },
        }

        # Initialize buttons and register callbacks
        for key, btn_info in self.buttons.items():
            button = plt.Button(btn_info["axis"], btn_info["label"])
            button.on_clicked(btn_info["callback"])
            self.buttons[key]["button"] = button

    def rename_button(self, button_key: str, new_label: str) -> None:
        if button_key in self.buttons:
            self.buttons[button_key]["button"].label.set_text(new_label)
        else:
            raise ValueError(f"No button found with the key '{button_key}'")

    def on_run(self, event):
        self.notify_observers("play")

    def on_reset(self, event):
        self.notify_observers("reset")


class MySlider(Observable):
    def __init__(self, fig) -> None:
        super().__init__()
        self.fig = fig
        self.updating = False
        self.slider = self._create_slider()
        self.cid = self.slider.on_changed(self.update)
        self.slider.disconnect(self.cid)
        self.val = 0

    def _create_slider(self):
        # Create axes for sliders
        # variable inside add_axes is left, bottom, width, height
        ax_prog = self.fig.add_axes([0.3, 0.92, 0.4, 0.05])
        ax_prog.spines["top"].set_visible(True)
        ax_prog.spines["right"].set_visible(True)

        # Create slider object to iterate through the plot
        slider = Slider(
            ax=ax_prog,
            label="Progress ",
            valinit=0.0,
            valstep=0.01,
            valmin=0,
            valmax=1.0,
            valfmt=" %1.1f ",
            facecolor="#cc7000",
        )
        return slider

    def get_slider(self) -> Slider:
        return self.slider

    def update(self, val):
        self.updating = True  # Signal that the slider is being adjusted
        self.val = val  # Update frame based on slider position
        self.notify_observers("slider_update")
        self.updating = False

    def set_val(self, val):
        self.slider.set_val(val)

    def disconnect_callback(self):
        self.slider.disconnect(self.cid)

    def reconnect_callback(self):
        self.cid = self.slider.on_changed(self.update)
