
class SymbolTable(object):
    def __init__(self, initial_symbols=None):
        if initial_symbols is None:
            initial_symbols = {}
        self.symbols = initial_symbols.copy()

    def generate(self, memory, start_address):
        self.generate_code_symbols(memory, start_address)
        self.generate_data_symbols(memory, start_address)

    def generate_code_symbols(self, memory, start_address):
        for address in range(start_address, len(memory)):
            if memory.is_call_target(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('sub_%04x' % address, '')
            elif memory.is_jump_target(address) or memory.is_entry_point(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('lab_%04x' % address, '')
        # XXX do not overwrite

    def generate_data_symbols(self, memory, start_address):
        data_addresses = set()
        modes_always_data = ('saddrp', 'saddr', 'addrp16', 'sfr', 'sfrp',)
        modes_sometimes_data = ('addr16', )
        # never data: addr16
        # todo: imm16

        for _, inst in memory.iter_instructions():
            for mode in modes_always_data:
                address = getattr(inst, mode, None)
                if address is not None:
                    data_addresses.add(address)

            for mode in modes_sometimes_data:
                address = getattr(inst, mode, None)
                if address is not None:
                    jumped = memory.is_jump_target(address)
                    called = memory.is_call_target(address)
                    if (not jumped) and (not called):
                        data_addresses.add(address)

        for address in data_addresses:
            if address not in self.symbols:
                self.symbols[address] = ('mem_%04x' % address, '')


NEC78F0_COMMON_SYMBOLS = {}
for i, address in enumerate(range(0x40, 0x7f, 2)):
    NEC78F0_COMMON_SYMBOLS[address] = ("callt_%d_vect" % i, "CALLT #%d" % i)

D78F0547_SYMBOLS = NEC78F0_COMMON_SYMBOLS.copy()
D78F0547_SYMBOLS.update(
{
    # hardware vectors
    0x0000: ("RESET input, POC, LVI, WDT_vect", "RESET input, POC, LVI, WDT"),
    0x0004: ("INTLVI_vect", "INTLVI"),
    0x0006: ("INTP0_vect", "INTP0"),
    0x0008: ("INTP1_vect", "INTP1"),
    0x000A: ("INTP2_vect", "INTP2"),
    0x000C: ("INTP3_vect", "INTP3"),
    0x000E: ("INTP4_vect", "INTP4"),
    0x0010: ("INTP5_vect", "INTP5"),
    0x0012: ("INTSRE6_vect", "INTSRE6"),
    0x0014: ("INTSR6_vect", "INTSR6"),
    0x0016: ("INTST6_vect", "INTST6"),
    0x0018: ("INTCSI10/INTST0_vect", "INTCSI10/INTST0"),
    0x001A: ("INTTMH1_vect", "INTTMH1"),
    0x001C: ("INTTMH0_vect", "INTTMH0"),
    0x001E: ("INTTM50_vect", "INTTM50"),
    0x0020: ("INTTM000_vect", "INTTM000"),
    0x0022: ("INTTM010_vect", "INTTM010"),
    0x0024: ("INTAD_vect", "INTAD"),
    0x0026: ("INTSR0_vect", "INTSR0"),
    0x0028: ("INTWTI_vect", "INTWTI"),
    0x002A: ("INTTM51_vect", "INTTM51"),
    0x002C: ("INTKR_vect", "INTKR"),
    0x002E: ("INTWT_vect", "INTWT"),
    0x0030: ("INTP6_vect", "INTP6"),
    0x0032: ("INTP7_vect", "INTP7"),
    0x0034: ("INTIIC0/NTDMU_vect", "INTIIC0/NTDMU"),
    0x0036: ("INTCSI11_vect", "INTCSI11"),
    0x0038: ("INTTM001_vect", "INTTM001"),
    0x003A: ("INTTM011_vect", "INTTM011"),
    0x003C: ("INTACSI_vect", "INTACSI"),
    0x003E: ("BRK_vect", "BRK"),
    # special function registers
    0xff00: ('p0', 'Port 0'),
    0xff01: ('p1', 'Port 1'),
    0xff02: ('p2', 'Port 2'),
    0xff03: ('p3', 'Port 3'),
    0xff04: ('p4', 'Port 4'),
    0xff05: ('p5', 'Port 5'),
    0xff06: ('p6', 'Port 6'),
    0xff07: ('p7', 'Port 7'),
    0xff08: ('ADCR', '10-bit A/D conversion result register'),
    0xff09: ('ADCRH', '8-bit A/D conversion result register'),
    0xff0a: ('RXB6', 'Receive buffer register 6'),
    0xff0b: ('TXB6', 'Transmit buffer register 6'),
    0xff0c: ('P12', 'Port register 12'),
    0xff0d: ('P13', 'Port register 13'),
    0xff0e: ('P14', 'Port register 14'),
    0xff0f: ('SIO10', 'Serial I/O shift register 10'),
    0xff10: ('TM00', '16-bit timer counter 00'),
    0xff12: ('CR000', '16-bit timer capture/compare register 000'),
    0xff14: ('CR010', '16-bit timer capture/compare register010'),
    0xff16: ('TM50', '8-bit timer counter 50'),
    0xff17: ('CR50', '8-bit timer compare register 50'),
    0xff18: ('CMP00', '8-bit timer H compare register 00'),
    0xff19: ('CMP10', '8-bit timer H compare register 10'),
    0xff1a: ('CMP01', '8-bit timer H compare register 01'),
    0xff1b: ('CMP11', '8-bit timer H compare register 11'),
    0xff1f: ('TM51', '8-bit timer counter 51'),
    0xff20: ('pm0', 'Port mode register 0'),
    0xff21: ('pm1', 'Port mode register 1'),
    0xff22: ('pm2', 'Port mode register 2'),
    0xff23: ('pm3', 'Port mode register 3'),
    0xff24: ('pm4', 'Port mode register 4'),
    0xff25: ('pm5', 'Port mode register 5'),
    0xff26: ('pm6', 'Port mode register 6'),
    0xff27: ('pm7', 'Port mode register 7'),
    0xff28: ('ADM', 'A/D converter mode register'),
    0xff29: ('ADS', 'Analog input channel specification register'),
    0xff2c: ('PM12', 'Port mode register 12'),
    0xff2e: ('PM14', 'Port mode register 14'),
    0xff2f: ('ADPC', 'A/D port configuration register'),
    0xff30: ('pu0', 'Pull-up resistor option register 0'),
    0xff31: ('pu1', 'Pull-up resistor option register 1'),
    0xff33: ('pu3', 'Pull-up resistor option register 3'),
    0xff34: ('pu4', 'Pull-up resistor option register 4'),
    0xff35: ('pu5', 'Pull-up resistor option register 5'),
    0xff36: ('pu6', 'Pull-up resistor option register 6'),
    0xff37: ('pu7', 'Pull-up resistor option register 7'),
    0xff3c: ('pu12', 'Pull-up resistor option register 12'),
    0xff3e: ('pu14', 'Pull-up resistor option register 14'),
    0xff40: ('cks', 'Clock output selection register'),
    0xff41: ('CR51', '8-bit timer compare register 51'),
    0xff43: ('TMC51', '8-bit timer mode control register 51'),
    0xff48: ('egp', 'External interrupt rising edge enable register'),
    0xff49: ('egn', 'External interrupt falling edge enable register'),
    0xff4a: ('SIO11', 'Serial I/O shift register 11'),
    0xff4c: ('SOTB11',  'Transmit buffer register 11'),
    0xff4f: ('ISC', 'Input switch control register'),
    0xff50: ('ASIM6', 'Asynchronous serial interface operation mode register 6'),
    0xff53: ('ASIS6', 'Asynchronous serial interface reception error status register 6'),
    0xff55: ('ASIF6', 'Asynchronous serial interface transmission status register 6'),
    0xff56: ('CKSR6', 'Clock selection register 6'),
    0xff57: ('BRGC6', 'Baud rate generator control register 6'),
    0xff58: ('ASICL6', 'Asynchronous serial interface control register 6'),
    0xff60: ('SDR0L', 'Remainder data register 0'),
    0xff61: ('SDR0H', 'Remainder data register 0'),
    0xff62: ('MDA0LL', 'Multiplication/division data register A0'),
    0xff63: ('MDA0LH', 'Multiplication/division data register A0'),
    0xff64: ('MDA0HL', 'Multiplication/division data register A0'),
    0xff65: ('MDA0HH', 'Multiplication/division data register A0'),
    0xff66: ('MDB0L', 'Multiplication/division data register B0'),
    0xff67: ('MDB0H', 'Multiplication/division data register B0'),
    0xff68: ('DMUC0', 'Multiplier/divider control register 0'),
    0xff69: ('TMHMD0', '8-bit timer H mode register 0'),
    0xff6a: ('TCL50', 'Timer clock selection register 50'),
    0xff6b: ('TMC50', '8-bit timer mode control register 50'),
    0xff6c: ('TMHMD1', '8-bit timer H mode register 1'),
    0xff6d: ('TMCYC1', '8-bit timer H carrier control register 1'),
    0xff6e: ('KRM', 'Key return mode register'),
    0xff6f: ('WTM', 'Watch timer operation mode register'),
    0xff70: ('ASIM0', 'Asynchronous serial interface operation mode register 0'),
    0xff71: ('BRGC0', 'Baud rate generator control register 0'),
    0xff72: ('RXB0', 'Receive buffer register 0'),
    0xff73: ('ASIS0', 'Asynchronous serial interface reception error status register 0'),
    0xff74: ('TXS0', 'Transmit shift register 0'),
    0xff80: ('adm00', 'A/D converter mode register 00'),
    0xff81: ('ads00', 'Analog input channel specification register 00'),
    0xff84: ('SOTB10', 'Transmit buffer register 10'),
    0xff88: ('CSIM11', 'Serial operation mode register 11'),
    0xff89: ('CSIC11', 'Serial clock selection register 11'),
    0xff8c: ('TCL51', 'Timer clock selection register 51'),
    0xff90: ('CSIMA0', 'Serial operation mode specification register 0'),
    0xff91: ('CSIS0', 'Serial status register 0'),
    0xff92: ('CSIT0', 'Serial trigger register 0'),
    0xff93: ('BRGCA0', 'Division value selection register 0'),
    0xff94: ('ADTP0', 'Automatic data transfer address point specification register 0'),
    0xff95: ('ADTI0', 'Automatic data transfer interval specification register 0'),
    0xff96: ('SIOA0', 'Serial I/O shift register 0'),
    0xff97: ('ADTC0', 'Automatic data transfer address count register 0'),
    0xff99: ('WDTE', 'Watchdog timer enable register'),
    0xff9f: ('OSCCTL', 'Clock operation mode select register'),    
    0xffa0: ('RCM', 'Internal oscillation mode register'),
    0xffa1: ('MCM', 'Main clock mode register'),
    0xffa2: ('MOC', 'Main OSC control register'),
    0xffa3: ('OSTC', 'Oscillation stabilization time counter status register'),
    0xffa3: ('aaa', 'xxx'),
    0xffa4: ('OSTS', 'Oscillation stabilization time select register'),
    0xffa5: ('IIC0', 'IIC shift register 0'),
    0xffa6: ('IICC0', 'IIC control register 0'),
    0xffa7: ('SVA0', 'Slave address register 0'),
    0xffa8: ('IICCL0', 'IIC clock selection register 0'),
    0xffa9: ('IICX0', 'IIC function expansion register 0'),
    0xffaa: ('IICS0', 'IIC status register 0'),
    0xffab: ('IICF0', 'IIC flag register 0'),
    0xffac: ('RESF', 'Reset control flag register'),
    0xffb0: ('TM01', '16-bit timer counter 01'),
    0xffb2: ('CR001', '16-bit timer capture/compare register 001'),
    0xffb4: ('CR011', '16-bit timer capture/compare register 011'),
    0xffb6: ('TMC01', '16-bit timer mode control register 01'),
    0xffb7: ('PRM01', 'Prescaler mode register 01'),
    0xffb8: ('CRC01', 'Capture/compare control register 01'),
    0xffb9: ('TOC01', '16-bit timer output control register 01'),
    0xffba: ('TMC00', '16-bit timer mode control register 00'),
    0xffbb: ('PRM00', 'Prescaler mode register 00'),
    0xffbc: ('CRC00', 'Capture/compare control register 00'),
    0xffbd: ('TOC00', '16-bit timer output control register 00'),
    0xffbe: ('LVIM', 'Low-voltage detection register'),
    0xffbf: ('LVIS', 'Low-voltage detection level selection register'),
    0xffe0: ('if0l', 'Interrupt request flag register 0L'),
    0xffe1: ('if0h', 'Interrupt request flag register 0H'),
    0xffe2: ('if1l', 'Interrupt request flag register 1L'),
    0xffe3: ('if1h', 'Interrupt request flag register 1H'),
    0xffe4: ('mk0l', 'Interrupt mask flag register 0L'),
    0xffe5: ('mk0h', 'Interrupt mask flag register 0H'),
    0xffe6: ('mk1l', 'Interrupt mask flag register 1L'),
    0xffe7: ('mk1h', 'Internal mask flag register 1H'),
    0xffe8: ('pr0l', 'Priority level specification flag register 0L'),
    0xffe9: ('pr0h', 'Priority level specification flag register 0H'),
    0xffea: ('pr1l', 'Priority level specification flag register 1L'),
    0xffeb: ('pr1h', 'Priority level specification flag register 1H'),
    0xfff0: ('ims', 'Memory size switching register'),
    0xfff3: ('BANK', 'Memory bank select register'),
    0xfff4: ('ixs', 'Internal expansion RAM size switching register'),
    0xfffb: ('pcc', 'Processor clock control register'),
})
