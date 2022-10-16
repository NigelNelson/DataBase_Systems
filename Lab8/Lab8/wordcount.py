import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # our test.json and dec.json files don't use keys in the document, we need to extract keys ourselves
    # key: the a word from the document.
    # value: just number '1' as we are counting the number of times this word occured.
    value = record[0]
    words = value.split()
    name = ""
    for w in words:
        length = len(w)
        if length == 1:
            name = "tiny"
        elif 2 <= length <= 4:
            name = "small"
        elif 5 <= length <= 9:
            name = "medium"
        else:
            name = "large"
        mr.emit_intermediate(name, 1)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
      total += v
    mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open("dec.json", 'r')
    mr.execute(inputdata, mapper, reducer)
