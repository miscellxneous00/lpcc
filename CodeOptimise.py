def optimize_tac(tac_lines):
    print("--- Original Code ---")
    for line in tac_lines:
        print(line)
        
    print("\n--- Applying Optimizations ---")
    optimized_code = []
    
    known_constants = {} 
    computed_exprs = {}   #  Dictionary for CSE
    
    for line in tac_lines:
        parts = line.split()
        
        if len(parts) == 3:
            result = parts[0]
            val = parts[2]
            
            if val.isdigit():
                known_constants[result] = val
                print(f"Tracking Constant: Recognized {result} is always {val}")
                
            optimized_code.append(line)
            continue
            
        if len(parts) == 5:
            result = parts[0]
            arg1 = parts[2]
            operator = parts[3]
            arg2 = parts[4]
            
            # 0: Constant Propagation
            propagated = False
            if arg1 in known_constants:
                arg1 = known_constants[arg1]
                propagated = True
            if arg2 in known_constants:
                arg2 = known_constants[arg2]
                propagated = True
                
            if propagated:
                new_line = f"{result} = {arg1} {operator} {arg2}"
                print(f"Constant Propagation: {line}  -->  {new_line}")
                line = new_line 
            
            # 1: Constant Folding
            if arg1.isdigit() and arg2.isdigit():
                val1 = int(arg1)
                val2 = int(arg2)
                # Prevent divide by zero error during folding!
                if operator == '/' and val2 == 0:
                    pass 
                else:
                    if operator == '+': ans = val1 + val2
                    elif operator == '-': ans = val1 - val2
                    elif operator == '*': ans = val1 * val2
                    elif operator == '/': ans = val1 // val2
                    elif operator == '^': ans = val1 ** val2
                    
                    optimized_code.append(f"{result} = {ans}")
                    known_constants[result] = str(ans) 
                    print(f"Constant Folding: {line}  -->  {result} = {ans}")
                    continue
                
            # 2: Algebraic Simplification
            if (operator == '+' and arg2 == '0') or (operator == '-' and arg2 == '0'):
                optimized_code.append(f"{result} = {arg1}")
                print(f"Algebraic Simplification: {line}  -->  {result} = {arg1}")
                continue
                
            if (operator == '*' and arg2 == '1') or (operator == '/' and arg2 == '1'):
                optimized_code.append(f"{result} = {arg1}")
                print(f"Algebraic Simplification: {line}  -->  {result} = {arg1}")
                continue

            # Annihilation (Multiplication by Zero)
            if operator == '*' and (arg2 == '0' or arg1 == '0'):
                optimized_code.append(f"{result} = 0")
                print(f"Algebraic Simplification: {line}  -->  {result} = 0")
                known_constants[result] = '0'
                continue

            # 3: Strength Reduction
            if operator == '*' and arg2 == '2':
                optimized_code.append(f"{result} = {arg1} + {arg1}")
                print(f"Strength Reduction: {line}  -->  {result} = {arg1} + {arg1}")
                continue
                
            if operator == '^' and arg2 == '2':
                optimized_code.append(f"{result} = {arg1} * {arg1}")
                print(f"Strength Reduction: {line}  -->  {result} = {arg1} * {arg1}")
                continue

            # 4: Common Subexpression Elimination (CSE)
            key = f"{arg1} {operator} {arg2}"
            if key in computed_exprs:    
                optimized_code.append(f"{result} = {computed_exprs[key]}")
                print(f"Common Subexpression: {line}  -->  {result} = {computed_exprs[key]}")
                continue # Skip to next line so we don't append the original
            else:    
                computed_exprs[key] = result
                # Note: We don't 'continue' here, so it falls down and appends the line
        
        # Fallback: if no optimizations matched (or if it's the first time seeing an expression)
        optimized_code.append(line)
        
    print("\n--- Final Optimized Code ---")
    for line in optimized_code:
        print(line)

# --- EXECUTION AREA ---
sample_code = [
    "t1 = 10 * 5",      
    "t2 = t1 - 0",       # Should trigger Algebraic Simplification
    "t3 = 2 ^ 2",        # Should trigger Strength Reduction
    "t4 = y / 1",        # Should trigger Algebraic Simplification
    "t5 = t2 + t3"      
]
optimize_tac(sample_code)
