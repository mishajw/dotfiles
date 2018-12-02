from number_widget import NumberWidget
import os
import re


class VolumeWidget(NumberWidget):
    def __init__(self):
        super(VolumeWidget, self).__init__('V')
        self.mute = False
        self.click_command = \
            "echo hello ; amixer sset Master mute ; amixer sset Master 0% ; echo VolumeWidget > $PANEL_FIFO"
        self.update_time = 60 * 5

    def update_number(self):
        p = os.popen("amixer sget Master | grep 'Front Left: Playback'")
        stats = p.read()

        spl = re.split(" +", stats)

        self.number = int(spl[5][1:-2])
        self.mute = spl[6][1:-2] == 'off'
