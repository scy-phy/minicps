"""
devices tests
"""

from minicps.devices import Device, PLC

from nose.tools import eq_


def test_Device():

    print
    device = Device(
        name='device',
        state={
            'path': 'temp/state_test_db.sqlite',
            'name': 'state_test'
        },
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

    # device.set('TAG1', '2')
    # device.get('TAG2')


def test_PLC():

    class TestPLC(PLC):

        def pre_loop(self, sleep=0.5):
            """PLC boot process.

            :sleep: sleep n sec after it
            """

            print self.get(('SENSOR3', 1))[0]
            time.sleep(sleep)

    print
    plc = TestPLC(
        name='plc',
        state={
            'path': 'temp/state_test_db.sqlite',
            'name': 'state_test'
        },
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

    # eq_(plc.get(('SENSOR3', 1))[0], '1')
    # eq_(plc.get(('SENSOR3', 2))[0], '2')
