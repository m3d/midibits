"""
  MID files parser(/writer?)
  usage:
      python ./midfile.py <MID file>
"""
# note, targeted for Python3 only

# MID file specification:
# http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html

import sys
import struct


def get_varlen(data):
    """variable read"""
    ret = 0
    for i, b in enumerate(data):
#        print(i, b)
        ret <<= 7
        ret += (0x7F & b)
        if b & 0x80 == 0:
#            print(b)
            return ret, data[i+1:]
    assert 0
#    return b, data[1:]


def parse(filename):
    f = open(filename, 'rb')

    # File Main Header
    header = f.read(4)
    assert header == b'MThd', header  # header data
    length, = struct.unpack('>I', f.read(4))
    assert length == 6, length  # simple header
    fmt, ntrks, division = struct.unpack('>HHH', f.read(length))
    assert fmt in [0, 1], fmt
    print('Number of tracks {}, division {}'.format(ntrks, division))

    while True:
        header = f.read(4)
        if len(header) != 4:
            break
        assert header == b'MTrk', header
        length, = struct.unpack('>I', f.read(4))
        data = f.read(length)
        print(len(data))
        # <delta-time> is stored as a variable-length quantity.
        # <event> = <MIDI event> | <sysex event> | <meta-event>
    
        while data:
            dt, data = get_varlen(data)
#            print(dt, data[0])
            event = data[0]
            if event == 0xFF:
                # meta event FF <type> <length> <bytes>
                etype = data[1]
                elen, data = get_varlen(data[2:])
                edata = data[:elen]
#                print(edata)
                data = data[elen:]
            elif event == 0xC0:
                # Program Change
                program_number = data[1]
                data = data[2:]
            elif event == 0xB0:
                # Control Change
                data = data[3:]
            elif event == 0xA0:
                # Polyphonic Key Pressure (Aftertouch)
                data = data[3:]
            elif event == 0x90:
                # Note On event.
                print('Note On {}, {}'.format(data[1], data[2]))
#                print('Note On {}, {} [{}]'.format(data[1], data[2],
#                    [hex(x) for x in data[3:10]]))
                data = data[3:]
            elif event < 128:
                # MIDI Controller Messages
                print('data at {} ({}, {})'.format(dt, data[0], data[1]))
                data = data[2:]
            else:
                assert event in [], hex(event)
                data = data[1:]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(-1)
    parse(filename=sys.argv[1])

# vim: expandtab sw=4 ts=4
