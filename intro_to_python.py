#! /usr/bin/python

# Assignment is easy:
x = 7
y = 3
z = "bob"
x = z

# Functions are easy:
def sum(a, b):
    return a + b
c = sum(5, 3)


def say_something(message = "hello"):
    print message
say_something("I like frogs")
say_something()


# Python has a few simple but flexible datatypes.

# Sequence types:
# A list is a mutable series of values of any type
my_list = []
my_list.append(1)
# Won't work:
my_list[1] = "cactus"
my_list.append("blah")
my_list[1] = "cactus"
my_list.append(["turtle", True, None, 27])
my_list.append("hot dogs")
my_list.reverse()
my_list.pop()
# its easy to test if something is a member of a sequence:
"cactus" in my_list

my_list

# A tuple is an immutable (as in, un-modifiable) series of values.
my_tup = (1, 7)
my_tup = (x, y)

# won't work:
my_tup[0] = "I do what I want"

# Strings are indexable like a sequence, but immutable:
this_str = "hueXhue hue hue hue"
this_str[3]
this_str = this_str.upper()
this_str.split() # we can split strings into groups of substrings
this_str.split('e')

# Mapping type: Dictionary (aka hash map) is a mutable type which is unordered
# It's key -> value pairs.  Keys must be hashable (and thus, immutable!)
a_dict = {}
a_dict['muh key'] = 'muh stuff'
a_dict[this_str.split()] = "won't work!"
a_dict[tuple(this_str.split())] = "this does though!"

# you can get a list of dictionary keys, or values, or both:
a_dict.keys() # returns a list [k1, k2, k3...]
a_dict.values() # returns a list [v1, v2, v3...]
a_dict.items() # returns a list of tuples! [(k1,v1), (k2,v2), ...]

# looping is very refreshing in Python.
# There is no c-style for (int i = 0; i<= n; i++)... just a foreach loop
for item in my_list:
    print item
# works for any sequence type!

# you can even loop neatly over pairs
for key, value in a_dict.items():
    print key, value
# note, for big dictionaries, iteritems() is faster and more efficient!

# using a dictionary in a list-context returns a list of keys.
for key in a_dict:
    print key
# functionally the same as typing a_dict.keys(), but actually faster!

# if you really need to have an index as you loop, you can:
for index, item in enumerate(my_list):
    print index, item

must_watch_python_videos = [
    'https://github.com/s16h/py-must-watch',
]
