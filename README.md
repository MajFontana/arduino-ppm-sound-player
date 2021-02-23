# arduino-ppm-sound-player
Arduino program that plays sound using pulse position modulation. Python utility to convert midi files included

To play a midi file of your choice, first set the SOURCE variable in midi_parser.py to the path to your midi file, and run the script. Then compile player.ino and upload the program to your Arduino.
In player.ino set the appropriate SPEAKER_PIN variable. You can configure the maxpoly variable to limit the amount of notes played at a time.

Note that at present the program doesn't filter out drum notes, and will treat them like all other notes, thus attempt to play them according to their note numbers.