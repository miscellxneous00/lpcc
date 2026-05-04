def main():
    # 1. THE INPUT CODE (Stored inside the file directly)
    source_code = """
MACRO
INCR &X, &Y
MOVER AREG, &X
ADD AREG, &Y
MOVEM AREG, &X
MEND

MACRO
DOUBLE_INCR &A, &B
INCR &A, &B
INCR &A, &B
MEND

START 100
READ N1
READ N2
DOUBLE_INCR N1, N2
STOP
N1 DS 1
N2 DS 1
END
"""

    # --- DATA STRUCTURES ---
    MNT = {}                # Macro Name Table (Name -> MDT Index)
    MDT = []                # Macro Definition Table
    intermediate_code = []  # Code after Pass 1
    final_code = []         # Final Output

    # Split the multi-line string into a list of lines
    lines = source_code.strip().split('\n')

    # --- PASS 1: DEFINITION & EARLY EXPANSION ---
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line: # Skip empty lines
            i += 1
            continue
        
        words = line.split()

        if words[0] == "MACRO":
            i += 1
            # Get Macro Name and its arguments
            def_line = lines[i].strip().replace(',', ' ').split()
            macro_name = def_line[0]
            dummy_args = def_line[1:] 

            # Add to MNT
            MNT[macro_name] = len(MDT)

            i += 1
            # Read lines until MEND
            while lines[i].strip() != "MEND":
                body_line = lines[i].strip()
                
                # 1. Replace parent's dummy arguments (&A) with markers (#1)
                for idx, arg in enumerate(dummy_args):
                    body_line = body_line.replace(arg, f"#{idx+1}")
                
                # Check for Nested Macro Call (Early Expansion)
                check_words = body_line.replace(',', ' ').split()
                if check_words and check_words[0] in MNT:
                    nested_name = check_words[0]
                    nested_args = check_words[1:] # e.g., ['#1', '#2']
                    nested_mdt_idx = MNT[nested_name]
                    
                    # Fetch and expand the nested macro's code right now
                    while MDT[nested_mdt_idx] != "MEND":
                        nested_inst = MDT[nested_mdt_idx]
                        
                        # Replace the nested macro's markers with the parent's markers
                        for idx, act_arg in enumerate(nested_args):
                            nested_inst = nested_inst.replace(f"#{idx+1}", act_arg)
                            
                        MDT.append(nested_inst)
                        nested_mdt_idx += 1
                else:
                    # Normal instruction, just add to MDT
                    MDT.append(body_line)
                i += 1
            
            MDT.append("MEND")
        else:
            # Not part of a macro definition, goes to intermediate code
            intermediate_code.append(line)
        i += 1

    # --- PASS 2: FINAL MACRO EXPANSION ---
    # (Notice how Pass 2 hasn't changed at all! The nesting was already handled)
    for line in intermediate_code:
        words = line.replace(',', ' ').split()
        
        if words and words[0] in MNT:
            macro_name = words[0]
            actual_args = words[1:]
            mdt_index = MNT[macro_name]
            
            while MDT[mdt_index] != "MEND":
                instruction = MDT[mdt_index]
                for idx, act_arg in enumerate(actual_args):
                    instruction = instruction.replace(f"#{idx+1}", act_arg)
                final_code.append(instruction)
                mdt_index += 1
        else:
            final_code.append(line)

    # --- PRINTING THE OUTPUTS ---
    print("--- Macro Name Table (MNT) ---")
    for name, idx in MNT.items():
        print(f"Name: {name} \t MDT Index: {idx}")

    print("\n--- Macro Definition Table (MDT) ---")
    for idx, instruction in enumerate(MDT):
        print(f"{idx} \t {instruction}")

    print("\n--- Final Expanded Code (Pass 2 Output) ---")
    for line in final_code:
        print(line)

if __name__ == "__main__":
    main()