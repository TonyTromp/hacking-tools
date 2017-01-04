#!/bin/bash

if pmset -g ps | grep -q "Now drawing from 'AC Power'"
  then echo "connected"
  else echo "not connected"
fi

