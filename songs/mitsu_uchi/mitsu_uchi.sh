#!/bin/sh

ASCII_DRUMMER=${ASCII_DRUMMER:-../../ascii_drummer.py}

cat mitsu_a.drum mitsu_a.drum \
    mitsu_b.drum mitsu_b.drum \
    mitsu_c.drum mitsu_c.drum \
    mitsu_d.drum mitsu_d.drum \
    mitsu_zwischen.drum | $ASCII_DRUMMER "$@"

