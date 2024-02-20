'''
Usage: k0dasm <filename.bin>

'''

import sys

from k0dasm.disassemble import disassemble
from k0dasm.memory import Memory
from k0dasm.trace import Tracer
from k0dasm.listing import Printer
from k0dasm.symbols import SymbolTable, D78F0547_SYMBOLS

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    with open(sys.argv[1], 'rb') as f:
        rom = bytearray(f.read())
    memory = Memory(rom)

    start_address = 0
    entry_points = []
    hardware_vectors = [ # TODO these are D78F0547 specific
        0x0000, # RESET input, POC, LVI, WDT
        0x0004, # INTLVI
        0x0006, # INTP0
        0x0008, # INTP1
        0x000A, # INTP2
        0x000C, # INTP3
        0x000E, # INTP4
        0x0010, # INTP5
        0x0012, # INTSRE6
        0x0014, # INTSR6
        0x0016, # INTST6
        0x0018, # INTCSI10/INTST0
        0x001A, # INTTMH1
        0x001C, # INTTMH0
        0x001E, # INTTM50
        0x0020, # INTTM000
        0x0022, # INTTM010
        0x0024, # INTAD
        0x0026, # INTSR0
        0x0028, # INTWTI
        0x002A, # INTTM51
        0x002C, # INTKR
        0x002E, # INTWT
        0x0030, # INTP6
        0x0032, # INTP7
        0x0034, # INTIIC0/NTDMU
        0x0036, # INTCSI11
        0x0038, # INTTM001
        0x003A, # INTTM011
        0x003C, # INTACSI
        0x003E, # BRK
    ]
    callt_vectors = list(range(0x40, 0x7f, 2))
    all_vectors = hardware_vectors + callt_vectors

    traceable_range = range(start_address, start_address + len(rom) + 1)
    tracer = Tracer(memory, entry_points, all_vectors, traceable_range)
    tracer.trace(disassemble)

    symbol_table = SymbolTable(D78F0547_SYMBOLS) # TODO
    symbol_table.generate(memory, start_address) # xxx should pass traceable_range

    printer = Printer(memory,
                      start_address,
                      traceable_range[-1] - 1,
                      symbol_table
                      )
    printer.print_listing()
