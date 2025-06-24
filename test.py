cat > test_bug.py << 'EOF'
def calculate_average(numbers)  # Missing colon
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

result = calculate_average([1, 2, 3, 4, 5])
print(f"Average is: {result}"  # Missing closing parenthesis

print(undefined_variable)
EOF