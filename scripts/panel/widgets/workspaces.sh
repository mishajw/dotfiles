#!/bin/bash

bspc control --subscribe | $PANEL_PATH/widgets/.workspace-parser.sh
