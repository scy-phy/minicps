import time

# PLC is a Device Obj
# PLC attributes
#     has a name string -> used also by Topo
#     has a protocol -> network emulation
#     has a state -> PHY layer API backend
#     has a disk dict -> client
#     has a memory dict -> client
# PLC methods
#     has a network unit: send, rec
#     has a control unit: set, get
#     has a boot process
#     has a main_loop


# tags are strings key-val pairs

from minicps.devices import PLC

# from minicps.example.swat.utils import PLC1_TAG_DICT
PLC1_TAG_DICT = {
    'TAG1' '1',
    'TAG2' '2',
    'TAG3' '3',
    'TAG4' '4',
    'TAG5' '5',
}


class ToyPLC1(PLC):

    # TODO: state good name?
    def __init__(self, name, protocol, state, disk={}, memory={}):
        """PLC1 initialization steps:

        :name: name
        :state: database backend
        :protocol: database backend
        """

        self.name = name
        self.state = state
        self.protocol = protocol
        self.memory = memory
        self.disk = disk

    # TODO: is boot a good name?
    def boot(sleep=0):
        """PLC boot process.

        :sleep: sleep n sec after the boot
        """

        # read pp state
        tag1 = self.get('TAG1')  # TODO: test it

        if tag1 == '1':
            # update internal state
            self.memory('TAG1') = tag1
        else:
            # update internal state and set a control value
            self.memory('TAG1') = tag1
            self.memory('TAG3') = '0'
            self.set('TAG3', '0')  # TODO: test it

        tag2 = self.get(tag_dict['TAG1'])

        # wait for the other plcs
        time.sleep(sleep)  # TODO: test it

    def main_loop(sleep=0):
        """PLC main loop.

        :sleep: sleep n sec after each iteration
        """

        while(time.time() - start_time < TIMEOUT):

            # TODO: translate to high level code
            # Read and update HMI_tag
            lit101_str = read_single_statedb('1', 'AI_LIT_101_LEVEL')[3]

            self.send(HMI_IP, 

            write_cpppo(L1_PLCS_IP['plc1'], 'HMI_LIT101-Pv', lit101_str)
            val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_LIT101-Pv', PLC1_CPPPO_CACHE)
            logger.debug("PLC1 - read_cpppo HMI_LIT101-Pv: %s" % val)

            lit101 = float(lit101_str)

            # lit101
            if lit101 >= LIT_101['HH']:
                logger.warning("PLC1 - lit101 over HH: %.2f >= %.2f" % (
                    lit101, LIT_101['HH']))

            elif lit101 <= LIT_101['LL']:
                logger.warning("PLC1 - lit101 under LL: %.2f <= %.2f" % (
                    lit101, LIT_101['LL']))
                # CLOSE p101
                update_statedb('0', 'DO_P_101_START')
                write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '1')
                val = read_cpppo(
                    L1_PLCS_IP['plc1'], 'HMI_P101-Status', PLC1_CPPPO_CACHE)
                logger.warning("PLC1 - close p101: HMI_P101-Status: %s" % val)

            elif lit101 <= LIT_101['L']:
                # OPEN mv101
                update_statedb('0', 'DO_MV_101_CLOSE')
                update_statedb('1', 'DO_MV_101_OPEN')
                write_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', '2')
                val = read_cpppo(
                    L1_PLCS_IP['plc1'], 'HMI_MV101-Status', PLC1_CPPPO_CACHE)
                logger.info(
                    "PLC1 - lit101 under L -> "
                    "open mv101: HMI_MV101-Status: %s" % val)

            elif lit101 >= LIT_101['H']:
                # CLOSE mv101
                update_statedb('1', 'DO_MV_101_CLOSE')
                update_statedb('0', 'DO_MV_101_OPEN')
                write_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', '1')
                val = read_cpppo(
                    L1_PLCS_IP['plc1'], 'HMI_MV101-Status', PLC1_CPPPO_CACHE)
                logger.info(
                    "PLC1 - lit101 over H -> "
                    "close mv101: HMI_MV101-Status: %s" % val)

            # read from PLC2
            val = read_cpppo(L1_PLCS_IP['plc2'], 'HMI_FIT201-Pv', PLC1_CPPPO_CACHE)
            logger.debug("PLC1 - read_cpppo HMI_FIT201-Pv: %s" % val)
            fit201 = float(val)

            # read from PLC3
            val = read_cpppo(L1_PLCS_IP['plc3'], 'HMI_LIT301-Pv', PLC1_CPPPO_CACHE)
            logger.debug("PLC1 - read_cpppo HMI_LIT301-Pv: %s" % val)
            lit301 = float(val)

            if fit201 <= FIT_201:  # or lit301 >= LIT_301['H']:
                # CLOSE p101
                update_statedb('0', 'DO_P_101_START')
                write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '1')
                val = read_cpppo(
                    L1_PLCS_IP['plc1'], 'HMI_P101-Status', PLC1_CPPPO_CACHE)
                logger.info(
                    "PLC1 - fit201 under FIT_201 -> "
                    "close p101: HMI_P101-Status: %s" % val)

            # elif lit301 <= LIT_301['L']:
            #     # OPEN p101
            #     update_statedb('1', 'DO_P_101_START')
            #     write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '2')
            #     val = read_cpppo(
            #         L1_PLCS_IP['plc1'], 'HMI_P101-Status', PLC1_CPPPO_CACHE)
            #     logger.info("PLC1 - open p101: HMI_P101-Status: %s" % val)

            # Sleep
            time.sleep(T_PLC_R)


if __name__ == "__main__":

    plc = PLC(
        name='plc1',
        state='sqlite',
        protocol='enip',
        memory={
            'TAG1' '1',
            'TAG2' '2',
            'TAG3' '3',
        },
        disk=PLC1_TAG_DICT)

    plc.boot(sleep=2)

    plc.mainloop(sleep=1)
