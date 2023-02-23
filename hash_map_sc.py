# Name: Kirby Little
# OSU Email: littleki@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/09/2022
# Description: Implementation of a hash map using separate chaining.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds the input key/value pair to a HashMap object.
        """
        # Check if key already exists and replace with new value if so.
        # Otherwise, create new node with key and value.
        node = self.get_node(key)
        if node:
            node.value = value
        else:
            index = self.calc_index(key)
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in a HashMap.
        """
        empty = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        Returns the current load factor of a HashMap.
        """
        return float(self.get_size() / self.get_capacity())

    def clear(self) -> None:
        """
        Clears all entries from a HashMap.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the HashMap's capacity to the input capacity. If new
        capacity is not prime, the next prime is used.
        """
        if new_capacity < 1:
            return

        # Make sure new capacity is prime and make it next nearest prime if
        # not.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Fill new table with linked lists.
        new_buckets = DynamicArray()
        for i in range(new_capacity):
            new_buckets.append(LinkedList())

        # Iterate through old table, stopping at indices with non-empty
        # lists. Iterate through lists, rehashing and copying nodes to new
        # table.
        for i in range(self._capacity):
            bucket = self._buckets[i]
            for node in bucket:
                index = self._hash_function(node.key) % new_capacity
                new_buckets[index].insert(node.key, node.value)

        # Reassign new buckets and capacity to the HashMap.
        self._buckets = new_buckets
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Returns the value of the input key's entry if it exists or None
        otherwise.
        """
        # Grab the bucket to search for key in.
        index = self.calc_index(key)
        bucket = self._buckets[index]

        # Search the LinkedList in the bucket.
        node = bucket.contains(key)
        if node:
            return node.value

        return None

    def get_node(self, key: str) -> object:
        """
        Returns the node matching input key or None if node doesn't exist.
        """
        index = self.calc_index(key)
        bucket = self._buckets[index]
        return bucket.contains(key)

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the input key exists in the HashMap or False otherwise.
        """
        if self._size == 0:
            return False

        index = self.calc_index(key)
        if self._buckets[index].contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the entry matching input key from the HashMap.
        """
        # Grab proper bucket and search for entry to remove. If entry is
        # removed, decrement size.
        index = self.calc_index(key)
        bucket = self._buckets[index]
        if bucket.remove(key):
            self._size -= 1

        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of tuples of all key/value pairs in the HashMap.
        """
        # Iterate through HashMap, copying all key/value pairs to the DA.
        table_array = DynamicArray()
        for i in range(self._capacity):
            bucket = self._buckets[i]
            if bucket:
                for node in bucket:
                    tuple = (node.key, node.value)
                    table_array.append(tuple)

        return table_array

    def calc_index(self, key):
        """
        Returns the index for a HashMap entry calculated from input key.
        """
        index = self._hash_function(key) % self._capacity
        return index


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple of 1) an array of the highest occurrence values in the
    HashMap and 2) the number of occurrences of those values.
    """
    map = HashMap()
    # Add DA values as keys, count as values to map. If key exists, increment
    # value instead of replace.
    for i in range(da.length()):
        key = da[i]
        node = map.get_node(key)
        if node:
            node.value += 1
        else:
            map.put(key, 1)

    mode_arr = DynamicArray()
    keys_vals = map.get_keys_and_values()
    count = 0
    for i in range(keys_vals.length()):
        if keys_vals[i][1] == count:
            mode_arr.append(keys_vals[i][0])
        if keys_vals[i][1] > count:
            mode_arr = DynamicArray()
            mode_arr.append(keys_vals[i][0])
            count = keys_vals[i][1]

    tuple = (mode_arr, count)

    return tuple


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
