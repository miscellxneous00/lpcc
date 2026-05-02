def tables(source_code):
    OP = {'STOP':('IS','00'), 'ADD':('IS','01') ,'SUB':('IS','02'), 'MULT':('IS','03'), 'MOVER':('IS','04'),'MOVEM':('IS','05'), 'CMP':('IS','06'), 'BC':('IS','07'), 'DIV':('IS','08'), 'READ':('IS','09'), 'PRINT':('IS','10') }

    AD = {'START':('AD','01'), 'END':('AD','02'), 'ORIGIN':('AD','03'), 'EQU':('AD','04'), 'LTORG':('AD','05')}

    DL = {'DC':('DL','01'),'DS':('DL','02')}

    REG = {'AREG':'1','BREG':'2','CREG':'3','DREG':'4'}

    COND = {'EQ':'1','LT':'2','GT':'3','LE':'4','GE':'5','ANY':'6'}

    sym_tab = {}  # {symbol : [index , addr]}
    lit_tab = []  # [ [lit , addr] ]
    pool_tab = [0]
    ic = []
    sym_index = 1
    lc=0

    lines = source_code.strip().split('\n')

    for line in lines:
        parts = line.replace(',',' ').split()
        if not parts : continue

        inter_code = []
        current_label = None

        # Labels
        if(parts[0] not in AD and parts[0] not in DL and parts[0] not in OP):
            current_label = parts[0]

            if current_label not in sym_tab:
                sym_tab[current_label] = [sym_index,lc]
                sym_index+=1
            else:
                sym_tab[current_label][1] = lc

            parts = parts[1:]

        mnenomic = parts[0]

        # AD
        if mnenomic in AD:

            inter_code.append(f"({AD[mnenomic][0]} , {AD[mnenomic][1]})")

            if mnenomic == 'START':
                lc = int(parts[1]) if len(parts) > 1 else 0
                if len(parts) > 1 : inter_code.append(f"(C , {lc})")
            
            elif mnenomic == 'END' or mnenomic == 'LTORG':
                for i in range(pool_tab[-1],len(lit_tab)):
                    lit_tab[i][1] = lc
                    lc+=1
                
                if mnenomic == 'LTORG':
                    pool_tab.append(len(lit_tab))
            
            elif mnenomic == 'ORIGIN':
                if parts[1] in sym_tab:
                    lc = sym_tab[parts[1]][1]
                else:
                    lc = int(parts[1])

                inter_code.append(f"(C , {lc})")
            
            elif mnenomic == 'EQU':
                target_address = sym_tab[parts[1]][1]

                if current_label and current_label in sym_tab:
                    sym_tab[current_label][1] = target_address

                inter_code.append(f"(C , {target_address})")
                
            ic.append(f"{'-':<5} | " + " ".join(inter_code))
            continue

        #DL
        if mnenomic in DL:
            inter_code.append(f"({DL[mnenomic][0]} , {DL[mnenomic][1]})")
            inter_code.append(f"(C , {parts[1]})")
            ic.append(f"{lc:<5} | " + " ".join(inter_code))

            if mnenomic == 'DC' : lc+=1
            elif mnenomic == 'DS' : lc+=int(parts[1])

            continue

        #OP
        if parts[0] in OP:
            inter_code.append(f"({OP[mnenomic][0]} , {OP[mnenomic][1]})")

            for op in parts[1:]:
                if op in REG:
                    inter_code.append(f"(R , {REG[op]})")
                elif op in COND:
                     inter_code.append(f"(C , {COND[op]})")
                elif op.startswith("='"):
                    lit_tab.append([op,-1])
                    inter_code.append(f"(L , {len(lit_tab)})")
                else:
                    if op not in sym_tab:
                        sym_tab[op] = [sym_index,-1]
                        sym_index += 1
                    inter_code.append(f"(S , {sym_tab[op][0]})")

            ic.append(f"{lc:<5} | " + " ".join(inter_code))
            lc += 1

    print("Symbol Table : ", sym_tab)
    print("Literal Table : ", lit_tab)
    print("Pool Table : ", pool_tab)

    print("--- INTERMEDIATE CODE ---")
    for line in ic: print(line)

sample_code2 = """
START 100
A DS 3
L1 MOVER AREG, B
ADD BREG, ='5'
LTORG
B DC 10
ORIGIN B
NEW EQU B
Z DC 1
STOP
END
"""

tables(sample_code2)

