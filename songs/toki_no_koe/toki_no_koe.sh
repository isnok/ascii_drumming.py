#!/bin/sh

ASCII_DRUMMER=${ASCII_DRUMMER:-../../ascii_drummer.py}

cat toki_a.drum toki_a.drum \
    toki_a.drum toki_a.drum \
    toki_shime.drum \
    toki_b.drum toki_b.drum toki_b.drum \
    toki_shime.drum \
    toki_a.drum toki_a.drum \
    | $ASCII_DRUMMER "$@" -o toki_A.ogg

cat toki_a.drum toki_a.drum \
    toki_shime.drum \
    toki_b.drum toki_b.drum toki_b.drum \
    toki_shime.drum \
    toki_a.drum toki_a.drum \
    toki_a.drum toki_a.drum \
    | $ASCII_DRUMMER "$@" -o toki_B.ogg

