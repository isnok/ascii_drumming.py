#!/usr/bin/env python3

from pydub import AudioSegment

do = AudioSegment.from_file('my_set/do.wav', 'wav')
ko = AudioSegment.from_file('my_set/ko.wav', 'wav')
don = AudioSegment.from_file('my_set/don.wav', 'wav')
kon = AudioSegment.from_file('my_set/kon.wav', 'wav')
rim = AudioSegment.from_file('my_set/rim.wav', 'wav')

Don = don.overlay(kon)

click = AudioSegment.from_file('my_set/click.wav', 'wav')

bpm = 90
beats = 20

tick = 1000 * 60 / float(bpm * 4) # dokodoko = 1 beat = 4 ticks
ticks = beats * 4

tick_times = [ x * tick for x in range(ticks) ]

song = AudioSegment.silent(duration=ticks*tick+2)

for cnt, t in enumerate(tick_times):
    if not (cnt % 4):
        song = song.overlay(click, position=t)

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


for cnt, t in enumerate(tick_times[16:32]):
    if not (cnt % 4):
        print(t)
        song = song.overlay(dondoko, position=t)

for cnt, t in enumerate(tick_times[32:48]):
    if not (cnt % 4):
        print(t)
        song = song.overlay(dokodoko, position=t)

for cnt, t in enumerate(tick_times[48:64]):
    if not (cnt % 4):
        print(t)
        song = song.overlay(dokonko, position=t)

for cnt, t in enumerate(tick_times[64:]):
    if not (cnt % 4):
        print(t)
        song = song.overlay(dokodoko, position=t)

song.export('song.mp3', 'mp3')
