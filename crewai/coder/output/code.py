The python code for the assignment is:
```python
def calculate_series(n_terms):
    total = 0.0
    for i in range(n_terms):
        term = (-1)**i / (2 * i + 1)
        total += term
    return total * 4

# Calculate the first 10,000 terms
result = calculate_series(10000)
print(f'The result of the series multiplied by 4 is: {result}')
```
The output of the code is:
```
The result of the series multiplied by 4 is: 3.1414926535900345
```