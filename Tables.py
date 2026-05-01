def pass_one_assembler(source_code):
    # Dictionaries for our Mnemonics (Standard format)
    OPTAB = {
        'STOP': ('IS', '00'), 'ADD': ('IS', '01'), 'SUB': ('IS', '02'), 
        'MULT': ('IS', '03'), 'MOVER': ('IS', '04'), 'MOVEM': ('IS', '05'),
        'COMP': ('IS', '06'), 'BC': ('IS', '07'), 'DIV': ('IS', '08'), 
        'READ': ('IS', '09'), 'PRINT': ('IS', '10')
    }
    AD = {'START': ('AD', '01'), 'END': ('AD', '02'), 'ORIGIN': ('AD', '03'), 'EQU': ('AD', '04'), 'LTORG': ('AD', '05')}
    DL = {'DC': ('DL', '01'), 'DS': ('DL', '02')}
    REG = {'AREG': '1', 'BREG': '2', 'CREG': '3', 'DREG': '4'}
    COND = {'EQ': '1', 'LT': '2', 'GT': '3', 'LE': '4', 'GE': '5', 'ANY': '6'}

    # Data Structures required for the output
    symtab = {}       # Symbol Table: {Symbol: [Address, Index]}
    littab = []       # Literal Table: [[Literal, Address]]
    pooltab = [0]     # Pool Table: [Start Index of Literals]
    ic = []           # Intermediate Code
    
    lc = 0            # Location Counter
    sym_index = 1

    lines = source_code.strip().split('\n')

    for line in lines:
        parts = line.replace(',', ' ').split()
        if not parts: continue
        
        intermediate_line = []
        
        # 1. Handle Label (Symbol)
        if parts[0] not in OPTAB and parts[0] not in AD and parts[0] not in DL:
            label = parts[0]
            if label not in symtab:
                symtab[label] = [lc, sym_index]
                sym_index += 1
            else:
                symtab[label][0] = lc # Update address if already present
            parts = parts[1:] # Move to the next part of the instruction

        if not parts: continue
        mnemonic = parts[0]

        # 2. Handle Assembler Directives (AD)
        if mnemonic in AD:
            intermediate_line.append(f"({AD[mnemonic][0]}, {AD[mnemonic][1]})")
            
            if mnemonic == 'START':
                lc = int(parts[1]) if len(parts) > 1 else 0
                if len(parts) > 1: intermediate_line.append(f"(C, {parts[1]})")
            
            elif mnemonic == 'END' or mnemonic == 'LTORG':
                # Assign addresses to unassigned literals
                for i in range(pooltab[-1], len(littab)):
                    littab[i][1] = lc
                    lc += 1
                if mnemonic == 'LTORG':
                    pooltab.append(len(littab))
            
            ic.append(f"{'-':<5} | " + " ".join(intermediate_line))
            continue

        # 3. Handle Declarative Statements (DL)
        elif mnemonic in DL:
            intermediate_line.append(f"({DL[mnemonic][0]}, {DL[mnemonic][1]})")
            intermediate_line.append(f"(C, {parts[1]})")
            ic.append(f"{lc:<5} | " + " ".join(intermediate_line))
            
            if mnemonic == 'DS': lc += int(parts[1])
            elif mnemonic == 'DC': lc += 1
            continue

        # 4. Handle Imperative Statements (IS)
        elif mnemonic in OPTAB:
            intermediate_line.append(f"({OPTAB[mnemonic][0]}, {OPTAB[mnemonic][1]})")
            
            for op in parts[1:]:
                if op in REG:
                    intermediate_line.append(f"(R, {REG[op]})")
                elif op in COND:
                    intermediate_line.append(f"(C, {COND[op]})")
                elif op.startswith("='"): # It's a Literal
                    littab.append([op, -1]) # -1 means address not yet assigned
                    intermediate_line.append(f"(L, {len(littab)})")
                else: # It's a Symbol
                    if op not in symtab:
                        symtab[op] = [-1, sym_index] # -1 means address not yet assigned
                        sym_index += 1
                    intermediate_line.append(f"(S, {symtab[op][1]})")
            
            ic.append(f"{lc:<5} | " + " ".join(intermediate_line))
            lc += 1

    # Print Outputs
    print("--- INTERMEDIATE CODE ---")
    for line in ic: print(line)
    
    print("\n--- SYMBOL TABLE ---")
    print(f"{'Index':<10} | {'Symbol':<10} | {'Address':<10}")
    for sym, data in symtab.items(): print(f"{data[1]:<10} | {sym:<10} | {data[0]:<10}")
        
    print("\n--- LITERAL TABLE ---")
    print(f"{'Index':<10} | {'Literal':<10} | {'Address':<10}")
    for i, lit in enumerate(littab): print(f"{i:<10} | {lit[0]:<10} | {lit[1]:<10}")
        
    print("\n--- POOL TABLE ---")
    print(pooltab)
    # print(f"{'Index':<10} | {'Literal_Index':<10}")
    # for i, p in enumerate(pooltab): print(f"{i:<10} | {p:<10}")

# Example Assembly Code
sample_code = """
START   200
        MOVER   AREG, ='5'
        MOVER   BREG, ='6'
        ADD     AREG, BREG
        LTORG
A       DS      1
B       DS      2
        MOVER   CREG, ='3'
        MOVEM   CREG, A
        STOP
        END
"""

pass_one_assembler(sample_code)
