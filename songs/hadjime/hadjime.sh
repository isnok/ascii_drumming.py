#!/bin/sh

ASCII_DRUMMER=${ASCII_DRUMMER:-../../ascii_drummer.py}

cat hadjime_a.drum hadjime_b.drum hadjime_shime.drum \
    hadjime_a.drum hadjime_b.drum hadjime_shime.drum \
    hadjime_a.drum hadjime_b.drum hadjime_shime.drum | $ASCII_DRUMMER "$@"

