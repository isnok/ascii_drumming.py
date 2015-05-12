#!/bin/sh

ASCII_DRUMMER=${ASCII_DRUMMER:-../../ascii_drummer.py}

cat toki_a.drum | $ASCII_DRUMMER "$@"

