import re

# Machine Opcode Table (MOT)
# Opcode: [Type, Opcode_Value, Length]
MOT = {
    "STOP": ["IS", "00", 1],
    "ADD": ["IS", "01", 1],
    "SUB": ["IS", "02", 1],
    "MOVR": ["IS", "03", 1],
    "MOVEM": ["IS", "04", 1],
    "COMP": ["IS", "05", 1],
    "BC": ["IS", "06", 1],
    "DIV": ["IS", "07", 1],
    "READ": ["IS", "08", 1],
    "PRINT": ["IS", "09", 1],
    "START": ["AD", "01", 0],
    "END": ["AD", "02", 0],
    "ORIGIN": ["AD", "03", 0],
    "EQU": ["AD", "04", 0],
    "LTORG": ["AD", "05", 0],
    "DS": ["DL", "01", 0],
    "DC": ["DL", "02", 0],
}

# Register Table
REG_TABLE = {
    "AREG": "1",
    "BREG": "2",
    "CREG": "3",
    "DREG": "4",
}

# Condition Code Table for BC instruction
CC_TABLE = {
    "LT": "1", "LE": "2", "EQ": "3", "GT": "4", "GE": "5", "ANY": "6"
}

# --- Global Tables for Pass I & II ---
symbol_table = []  # List of dictionaries: {"symbol": str, "address": int, "length": int, "defined": bool}
literal_table = [] # List of dictionaries: {"literal": str, "address": int}
pool_table = [0]   # List of integers: indices into literal_table where new pools start

# --- Helper Functions ---

def get_symbol_index(symbol, create_if_not_exists=False):
    """Returns index of symbol in symbol_table, optionally creating a placeholder."""
    for i, entry in enumerate(symbol_table):
        if entry["symbol"] == symbol:
            return i
    if create_if_not_exists:
        symbol_table.append({"symbol": symbol, "address": -1, "length": 0, "defined": False})
        return len(symbol_table) - 1
    return -1 # Symbol not found

def get_literal_index(literal, pool_start_index):
    """Returns index of literal in literal_table within the current pool, or adds it."""
    # Check if literal already exists in the current pool
    for i in range(pool_start_index, len(literal_table)):
        if literal_table[i]["literal"] == literal:
            return i
    # If not found, add it
    literal_table.append({"literal": literal, "address": -1})
    return len(literal_table) - 1

def evaluate_expression(expression, current_lc):
    """Evaluates expressions like 'SYMBOL + 5' or 'LC - 2'."""
    # Replace LC with its current value
    expr = str(expression).replace("LC", str(current_lc))

    # Replace symbols with their addresses
    for entry in symbol_table:
        if entry["defined"] and entry["symbol"] in expr:
            expr = expr.replace(entry["symbol"], str(entry["address"]))
    
    # Simple evaluation for now, can be extended for more complex expressions
    try:
        return eval(expr)
    except Exception as e:
        print(f"Error evaluating expression '{expression}': {e}")
        return None

# --- Pass I ---

def pass_one(source_file="source.asm",
             intermediate_file="intermediate.txt",
             st_file="symbol_table.txt",
             lt_file="literal_table.txt",
             pt_file="pool_table.txt"):

    lc = 0
    pool_start_index = 0
    intermediate_code = []

    print("\n--- Starting Pass I ---")

    with open(source_file, 'r') as f_in:
        for line_num, line in enumerate(f_in, 1):
            original_line = line.strip()
            if not original_line:
                continue

            parts = re.split(r'\s+', original_line)
            label = None
            opcode = None
            operands = []

            if parts[0] not in MOT and parts[0] not in REG_TABLE and not parts[0].startswith('='):
                label = parts[0]
                opcode = parts[1]
                operands = parts[2:]
            else:
                opcode = parts[0]
                operands = parts[1:]

            if label:
                sym_idx = get_symbol_index(label)
                if sym_idx != -1:
                    if symbol_table[sym_idx]["defined"]:
                        print(f"Error (Pass I, line {line_num}): Symbol '{label}' redefined.")
                    else:
                        symbol_table[sym_idx]["address"] = lc
                        symbol_table[sym_idx]["defined"] = True
                else:
                    symbol_table.append({"symbol": label, "address": lc, "length": 0, "defined": True})

            if opcode not in MOT:
                print(f"Error (Pass I, line {line_num}): Invalid opcode '{opcode}'.")
                continue

            op_info = MOT[opcode]
            op_type = op_info[0]
            op_value = op_info[1]
            op_length = op_info[2]

            ic_entry = {"lc": lc, "type": op_type, "value": op_value, "operands": []}

            if op_type == "AD": # Assembler Directives
                if opcode == "START":
                    if operands:
                        lc = int(operands[0])
                    ic_entry["operands"].append(("C", str(lc))) # Store start address
                elif opcode == "END":
                    for i in range(pool_start_index, len(literal_table)):
                        literal_table[i]["address"] = lc
                        intermediate_code.append({"lc": lc, "type": "DL", "value": MOT["DC"][1], "operands": [("L", i)]})
                        lc += 1
                    pool_table.append(len(literal_table)) # Mark end of last pool
                    intermediate_code.append(ic_entry) # Add END directive to IC
                    break # End of assembly
                elif opcode == "LTORG":
                    for i in range(pool_start_index, len(literal_table)):
                        literal_table[i]["address"] = lc
                        intermediate_code.append({"lc": lc, "type": "DL", "value": MOT["DC"][1], "operands": [("L", i)]})
                        lc += 1
                    pool_start_index = len(literal_table) # Start new pool
                    pool_table.append(pool_start_index)
                elif opcode == "ORIGIN":
                    if operands:
                        new_lc = evaluate_expression(operands[0], lc)
                        if new_lc is not None:
                            lc = new_lc
                            ic_entry["operands"].append(("C", str(lc)))
                elif opcode == "EQU":
                    if label and operands:
                        sym_idx = get_symbol_index(label)
                        if sym_idx != -1:
                            equ_value = evaluate_expression(operands[0], lc)
                            if equ_value is not None:
                                symbol_table[sym_idx]["address"] = equ_value
                                symbol_table[sym_idx]["defined"] = True
                                ic_entry["operands"].append(("S", sym_idx))
                                ic_entry["operands"].append(("C", str(equ_value)))
                        else:
                            print(f"Error (Pass I, line {line_num}): EQU label '{label}' not found.")
                    intermediate_code.append(ic_entry)
                    continue # Skip LC increment at end of loop for EQU

            elif op_type == "DL": # Declarative Statements
                if opcode == "DS":
                    if label and operands:
                        length = int(operands[0])
                        sym_idx = get_symbol_index(label)
                        if sym_idx != -1:
                            symbol_table[sym_idx]["length"] = length
                        ic_entry["operands"].append(("S", sym_idx))
                        ic_entry["operands"].append(("C", str(length)))
                        lc += length
                elif opcode == "DC":
                    if label and operands:
                        sym_idx = get_symbol_index(label)
                        symbol_table[sym_idx]["length"] = 1
                        ic_entry["operands"].append(("S", sym_idx))
                        ic_entry["operands"].append(("C", operands[0].strip("'\"")))
                        lc += 1

            elif op_type == "IS": # Imperative Statements
                for operand in operands:
                    operand = operand.strip(',')
                    if operand in REG_TABLE:
                        ic_entry["operands"].append(("REG", REG_TABLE[operand]))
                    elif operand.startswith('='): # Literal
                        lit_idx = get_literal_index(operand, pool_start_index)
                        ic_entry["operands"].append(("L", lit_idx))
                    elif operand in CC_TABLE: # Condition Code
                        ic_entry["operands"].append(("CC", CC_TABLE[operand]))
                    elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()): # Numeric Constant
                        ic_entry["operands"].append(("C", operand))
                    else: # Symbol
                        sym_idx = get_symbol_index(operand, create_if_not_exists=True)
                        ic_entry["operands"].append(("S", sym_idx))
                lc += op_length
            
            if opcode not in ["END", "LTORG", "EQU"]:
                intermediate_code.append(ic_entry)

    # Write Pass I outputs
    with open(intermediate_file, 'w') as f_ic:
        for entry in intermediate_code:
            op_str = f"({entry['type']}, {entry['value']})"
            ops_str = " ".join([f"({op_type}, {op_val})" for op_type, op_val in entry['operands']])
            f_ic.write(f"{entry['lc']} {op_str} {ops_str}\n")

    with open(st_file, 'w') as f_st:
        f_st.write("Symbol | Address | Length | Defined\n")
        f_st.write("----------------------------------\n")
        for entry in symbol_table:
            f_st.write(f"{entry['symbol']:<6} | {entry['address']:<7} | {entry['length']:<6} | {entry['defined']}\n")

    with open(lt_file, 'w') as f_lt:
        f_lt.write("Literal | Address\n")
        f_lt.write("-----------------\n")
        for entry in literal_table:
            f_lt.write(f"{entry['literal']:<7} | {entry['address']}\n")

    with open(pt_file, 'w') as f_pt:
        f_pt.write("Pool_Start_Index\n")
        f_pt.write("----------------\n")
        for index in pool_table:
            f_pt.write(f"{index}\n")

    print("Pass I Complete. Outputs written to files.")

# --- Pass II ---

def pass_two(intermediate_file="intermediate.txt",
             st_file="symbol_table.txt",
             lt_file="literal_table.txt",
             pt_file="pool_table.txt",
             object_file="object_code.txt",
             listing_file="listing.txt",
             source_file="source.asm"):

    print("\n--- Starting Pass II ---")

    # Reload tables (in a real scenario, these would be passed or loaded from files)
    # For this example, we'll assume pass_one was just run and tables are in memory.
    # If running pass_two independently, you'd need to load them here.

    # Read source lines for listing file
    with open(source_file, 'r') as f_src:
        source_lines = [line.strip() for line in f_src if line.strip()]

    object_code_output = []
    listing_output = []
    source_line_idx = 0 # To match source lines with intermediate code lines

    with open(intermediate_file, 'r') as f_ic:
        for ic_line in f_ic:
            ic_line = ic_line.strip()
            if not ic_line: continue

            match = re.match(r'(\d+)\s+\((\w+),\s*(\w+)\)(.*)', ic_line)
            if not match:
                print(f"Error (Pass II): Could not parse intermediate code line: {ic_line}")
                continue

            lc_str, op_type, op_value, operands_str = match.groups()
            lc = int(lc_str)

            parsed_operands = []
            if operands_str:
                op_matches = re.findall(r'\((\w+),\s*([^\)]+)\)', operands_str)
                for op_type_val, op_val_str in op_matches:
                    parsed_operands.append((op_type_val, op_val_str))

            machine_code = ""
            listing_line = f"{lc:03d} "

            current_source_line = source_lines[source_line_idx] if source_line_idx < len(source_lines) else ""
            if op_type in ["IS", "DL"] or (op_type == "AD" and MOT[op_value][0] in ["START", "END", "ORIGIN", "LTORG"]):
                 if not (op_type == "AD" and MOT[op_value][0] == "EQU"): # EQU doesn't consume a source line in the same way
                     source_line_idx += 1

            if op_type == "IS":
                opcode_mc = op_value
                reg_mc = "0"
                addr_mc = "000"

                if parsed_operands:
                    op1_type, op1_val = parsed_operands[0]
                    if op1_type == "REG":
                        reg_mc = op1_val
                    elif op1_type == "CC": # For BC instruction
                        reg_mc = op1_val # Condition code goes in 'reg' field
                    elif op1_type == "C": # For instructions like READ/PRINT that take a constant
                        addr_mc = f"{int(op1_val):03d}" # Direct constant value

                    if len(parsed_operands) > 1:
                        op2_type, op2_val = parsed_operands[1]
                        target_addr = -1
                        if op2_type == "S":
                            sym_idx = int(op2_val)
                            target_addr = symbol_table[sym_idx]["address"]
                        elif op2_type == "L":
                            lit_idx = int(op2_val)
                            target_addr = literal_table[lit_idx]["address"]
                        elif op2_type == "C":
                            target_addr = int(op2_val) # Direct constant address
                        
                        if target_addr != -1:
                            addr_mc = f"{target_addr:03d}"
                        else:
                            print(f"Error (Pass II, LC {lc}): Undefined symbol/literal address for operand '{op2_val}'.")
                            addr_mc = "ERR" # Indicate error in machine code

                machine_code = f"{opcode_mc}{reg_mc}{addr_mc}"
                object_code_output.append(f"{lc:03d} {machine_code}")
                listing_line += f"{machine_code:<10} {current_source_line}"

            elif op_type == "DL": # Declarative Statements
                if MOT[op_value][0] == "DC":
                    constant_val_str = parsed_operands[1][1] if len(parsed_operands) > 1 else "0"
                    
                    if parsed_operands[0][0] == "L":
                        lit_idx = int(parsed_operands[0][1])
                        constant_val_str = literal_table[lit_idx]["literal"].strip("='") # Remove =' and '
                    
                    try:
                        if constant_val_str.isdigit() or (constant_val_str.startswith('-') and constant_val_str[1:].isdigit()):
                            machine_code = f"{int(constant_val_str):06d}" # 6 digits for constant
                        elif len(constant_val_str) == 1: # Single character
                            machine_code = f"{ord(constant_val_str):06d}" # ASCII value
                        else: # Fallback for other strings
                            machine_code = "000000" # Default or error
                    except ValueError:
                        print(f"Warning (Pass II, LC {lc}): Could not convert '{constant_val_str}' to numeric for DC.")
                        machine_code = "000000"

                    object_code_output.append(f"{lc:03d} {machine_code}")
                    listing_line += f"{machine_code:<10} {current_source_line}"

                elif MOT[op_value][0] == "DS":
                    length = int(parsed_operands[1][1]) if len(parsed_operands) > 1 else 1
                    listing_line += f"{'':<10} {current_source_line} (Reserves {length} words)"

            elif op_type == "AD": # Assembler Directives
                if MOT[op_value][0] == "START":
                    listing_line += f"{'':<10} {current_source_line} (Start address: {lc})"
                elif MOT[op_value][0] == "END":
                    listing_line += f"{'':<10} {current_source_line} (End of program)"
                elif MOT[op_value][0] == "LTORG":
                    listing_line += f"{'':<10} {current_source_line} (Literal Pool Origin)"
                elif MOT[op_value][0] == "ORIGIN":
                    listing_line += f"{'':<10} {current_source_line} (LC set to {lc})"
                elif MOT[op_value][0] == "EQU":
                    sym_idx = int(parsed_operands[0][1])
                    equ_val = parsed_operands[1][1]
                    listing_line += f"{'':<10} {current_source_line} ({symbol_table[sym_idx]['symbol']} = {equ_val})"
            
            listing_output.append(listing_line)

    # Write Pass II outputs
    with open(object_file, 'w') as f_obj:
        for line in object_code_output:
            f_obj.write(line + '\n')

    with open(listing_file, 'w') as f_list:
        f_list.write("LC   Machine Code Source Line\n")
        f_list.write("--------------------------------------------------\n")
        for line in listing_output:
            f_list.write(line + '\n')

    print("Pass II Complete. Outputs written to files.")


# --- Main Execution ---
if __name__ == "__main__":

    pass_one()
    pass_two()