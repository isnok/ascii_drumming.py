#!/usr/bin/env python3
""" ascii_drummer.py - drum some ascii!

Usage:
    ascii_drummer.py [-p] [-m=<INT>] [-d=CNT] [-o=FILE] [-b=BPM] [PATTERN ...]

    Where PATTERN can be composed of these 'sounds':

        d - do
        k - ko
        D - don
        K - kon
        B - both (don+kon)
        r - rim
        s - shime do
        z - shime ko
        S - shime don
        : - sa

    everything else is interpreted as a one-tick pause.

Options:
    -b, --bpm=<BPM>         set tempo to BPM beats per minute [default: 90]
    -o, --output=<FILE>     write song to FILE
    -m, --metronome=<INT>   insert metronome clicks every INT ticks
    -d, --dondokos=<CNT>    insert CNT backbeat dondokos
    -p, --playback          play assembled pattern

Examples:
    The famous dondoko beat: D.dkD.dkD.dkD.dk ...

    $ ./ascii_drummer.py -p -m4 D.dkD.dkD.dkD.dk D.dkD.dkD.dkD.dk

    The rolling dokonko beat: Dk.kDk.kDk.kDk.k ...

    $ ./ascii_drummer.py -p -m4 -b 72 Dk.kDk.kDk.kDk.k Dk.kDk.kDk.kDk.k

"""

from ascii_drumming import play
import sys

def read_pattern(stream=sys.stdin):
    pattern = ''
    for line in stream.readlines():
        if not line.strip() or line.strip().startswith('#'):
            continue
        pattern += line.strip()
    return pattern


if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)
    print(args)

    bpm = int(args['--bpm'])

    if args['PATTERN']:
        pattern = ''.join(args['PATTERN'])
    else:
        pattern = read_pattern()

    print('Pattern: %r' % pattern)

    if args['--metronome'] is not None:
        metronome = int(args['--metronome'])
    else:
        metronome = None

    if args['--dondokos'] is not None:
        dondokos = int(args['--dondokos'])
    else:
        dondokos = None

    song = play(pattern, bpm, metronome, dondokos)

    if not (args['--output'] or args['--playback']):
        args['--playback'] = True

    if args['--playback']:
        print('Playing song.')
        from pydub import playback
        playback.play(song)

    if args['--output'] is not None:
        out_file = args['--output']

        if '.' in out_file:
            out_fmt = out_file.split('.')[-1]
        else:
            out_fmt = 'mp3'

        print('Delivering (as %s) to %s.' % (out_fmt, out_file))
        song.export(out_file, out_fmt)
