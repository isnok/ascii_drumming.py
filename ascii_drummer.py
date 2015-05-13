#!/usr/bin/env python3
""" ascii_drummer.py - drum some ascii!

Usage:
    ascii_drummer.py [-m=<INT>] [-d=CNT] [-o=FILE] [-b=BPM] [PATTERN ...]

    Where PATTERN can be composed of these 'sounds':

        d - do
        k - ko
        D - don
        K - kon
        B - both (don+kon)
        r - rim
        : - sa

    everything else is interpreted as a one-tick pause.

Options:
    -b, --bpm=<BPM>         set tempo to BPM beats per minute [default: 90]
    -o, --output=<FILE>     write song to FILE [default: song.mp3]
    -m, --metronome=<INT>   insert metronome clicks every INT ticks
    -d, --dondokos=<CNT>    insert CNT backbeat dondokos

Examples:
    The famous dondoko beat: D.dkD.dkD.dkD.dk ...

    $ ./ascii_drummer.py -m4 D.dkD.dkD.dkD.dk D.dkD.dkD.dkD.dk

    The rolling dokonko beat: Dk.kDk.kDk.kDk.k ...

    $ ./ascii_drummer.py -m4 -b 72 Dk.kDk.kDk.kDk.k Dk.kDk.kDk.kDk.k

"""

from pydub import AudioSegment, effects
import os, glob

def my_sample(name, fmt=None):
    #print('Searching: %s' % name)

    if fmt is None:
        fmt = name.split('.')[-1]

    def find_samples(name):
        return glob.glob(name) + glob.glob('my_set'+os.sep+name)

    restore = os.getcwd()
    samples = find_samples(name)
    lastdir = None
    rel_pos = ''

    while (not samples) and os.getcwd() != lastdir:
        lastdir = os.getcwd()
        os.chdir('..')
        rel_pos += '..' + os.sep
        #print('Moving: %s -> %s' % (lastdir, os.getcwd()))
        samples = find_samples(name)

    #print('Got:', samples)

    os.chdir(restore)

    return AudioSegment.from_file(rel_pos + samples[0], fmt)

do =  my_sample('taiko4.wav') - 3
ko =  my_sample('taiko2.wav') - 3
don = my_sample('taiko3.wav')
kon = my_sample('taiko5.wav')
rim = my_sample('rim.wav') - 12
sa = effects.speedup(my_sample('sa.wav')[305:], playback_speed=3.5) - 12
#sa = effects.speedup(my_sample('sa.wav')[310:800], playback_speed=3.5) - 12

Don = my_sample('taiko1.wav')
#Don = don.overlay(kon)

click = my_sample('click.wav') - 12

char_map = {
    'd': do,
    'k': ko,
    'D': don,
    'K': kon,
    'B': Don,
    'r': rim,
    ':': sa,
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

    if args['--dondokos']:
        DONDOKOS_EARLY = int(args['--dondokos'])
        beats += DONDOKOS_EARLY

    ticks = beats * 4
    print('Beats: %d, ticks: %d' % (beats, ticks))

    tick_times = [ x * tick for x in range(ticks) ]

    song = AudioSegment.silent(duration=ticks*tick+2)

    # add Metronome
    if args['--metronome']:
        metronome_interval = int(args['--metronome'])
        print('Inserting metronome clicks every %s ticks.' % metronome_interval)
        for cnt, t in enumerate(tick_times):
            if not (cnt % metronome_interval):
                song = song.overlay(click, position=t)
        tick_times = tick_times[METRONOME_EARLY*metronome_interval:]


    # add dondokos
    if args['--dondokos']:
        print('Inserting dondokos (%s before start of pattern).' % DONDOKOS_EARLY)
        dondoko = AudioSegment.silent(duration=4*tick+2)
        dondoko = dondoko.overlay(my_sample('shime1.wav'), position=0)
        dondoko = dondoko.overlay(my_sample('shime2.wav') - 6, position=2*tick)
        dondoko = dondoko.overlay(my_sample('shime3.wav') - 6, position=3*tick)
        dondoko = dondoko - 16

        for cnt, t in enumerate(tick_times):
            if not (cnt % 4):
                song = song.overlay(dondoko, position=t)
        tick_times = tick_times[DONDOKOS_EARLY*4:]

    if not 'implemented':
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


    print('Playing song:')

    char_accu = ''
    for cnt, tup in enumerate(zip(tick_times, pattern)):

        t, char = tup
        song = song.overlay(char_map.get(char, pause), position=t)

        char_accu += char
        if not (cnt+1) % 8:
            print(char_accu)
            char_accu = ''

    if char_accu:
        print(char_accu)

    song = effects.normalize(song)

    out_file = args['--output']

    if '.' in out_file:
        out_fmt = out_file.split('.')[-1]
    else:
        out_fmt = 'mp3'

    print('Delivering (as %s) to %s.' % (out_fmt, out_file))

    song.export(out_file, out_fmt)
