#!/usr/bin/env python3
""" ascii_drummer.py - drum some ascii!

Usage:
    ascii_drummer.py [-m] [-b=BPM] [PATTERN ...]

    Where pattern can consits of these 'sounds':

        d - do
        k - ko
        D - don
        K - kon
        B - both (don+kon)
        r - rim

    everything else is interpreted as a one-tick pause.

Options:
    -m, --metronome         insert metronome clicks
    -b, --bpm=<BPM>         set tempo to BPM beats per minute [default: 90]

Examples:
    The famous dondoko beat: D.dkD.dkD.dkD.dk ...
    The famous dokonko beat: Dk.kDk.kDk.kDk.k ...

"""

from pydub import AudioSegment

do = AudioSegment.from_file('my_set/ko.wav', 'wav')
ko = AudioSegment.from_file('my_set/do.wav', 'wav')
don = AudioSegment.from_file('my_set/kon.wav', 'wav')
kon = AudioSegment.from_file('my_set/don.wav', 'wav')
rim = AudioSegment.from_file('my_set/rim.wav', 'wav') - 12

Don = don.overlay(kon)

click = AudioSegment.from_file('my_set/click.wav', 'wav')

char_map = {
    'd': do,
    'k': ko,
    'D': don,
    'K': kon,
    'B': Don,
    'r': rim,
}

pause = AudioSegment.silent(duration=0.1)

if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)
    print(args)

    bpm = int(args['--bpm'])
    tick = 1000 * 60 / float(bpm * 4) # dokodoko = 1 beat = 4 ticks
    print('BPM: %s, tick: %s' % (bpm, tick))

    if args['PATTERN']:
        pattern = ''.join(args['PATTERN'])
    else:
        import sys
        pattern = sys.stdin.read()
        pattern = pattern.replace(' ', '').replace('\n', '')

    print('Pattern: %r' % pattern)

    beats = (len(pattern)+3) // 4

    METRONOME_EARLY = 4
    if args['--metronome']:
        beats += METRONOME_EARLY

    ticks = beats * 4
    print('Beats: %d, ticks: %d' % (beats, ticks))

    tick_times = [ x * tick for x in range(ticks) ]

    song = AudioSegment.silent(duration=ticks*tick+2)

    # add Metronome
    if args['--metronome']:
        for cnt, t in enumerate(tick_times):
            if not (cnt % 4):
                song = song.overlay(click, position=t)
        tick_times = tick_times[METRONOME_EARLY*4:]


    dondoko = AudioSegment.silent(duration=4*tick+2)
    dondoko = dondoko.overlay(don, position=0)
    dondoko = dondoko.overlay(do, position=2*tick)
    dondoko = dondoko.overlay(ko, position=3*tick)
    dondoko = dondoko - 16

    dokodoko = AudioSegment.silent(duration=4*tick+2)
    dokodoko = dokodoko.overlay(do, position=0)
    dokodoko = dokodoko.overlay(ko, position=tick)
    dokodoko = dokodoko.overlay(do, position=2*tick)
    dokodoko = dokodoko.overlay(ko, position=3*tick)
    dokodoko = dokodoko - 16

    dokonko = AudioSegment.silent(duration=4*tick+2)
    dokonko = dokonko.overlay(do, position=0)
    dokonko = dokonko.overlay(ko, position=tick)
    dokonko = dokonko.overlay(ko, position=3*tick)
    dokonko = dokonko - 16

    for t, char in zip(tick_times, pattern):
        song = song.overlay(char_map.get(char, pause), position=t)

    song.export('song.mp3', 'mp3')
