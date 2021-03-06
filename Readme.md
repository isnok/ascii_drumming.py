Ascii Drummer
=============

rockahoolio beats from the ascii world.

Installation / Setup
--------------------

You need python3 and pyvenv to easily fetch all dependencies as follows:

```
... $ pyvenv venv
... $ . venv/bin/activate
(venv) ... $ pip install -r requirements.txt
```

Test it out, say with a dokonko beat ontop of a dondoko backbeat:

```
(venv) ... $ ./ascii_drummer.py -o dokonko.ogg -d4 Dk.k Dk.k Dk.k Dk.k
```

Then, play the newly created track:

```
(venv) ... $ mpv dokonko.ogg
```

You can also assemble a beat and play it back directly:

```
(venv) ... $ ./ascii_drummer.py -p -m4 -d2 D.dkD.dkD.dkD.dk D.dkD.dkD.dkD.dk
```

Have fun!
