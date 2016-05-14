import time

# PLC is a Device Obj
# PLC
#     has a name, ect
#     has a memory: init, update
#     has a network unit: send, rec
#     has a control unit: set, get

# tags are strings key-val pairs

from minicps.devices import PLC

from minicps.example.swat.utils import PLC1_TAG_DICT

if __name__ == "__main__":
    plc = PLC(name='plc1')

    tag_dict = {
        'TAG1': '1',
        'TAG2': '2',
    }
    plc.init_memory(tag_dict)

    # read pp state
    tag1 = plc.get(tag_dict['TAG1'])

    if tag1 == '1':
        # update internal state
        plc.update_memory('TAG3', '3')
    else:
        # update internal state and set a control value
        plc.update_memory('TAG3', '2')
        plc.set('TAG3', '2')

    tag2 = plc.get(tag_dict['TAG1'])

    # wait for the other plcs
    time.sleep(3)
