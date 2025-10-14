"""Pass-I of a simple two-pass assembler (improved and functional).

Produces:
- intermediate.txt : intermediate code with references to symbol/literal indexes
- symbol_table.txt : symbol -> address
- literal_table.txt : literal -> address

This module reads a simple assembly file (default: code.asm) and generates
the tables required for Pass-II.
"""

import re
import sys


def read_assembly_file(filename):
	with open(filename, 'r') as f:
		# strip comments and blank lines
		lines = []
		for raw in f:
			line = raw.split(';', 1)[0].strip()
			if line:
				lines.append(line)
		return lines


def write_table(filename, lines):
	with open(filename, 'w') as f:
		for line in lines:
			f.write(f"{line}\n")


"""Pass-I assembler (clean implementation)

Generates:
- intermediate.txt
- symbol_table.txt
- literal_table.txt

This implements a basic Pass-1 for a simple assembly language. It assigns
symbol and literal indices and writes intermediate code using (IS/AD/DL),
registers as (RG, rr) and symbol/literal references as (S, n) / (L, n).
"""

import re
"""Pass-I assembler (clean implementation)

Generates:
- intermediate.txt
- symbol_table.txt
- literal_table.txt

This implements a basic Pass-1 for a simple assembly language. It assigns
symbol and literal indices and writes intermediate code using (IS/AD/DL),
registers as (RG, rr) and symbol/literal references as (S, n) / (L, n).
"""

import re
import sys
from typing import List


def read_assembly_file(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        lines = []
        for raw in f:
            line = raw.split(';', 1)[0].strip()
            if line:
                lines.append(line)
        return lines


def write_lines(filename: str, lines: List[str]) -> None:
    with open(filename, 'w') as f:
        for l in lines:
            f.write(l + "\n")


def pass1_assembler(input_file: str = 'code.asm',
                    sym_file: str = 'symbol_table.txt',
                    lit_file: str = 'literal_table.txt',
                    interm_file: str = 'intermediate.txt') -> None:
    # Tables
    IS = {'MOVER': '04', 'ADD': '01', 'SUB': '02', 'MULT': '03', 'MOVEM': '05', 'BC': '07'}
    AD = {'START': '01', 'END': '02'}
    DL = {'DS': '01', 'DC': '02'}
    REG = {'AREG': '01', 'BREG': '02', 'CREG': '03', 'DREG': '04'}

    symbol_index = {}   # name -> index (1-based)
    symbol_table = {}   # name -> address (None if unknown yet)
    literal_index = {}  # literal -> index (1-based)
    literal_table = {}  # literal -> address (None if unknown yet)
    literal_pool = []   # list of literals in order of first appearance

    intermediate = []
    loc = 0

    lines = read_assembly_file(input_file)

    for line in lines:
        tokens = [t for t in re.split(r"[ ,\t]+", line) if t != '']
        if not tokens:
            continue

        # detect label
        label = None
        if tokens[0] not in IS and tokens[0] not in AD and tokens[0] not in DL:
            label = tokens[0]
            tokens = tokens[1:]
            # if label alone, define its address
            if not tokens:
                if label not in symbol_index:
                    symbol_index[label] = len(symbol_index) + 1
                symbol_table[label] = loc
                continue

        if not tokens:
            continue

        opcode = tokens[0]

        # Assembler Directives
        if opcode in AD:
            if opcode == 'START':
                val = tokens[1] if len(tokens) > 1 else '0'
                try:
                    loc = int(val)
                except ValueError:
                    loc = 0
                intermediate.append(f"(AD, {AD[opcode]}) (C, {val})")
            elif opcode == 'END':
                intermediate.append(f"(AD, {AD[opcode]})")
                # assign addresses to literals in pool starting at current loc
                for lit in literal_pool:
                    if literal_table.get(lit) is None:
                        literal_table[lit] = loc
                        loc += 1
            continue

        # record label address
        if label:
            if label not in symbol_index:
                symbol_index[label] = len(symbol_index) + 1
            symbol_table[label] = loc

        # Imperative Statements
        if opcode in IS:
            op_code = IS[opcode]
            reg_code = '00'
            operand_part = ''

            # possible forms: OPC R,operand  OR OPC operand  OR OPC R
            # find register if present
            if len(tokens) > 1 and tokens[1] in REG:
                reg_code = REG[tokens[1]]
                # operand may be tokens[2]
                if len(tokens) > 2:
                    operand = tokens[2]
                else:
                    operand = None
            else:
                operand = tokens[1] if len(tokens) > 1 else None

            # format RG part
            rg_part = f"(RG, {reg_code})"
            is_part = f"(IS, {op_code})"

            # handle operand types
            if operand is None:
                intermediate.append(f"{is_part} {rg_part}")
            elif operand.startswith("='") and operand.endswith("'"):
                # literal
                lit = operand
                if lit not in literal_index:
                    literal_index[lit] = len(literal_index) + 1
                    literal_pool.append(lit)
                    literal_table[lit] = None
                intermediate.append(f"{is_part} {rg_part} (L, {literal_index[lit]})")
            elif re.match(r"^\d+$", operand):
                # constant
                intermediate.append(f"{is_part} {rg_part} (C, {operand})")
            else:
                # symbol
                sym = operand
                if sym not in symbol_index:
                    symbol_index[sym] = len(symbol_index) + 1
                    symbol_table[sym] = None
                intermediate.append(f"{is_part} {rg_part} (S, {symbol_index[sym]})")

            loc += 1

        # Declarative Statements
        elif opcode in DL:
            dl_code = DL[opcode]
            val = tokens[1] if len(tokens) > 1 else '0'
            intermediate.append(f"(DL, {dl_code}) (C, {val})")
            if opcode == 'DC':
                loc += 1
            elif opcode == 'DS':
                try:
                    loc += int(val)
                except ValueError:
                    pass

    # prepare output tables
    sym_lines = []
    for name, idx in sorted(symbol_index.items(), key=lambda x: x[1]):
        addr = symbol_table.get(name)
        sym_lines.append(f"{name} {addr if addr is not None else '-'}")

    lit_lines = []
    for lit, idx in sorted(literal_index.items(), key=lambda x: x[1]):
        addr = literal_table.get(lit)
        lit_lines.append(f"{lit} {addr if addr is not None else '-'}")

    write_lines(sym_file, sym_lines)
    write_lines(lit_file, lit_lines)
    write_lines(interm_file, intermediate)

    print(f"Pass-1 complete. Wrote {interm_file}, {sym_file}, {lit_file}.")


def pass2_assembler(interm_file: str = 'intermediate.txt',
                    sym_file: str = 'symbol_table.txt',
                    lit_file: str = 'literal_table.txt',
                    out_file: str = 'machine_code.txt') -> None:
    """Simple Pass-2: translate intermediate code into a basic machine code

    Machine code format (text): OPCODE RG ADDRESS/CONSTANT
    - OPCODE and RG are taken directly from the intermediate IS/RG fields.
    - ADDRESS is resolved from symbol/literal tables (index -> address).
    """
    # load symbol addresses (order in file corresponds to indices assigned in pass1)
    sym_addrs = []
    try:
        with open(sym_file, 'r') as f:
            for line in f:
                parts = line.split()
                if not parts:
                    continue
                addr = parts[1] if len(parts) > 1 else '-'
                sym_addrs.append(None if addr == '-' else int(addr))
    except FileNotFoundError:
        sym_addrs = []

    # load literal addresses
    lit_addrs = []
    try:
        with open(lit_file, 'r') as f:
            for line in f:
                parts = line.split()
                if not parts:
                    continue
                addr = parts[1] if len(parts) > 1 else '-'
                lit_addrs.append(None if addr == '-' else int(addr))
    except FileNotFoundError:
        lit_addrs = []

    # Declarative codes (used when emitting DC/DS machine lines)
    DL = {'DS': '01', 'DC': '02'}

    machine_lines = []
    # parse intermediate and produce machine code lines
    loc = 0
    with open(interm_file, 'r') as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            # extract parenthesized fields like 'IS, 04', 'RG, 01', 'L, 1', 'S, 2', 'C, 5'
            parts = [p.strip() for p in re.findall(r"\(([^)]+)\)", line)]
            # find IS/AD/DL/RG
            is_field = next((p for p in parts if p.startswith('IS,')), None)
            ad_field = next((p for p in parts if p.startswith('AD,')), None)
            dl_field = next((p for p in parts if p.startswith('DL,')), None)
            rg_field = next((p for p in parts if p.startswith('RG,')), None)

            # default values
            opcode = '00'
            rg = '00'
            addr = 0

            # AD handling: START may set loc
            if ad_field:
                # AD, xx
                kind, code = [x.strip() for x in ad_field.split(',', 1)]
                cfield = next((p for p in parts if p.startswith('C,')), None)
                if cfield and code == '01':  # START
                    try:
                        loc = int(cfield.split(',', 1)[1].strip())
                    except Exception:
                        loc = 0
                # skip AD lines in output
                continue

            if is_field:
                # IS, xx
                opcode = is_field.split(',', 1)[1].strip()
                if rg_field:
                    rg = rg_field.split(',', 1)[1].strip()

                # find operand field
                operand = None
                for p in parts:
                    if p.startswith(('L,', 'S,', 'C,')):
                        operand = p
                        break

                if operand is None:
                    addr = 0
                else:
                    kind, val = [x.strip() for x in operand.split(',', 1)]
                    if kind == 'L':
                        idx = int(val) - 1
                        addr = lit_addrs[idx] if 0 <= idx < len(lit_addrs) and lit_addrs[idx] is not None else 0
                    elif kind == 'S':
                        idx = int(val) - 1
                        addr = sym_addrs[idx] if 0 <= idx < len(sym_addrs) and sym_addrs[idx] is not None else 0
                    elif kind == 'C':
                        addr = int(val)

                machine_lines.append(f"{opcode} {rg} {addr}")
                loc += 1

            elif dl_field:
                # declarative - DL, xx (C, val)
                dl_code = dl_field.split(',', 1)[1].strip()
                cfield = next((p for p in parts if p.startswith('C,')), None)
                const = int(cfield.split(',', 1)[1].strip()) if cfield else 0
                # Output DL as: <DL_code> 00 <loc>  (opcode RG LC)
                machine_lines.append(f"{dl_code} 00 {loc}")
                # update loc according to DS/DC
                if dl_code == DL.get('DC'):
                    loc += 1
                else:
                    # DS - allocate block
                    try:
                        loc += int(const)
                    except Exception:
                        pass

            else:
                # unknown line or directives already handled
                continue

    write_lines(out_file, machine_lines)
    print(f"Pass-2 complete. Wrote {out_file} ({len(machine_lines)} lines).")

if __name__ == '__main__':
    in_file = sys.argv[1] if len(sys.argv) > 1 else 'code.asm'
    sym_file = sys.argv[2] if len(sys.argv) > 2 else 'symbol_table.txt'
    lit_file = sys.argv[3] if len(sys.argv) > 3 else 'literal_table.txt'
    interm_file = sys.argv[4] if len(sys.argv) > 4 else 'intermediate.txt'
	
    pass1_assembler(input_file=in_file, sym_file=sym_file, lit_file=lit_file, interm_file=interm_file)
    # Run pass-2 immediately to produce machine code
    try:
        pass2_assembler(interm_file=interm_file, sym_file=sym_file, lit_file=lit_file, out_file='machine_code.txt')
    except Exception as e:
        print(f"Pass-2 failed: {e}")
