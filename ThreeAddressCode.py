def generate_three_address_code(expression):
    # 1. Define the priority of our math operators (BODMAS logic)
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    operators = set(['+', '-', '*', '/'])

    print(f"--- Generating TAC for: {expression} ---")

    # ---------------------------------------------------------
    # PHASE 1: Convert Infix (normal math) to Postfix
    # ---------------------------------------------------------
    postfix = []
    operator_stack = []

    # Remove blank spaces to make reading the string easier
    expression = expression.replace(" ", "")

    for char in expression:
        # If it's a variable or number (like 'a' or '5'), add directly to postfix
        if char.isalnum(): 
            postfix.append(char)
            
        # If it's an opening bracket, push to stack
        elif char == '(':
            operator_stack.append(char)
            
        # If it's a closing bracket, pop everything until the opening bracket
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                postfix.append(operator_stack.pop())
            operator_stack.pop() # Remove the '(' from the stack
            
        # If it's an operator (+, -, *, /)
        elif char in operators:
            # Check precedence to maintain correct math order
            while (operator_stack and operator_stack[-1] != '(' and 
                   precedence.get(operator_stack[-1], 0) >= precedence.get(char, 0)):
                postfix.append(operator_stack.pop())
            operator_stack.append(char)

    # Empty any remaining operators from the stack
    while operator_stack:
        postfix.append(operator_stack.pop())


    # ---------------------------------------------------------
    # PHASE 2: Generate TAC from the Postfix expression
    # ---------------------------------------------------------
    tac_stack = []
    temp_variable_counter = 1

    print("Generated Code:")
    for char in postfix:
        # If it's a variable/number, push to our new stack
        if char.isalnum(): 
            tac_stack.append(char)
            
        # If it's an operator, it's time to generate an instruction
        elif char in operators: 
            # Pop the top two variables from the stack
            right_operand = tac_stack.pop()
            left_operand = tac_stack.pop()

            # Create a temporary variable name (t1, t2, t3...)
            temp_var = f"t{temp_variable_counter}"
            temp_variable_counter += 1

            # Print the actual Three Address Code line
            print(f"{temp_var} = {left_operand} {char} {right_operand}")

            # Push the temporary variable back onto the stack for the next calculation
            tac_stack.append(temp_var)
    print("\n")

# --- EXECUTION AREA ---
# You can change these equations to whatever your evaluator asks for.
equation_1 = "a + b * c"
generate_three_address_code(equation_1)

equation_2 = "(a + b) * (c - d)"
generate_three_address_code(equation_2)



