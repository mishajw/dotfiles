#!/bin/bash

sudo mkdir -p /mnt/sshfstw

sudo sshfs -o allow_other mxw449@tw.cs.bham.ac.uk:/home/students/mxw449/work/ /mnt/sshfstw

