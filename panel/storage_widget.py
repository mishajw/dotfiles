import subprocess

from widget import Widget

class StorageWidget(Widget):
    def __init__(self):
        super(StorageWidget, self).__init__()
        self.update_time = 20
        self.has_underline = True

    def update_text(self):
        df_output = subprocess.check_output("df").decode()
        lines = [
            line.split()
            for line in df_output.split("\n")[1:]
            if line.strip() != ""]

        # Find how much space is free on the root partition
        free = int([l[3] for l in lines if l[5] == "/"][0])

        if free < 1e3:
            self.text = f"{free}B"
        elif free < 1e6:
            self.text = f"{free / 1e3:.2f}M"
        else:
            self.text = f"{free / 1e6:.2f}G"
