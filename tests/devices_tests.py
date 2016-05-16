"""
devices tests
"""

from minicps.devices import Device, PLC


def test_Device():

    print
    device = Device(
        name='device',
        state='temp/state_test_db.sqlite',
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

    print 'Device name: ', device.name
    print 'Device state: ', device.state
    print 'Device protocol: ', device.protocol
    print 'Device memory: ', device.memory
    print 'Device disk: ', device.disk

    device.set('TAG1', '2')
    device.get('TAG2')


def test_PLC():

    print
    plc = PLC(
        name='plc',
        state='temp/state_test_db.sqlite',
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

    plc.set('TAG1', '2')
    plc.get('TAG2')
