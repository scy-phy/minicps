"""
devices tests
"""

from minicps.devices import Device


def test_Device():

    device = Device(
        name='device',
        state='sqlite',
        protocol='enip',
        memory={
            'TAG1': '1',
            'TAG2': '2',
        },
        disk={
            'TAG1': '1',
            'TAG2': '2',
            'TAG4': '4',
            'TAG5': '5',
        })

    print
    print device.name
    print device.state
    print device.protocol
    print device.memory
    print device.disk
