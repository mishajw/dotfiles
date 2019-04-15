#!/usr/bin/env bash

duplicity \
  --progress \
  --encrypt-key 92271A1D \
  --exclude /home/misha/.ssh \
  --exclude /home/misha/.gnupg \
  --exclude /home/misha/Downloads \
  --exclude /home/misha/media \
  --exclude /home/misha/data \
  --exclude /home/misha/Dropbox \
  --exclude /home/misha/misha.tar.gz \
  --exclude /home/misha/prog \
  $HOME file:///mnt/mycloud/duplicity-backups
