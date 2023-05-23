def find_local_extrema(numbers):
    extrema = []
    n = len(numbers)
    
    # Include the first number in the list as a local extremum
    extrema.append(numbers[0])
    
    # Iterate over the numbers, excluding the first and last ones
    for i in range(1, n - 1):
        # Check if the current number is a local extremum
        if (numbers[i] >= numbers[i-1] and numbers[i] >= numbers[i+1]) or \
           (numbers[i] <= numbers[i-1] and numbers[i] <= numbers[i+1]):
            if extrema[-1] != numbers[i]:
                extrema.append(numbers[i])
    
    # Include the last number in the list as a local extremum
    
    extrema.append(numbers[-1])
    
    return extrema


with open("logs/20232205_21h20m_balance.txt", "r") as file:
# with open("logs/20232205_21h20m_sequence.txt", "r") as file:
    # Read the lines and store them in an array
    original_sequence = [float(x) for x in file.readlines()]
    # original_sequence = list(original_sequence)

original_sequence = [185, 200, 185, 200, 160, 215, 210]
extrema = find_local_extrema(original_sequence)
print(extrema)  # Output: [200, 185, 215, 210]

max_fall = 0
if extrema[0] > extrema[1]:
    i = 0
    while i < len(extrema)-1:
        fall = extrema[i] - extrema[i+1]
        if fall > max_fall:
            max_fall = fall
        i = i + 2
        print('a')
else:
    i = 1
    while i < len(extrema)-1:
        fall = extrema[i] - extrema[i+1]
        if fall > max_fall:
            max_fall = fall
        i = i + 2

print(max_fall)