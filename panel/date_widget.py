from widget import Widget
import os
import re


OTHER_TIMEZONE = "America/Los_Angeles"
OTHER_TIMEZONE_INDICATOR = "EST"


class DateWidget(Widget):
    def __init__(self):
        super(DateWidget, self).__init__()
        self.has_underline = True
        self.update_time = 1

    def update_text(self):
        local_time = os.popen("date +'%a %e %l:%M:%S %p'").read().strip()
        cali_time = os.popen(
                f"TZ={OTHER_TIMEZONE} date +'%l%p'").read().strip()
        self.text = re.sub(
                r"[ ]+", " ",
                f"{local_time} ({cali_time} {OTHER_TIMEZONE_INDICATOR})\n")
