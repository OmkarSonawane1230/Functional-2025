# MacroProcessor.py
# Implements Pass-I and Pass-II of a two-pass macro processor
# Input: code2.asm
# Output: mnt.txt, mdt.txt, intermediate_macro.txt, expanded_code.asm

class MNTEntry:
    def __init__(self, name, mdt_index):
        self.name = name
        self.mdt_index = mdt_index

class MDTEntry:
    def __init__(self, line):
        self.line = line

class MacroProcessor:
    def pass3(self, expanded_file, machine_file):
        # Example opcode/register mappings
        OPCODES = {'START': '00', 'END': '00', 'DC': '02', 'INCR': '01'}
        REGISTERS = {'X': '01', 'Y': '02'}
        # Symbol table for addresses
        symbol_table = {}
        # First pass: collect symbol addresses
        lines = []
        with open(expanded_file, 'r') as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith('END'):
                    continue
                tokens = line.split()
                if len(tokens) == 3 and tokens[1] == 'DC':
                    symbol_table[tokens[0]] = tokens[2]
                lines.append(line)
        # Second pass: generate machine code
        with open(machine_file, 'w') as f:
            for line in lines:
                tokens = line.split()
                if not tokens:
                    continue
                if tokens[0] == 'START':
                    f.write(f"00 00 {tokens[1]}\n")
                elif len(tokens) == 3 and tokens[1] == 'DC':
                    # DC statement
                    f.write(f"02 00 {tokens[2]}\n")
                elif tokens[0] == 'END':
                    f.write("00 00 0\n")
                elif tokens[0] == 'INCR':
                    # Macro expansion, assume INCR <symbol>
                    reg = REGISTERS.get(tokens[1], '00')
                    addr = symbol_table.get(tokens[1], '00')
                    f.write(f"01 {reg} {addr}\n")
                else:
                    f.write("00 00 0\n")
    def __init__(self):
        self.mnt = []
        self.mdt = []
        self.intermediate = []

    def pass1(self, input_file, mnt_file, mdt_file, interm_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()
        in_macro = False
        mdt_index = 0
        macro_name = None
        for line in lines:
            line = line.split(';')[0].strip()
            if not line:
                continue
            if line.startswith('MACRO'):
                in_macro = True
                continue
            if in_macro:
                if macro_name is None:
                    tokens = line.split()
                    macro_name = tokens[0]
                    self.mnt.append(MNTEntry(macro_name, mdt_index))
                self.mdt.append(MDTEntry(line))
                mdt_index += 1
                if line == 'MEND':
                    in_macro = False
                    macro_name = None
                continue
            self.intermediate.append(line)
        # Write MNT
        with open(mnt_file, 'w') as f:
            for entry in self.mnt:
                f.write(f"{entry.name} {entry.mdt_index}\n")
        # Write MDT
        with open(mdt_file, 'w') as f:
            for entry in self.mdt:
                f.write(f"{entry.line}\n")
        # Write intermediate code
        with open(interm_file, 'w') as f:
            for s in self.intermediate:
                f.write(f"{s}\n")

    def pass2(self, interm_file, mnt_file, mdt_file, output_file):
        # Load MNT
        mnt_map = {}
        with open(mnt_file, 'r') as f:
            for line in f:
                tokens = line.strip().split()
                if len(tokens) >= 2:
                    mnt_map[tokens[0]] = int(tokens[1])
        # Load MDT
        mdt_lines = []
        with open(mdt_file, 'r') as f:
            mdt_lines = [line.rstrip('\n') for line in f]
        # Expand macros in intermediate code
        with open(interm_file, 'r') as f:
            interm_lines = f.readlines()
        with open(output_file, 'w') as f:
            for line in interm_lines:
                line = line.strip()
                if not line:
                    continue
                tokens = line.split(None, 1)
                macro_call = tokens[0]
                if macro_call in mnt_map:
                    idx = mnt_map[macro_call]
                    for i in range(idx + 1, len(mdt_lines)):
                        macro_line = mdt_lines[i]
                        if macro_line == 'MEND':
                            break
                        if len(tokens) > 1:
                            macro_line = macro_line.replace('&', tokens[1])
                        f.write(macro_line + '\n')
                else:
                    f.write(line + '\n')

if __name__ == '__main__':
    input_file = 'code2.asm'
    mnt_file = 'mnt.txt'
    mdt_file = 'mdt.txt'
    interm_file = 'intermediate_macro.txt'
    output_file = 'expanded_code.asm'
    mp = MacroProcessor()
    mp.pass1(input_file, mnt_file, mdt_file, interm_file)
    print('Pass-I complete. MNT, MDT, and intermediate code generated.')
    mp.pass2(interm_file, mnt_file, mdt_file, output_file)
    print('Pass-II complete. Macro expansion done. See expanded_code.asm.')
    mp.pass3(output_file, 'machine_code.txt')
    print('Pass-III complete. Machine code generated in machine_code.txt.')
