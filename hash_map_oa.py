# Name: Kirby Little
# OSU Email: littleki@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/09/2022
# Description: Implementation of a hash map using open addressing.


from a6_include import DynamicArray, HashEntry, hash_function_1, hash_function_2


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ""
        for i in range(self._buckets.length()):
            out += str(i) + ": " + str(self._buckets[i]) + "\n"
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
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
        while factor**2 <= capacity:
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
        # Resize table if load factor >= .5.
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        index_init = self.calc_index(key)
        index = self.calc_index(key)
        entry = self._buckets[index]
        tombstone_i = None
        j = 1

        # Probe through used buckets until None, marking first tombstone if
        # existent. If a matching key is found, replace old value with new
        # and make proper adjustments if the entry was a tombstone.
        while entry:
            if entry.key == key:
                entry.value = value
                if entry.is_tombstone:
                    entry.is_tombstone = False
                    self._size += 1
                return
            if entry.is_tombstone:
                tombstone_i = index
            index = (index_init + j ** 2) % self._capacity
            entry = self._buckets[index]
            j += 1

        # Place new key/value at first tombstone if it exists.
        if tombstone_i:
            self._buckets[tombstone_i] = HashEntry(key, value)
            self._size += 1
            return

        # Insert new HashEntry upon arriving at None and increment size.
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

        return

    def table_load(self) -> float:
        """
        Returns the load factor of a HashMap object.
        """
        return float(self.get_size() / self.get_capacity())

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in a HashMap object.
        """
        empty = 0
        for index in range(self._capacity):
            if self._buckets[index] is None:
                empty += 1

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes a HashMap object's capacity to the input capacity. Adjusts
        the new capacity to a prime number if it is not.
        """
        if new_capacity < self._size:
            return

        # Make sure new capacity is prime and make it next nearest prime if
        # not.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create new map to use put for filling.
        new_map = HashMap(new_capacity, self._hash_function)

        # Put all non-tombstone entries in old HashMap into the new one.
        for i in range(self._capacity):
            entry = self._buckets[i]
            if entry:
                if not entry.is_tombstone:
                    new_map.put(entry.key, entry.value)

        # Reassign new buckets and capacity to the resized HashMap.
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity

    def get(self, key: str) -> object:
        """
        Returns the value of the input key's entry or None if it doesn't exist.
        """
        index_init = self.calc_index(key)
        index = self.calc_index(key)
        j = 1
        entry = self._buckets[index]

        # Probe through HashMap for matching key.
        while entry:
            if entry.key == key:
                if entry.is_tombstone:
                    return None
                return entry.value
            index = (index_init + j ** 2) % self._capacity
            entry = self._buckets[index]
            j += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if input key is contained in the HashMap, False otherwise.
        """
        if self._size == 0:
            return False

        index_init = self.calc_index(key)
        index = self.calc_index(key)
        j = 1
        entry = self._buckets[index]

        # Probe through HashMap, looking for input key.
        while entry:
            if entry.key == key:
                if entry.is_tombstone:
                    return False
                return True
            index = (index_init + j ** 2) % self._capacity
            entry = self._buckets[index]
            j += 1

        return False

    def remove(self, key: str) -> None:
        """
        Removes the entry matching the input key from the HashMap.
        """
        index_init = self.calc_index(key)
        index = self.calc_index(key)
        j = 1
        entry = self._buckets[index]

        # Probe through HashMap looking for key. If found, set tombstone
        # marker and decrement size to delete.
        while entry:
            if entry.key == key:
                if entry.is_tombstone:
                    return
                entry.is_tombstone = True
                self._size -= 1
                return
            index = (index_init + j ** 2) % self._capacity
            entry = self._buckets[index]
            j += 1

        return

    def clear(self) -> None:
        """
        Clears the HashMap of all entries.
        """
        for i in range(self._capacity):
            self._buckets[i] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of tuples of all key/value pairs in the HashMap.
        """
        # Iterate through HashMap, adding any non-tombstone key/value pairs
        # to the DA.
        table_array = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets[i]
            if entry:
                if not entry.is_tombstone:
                    tuple = (entry.key, entry.value)
                    table_array.append(tuple)

        return table_array

    def calc_index(self, key):
        """
        Returns the index for a HashMap entry calculated from input key.
        """
        index = self._hash_function(key) % self._capacity
        return index


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put("str" + str(i), i * 100)
        if i % 25 == 24:
            print(
                m.empty_buckets(),
                round(m.table_load(), 2),
                m.get_size(),
                m.get_capacity(),
            )

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put("str" + str(i // 3), i * 100)
        if i % 10 == 9:
            print(
                m.empty_buckets(),
                round(m.table_load(), 2),
                m.get_size(),
                m.get_capacity(),
            )

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put("key1", 10)
    print(round(m.table_load(), 2))
    m.put("key2", 20)
    print(round(m.table_load(), 2))
    m.put("key1", 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put("key" + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key1", 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key2", 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key1", 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key4", 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put("key" + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(
                f"Check that the load factor is acceptable after the call to "
                f"resize_table().\n"
                f"Your load factor is {round(m.table_load(), 2)} and should "
                f"be less than or equal to 0.5"
            )

        m.put("some key", "some value")
        result = m.contains_key("some key")
        m.remove("some key")

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(
            capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2)
        )

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get("key"))
    m.put("key1", 10)
    print(m.get("key1"))

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
    m = HashMap(11, hash_function_1)
    print(m.contains_key("key1"))
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key3", 30)
    print(m.contains_key("key1"))
    print(m.contains_key("key4"))
    print(m.contains_key("key2"))
    print(m.contains_key("key3"))
    m.remove("key3")
    print(m.contains_key("key3"))

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
    print(m.get("key1"))
    m.put("key1", 10)
    print(m.get("key1"))
    m.remove("key1")
    print(m.get("key1"))
    m.remove("key4")

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key1", 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity())
    m.put("key2", 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put("20", "200")
    m.remove("1")
    m.resize_table(12)
    print(m.get_keys_and_values())
