#!/bin/bash

# This project is libre, and licenced under the terms of the
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENCE, version 3.1,
# as published by dtf on July 2019. See the LICENSE file or
# https://ph.dtf.wtf/w/wtfpl/#version-3-1 for more details.

# Here is a block for i3block designed to get pipewire's sink
# volume without asking to any pulseaudio component.

# Variables
SINK="@DEFAULT_AUDIO_SINK@"

AUDIO_HIGH_SYMBOL=' '

AUDIO_MED_HIGH_THRESH=70
AUDIO_MED_HIGH_SYMBOL=' '

AUDIO_MED_THRESH=30
AUDIO_MED_SYMBOL=' '

AUDIO_LOW_THRESH=0
AUDIO_LOW_SYMBOL=' '

AUDIO_MUTED_SYMBOL=' '

function IS_MUTED ()
{
  wpctl get-volume $SINK |grep MUTED
  if [ $? == 0 ]; then
    echo "true"
  else
    echo "false"
  fi
}

function BUILD_BLOCK ()
{

  if [[ $(IS_MUTED) == "false" ]]; then
    RAW_DATA=$(wpctl get-volume $SINK | cut -d' ' -f2)
    REFINED_DATA=$(bc -l <<< "$RAW_DATA * 100" |cut -d'.' -f1)

    SYMBOL=$AUDIO_HIGH_SYMBOL
    [[ ${REFINED_DATA/\%/} -le $AUDIO_MED_HIGH_THRESH ]] && SYMBOL=$AUDIO_MED_HIGH_SYMBOL
    [[ ${REFINED_DATA/\%/} -le $AUDIO_MED_THRESH ]] && SYMBOL=$AUDIO_MED_SYMBOL
    [[ ${REFINED_DATA/\%/} -le $AUDIO_LOW_THRESH ]] && SYMBOL=$AUDIO_LOW_SYMBOL

    echo $SYMBOL $REFINED_DATA "%"
  else
    SYMBOL=$AUDIO_MUTED_SYMBOL
    echo $SYMBOL
  fi
}

BUILD_BLOCK
