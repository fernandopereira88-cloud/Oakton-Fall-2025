from collections import Counter

# From a list
my_list = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
fruit_counts = Counter(my_list)
print(fruit_counts)

# From a string
word = "mississippi"
letter_counts = Counter(word)
print(letter_counts)

# From a dictionary
initial_counts = {'a': 2, 'b': 3}
my_counter = Counter(initial_counts)
print(my_counter)