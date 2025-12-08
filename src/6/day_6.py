import string
import pandas as pd
from math import prod


with open('file.txt', 'r') as file:
    lines = file.readlines()

df = pd.read_csv('file.txt', sep=r'\s+', engine='python', 
                 header=None,  # No header row
                 on_bad_lines='warn')

df_transposed = df.T.head()  # Get fresh copy from original df

row_sums = []

for i, row in df_transposed.iterrows():
    operator = row[4]
    row_sum = 1 if operator == '*' else 0
    print(f"Initial row_sum: {row_sum}")

    for j, col in enumerate(row):
        # Skip the operator column AND any existing row_sum column
        if j == 4 or (isinstance(col, str) and col == 'row_sum'):
            continue
            
        if str(col).isdigit() or (isinstance(col, (int, float)) and not pd.isna(col)):
            col_val = int(col) if str(col).isdigit() else int(col)
            
            if operator == '*':
                row_sum *= col_val
            else: 
                row_sum += col_val

    row_sums.append(row_sum)
    print(f"Row {i}: operator='{operator}', sum={row_sum}")

# Add the row_sum column
df_transposed['row_sum'] = row_sums
print(df_transposed)


# Check first few columns in detail
results = []
current_problem_numbers = []
current_operator = None

for col_idx, column in enumerate(zip(*lines)):
    if col_idx >= 20:  # Just check first 20 columns
        break
        
    # Check if all whitespace
    is_whitespace = all(c in string.whitespace for c in column)
    
    if is_whitespace:
        print(f'Column {col_idx}: WHITESPACE SEPARATOR')
        if current_operator and current_problem_numbers:
            print(f'  -> Processing problem: {current_problem_numbers} {current_operator}')
            if current_operator == '+':
                result = sum(current_problem_numbers)
            elif current_operator == '*':
                result = prod(current_problem_numbers)
            else:
                result = 0
            results.append(result)
            print(f'  -> Result: {result}')
        else:
            print(f'  -> Skipping (operator={current_operator}, numbers={current_problem_numbers})')
        
        # Reset
        current_problem_numbers.clear()
        current_operator = None
        continue
    
    # Extract content
    *number_chars, op_char = column
    
    # Check operator
    if op_char.strip() in '+*-/':
        current_operator = op_char.strip()
        print(f'Column {col_idx}: Found operator {current_operator}')
    
    # Extract number
    digit_chars = [c for c in number_chars if c in string.digits]
    if digit_chars:
        number = int(''.join(digit_chars))
        current_problem_numbers.append(number)
        print(f'Column {col_idx}: Added number {number}')

print(f'Final state: operator={current_operator}, numbers={current_problem_numbers}')
print(f'Total results so far: {len(results)}')