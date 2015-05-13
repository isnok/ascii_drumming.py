#!/usr/bin/env python
""" ascii_jukebox.py - make a lot of noise

Usage:
    ascii_jukebox.py [-m=INT] [-d=CNT] [-b=BPMS ...] [-o=DIR] [SONGS ...]
    ascii_jukebox.py [-l|--list]

Options:
    -b, --bpm=<BPMS>        [multiple] bpm values
    -o, --output=<DIR>      write songs to DIR [default: out]
    -m, --metronome=<INT>   insert metronome with INT ticks
    -d, --dondokos=<CNT>    insert backbeat dondokos
    -l, --list              list available songs
"""

from ascii_drumming import play
from ascii_drummer import read_pattern
from glob import glob
import os

def get_song_list():
    lst = glob(os.sep.join(['songs', '*','*.song']))
    lst = sorted(set([x.split(os.sep)[1] for x in lst]))
    return lst

song_list = get_song_list()

def list_songs():
    global song_list
    for cnt, name in enumerate(song_list):
        print('Song Nr. %d - %s' % (cnt, name))

def read_song(stream):
    for line in stream.readlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line

def interpret(file, bpm, metronome, dondokos):
    dirstack = file.split(os.sep)[:-1]
    pattern = ''
    for line in read_song(open(file)):
        drum_file = os.sep.join(dirstack + [line]) + '.drum'
        pattern += read_pattern(open(drum_file))
    return play(pattern, bpm, metronome, dondokos)

def do_song(name, bpm, metronome, dondokos):

    song_file = glob(os.sep.join(['songs', name, '*.song']))[0]
    print(song_file)
    song = interpret(song_file, bpm, metronome, dondokos)

    metro = '' if not metronome else '_metronome'
    ddks = '' if not dondokos else '_%dddks' % dondokos

    out_file = os.sep.join([args['--output'], name, '%s_-_%sbpm%s%s.ogg' % (name, bpm, metro, ddks)])
    print('Delivering: %s' % out_file)
    song.export(out_file, 'ogg')


if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    if args['--list']:
        list_songs()
        import sys
        sys.exit()

    print(args)

    if args['--metronome'] is not None:
        metronome = int(args['--metronome'])
    else:
        metronome = None

    if args['--dondokos'] is not None:
        dondokos = int(args['--dondokos'])
    else:
        dondokos = None

    bpms = [ int(x) for x in args['--bpm'] ]
    songs = [ int(x) for x in args['SONGS']]

    print('Songs to play:', ', '.join(args['SONGS']))

    for bpm in bpms:
        for number in songs:
            song_name = song_list[number]
            try:
                os.mkdir(args['--output'] + os.sep + song_name)
            except:
                pass

            do_song(song_name, bpm, metronome, dondokos)

            if metronome:
                do_song(song_name, bpm, None, dondokos)
            if dondokos:
                do_song(song_name, bpm, metronome, None)
            if metronome and dondokos:
                do_song(song_name, bpm, None, None)
