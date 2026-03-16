import random
import math

# ------------------------------
# Leaf (Bucket)
# ------------------------------
class Leaf:
    def __init__(self, index: int, depth: int):
        """
        index: integer index in directory (0..2^globalDepth - 1)
        depth: local depth (number of bits used)
        """
        self.index = index
        self.depth = depth
        self.directories = set()      # set of directory indices that reference this leaf
        self.items = []               # stored as bit-string keys

    # ----- Helper conversions -----
    @staticmethod
    def bin_to_int(b: str) -> int:
        return int(b, 2)

    def __contains__(self, key: str) -> bool:
        return key in self.items

    def __str__(self):
        rep = f"depth: {self.depth}, reference dirs: "
        if not self.directories:
            rep += "None"
        else:
            rep += str(sorted(self.directories))
        rep += ", items: "
        for k in self.items:
            rep += f"({k}, {self.bin_to_int(k)}), "
        return rep


# ------------------------------
# Extendible Hash Table
# ------------------------------
class ExtendibleHashTable:
    def __init__(self, globalDepth: int = 1, maxBucketSize: int = 4):
        self.globalDepth = globalDepth
        self.maxBucketSize = maxBucketSize
        self.directory = {}           # index (int) -> Leaf
        self.rehashCount = 0          # times we had to double the directory
        self.duplicateCount = 0       # number of duplicate insert attempts

        # initialize directory with 2^globalDepth leaves
        for i in range(2 ** self.globalDepth):
            leaf = Leaf(index=i, depth=self.globalDepth)
            leaf.directories.add(i)
            self.directory[i] = leaf

    # --------------------------
    # Hash / Index helpers
    # --------------------------
    def _key_to_bits(self, key):
        """
        Accept either a bit string like '10101' or an integer.
        Returns the bit string representation (no fixed width).
        """
        if isinstance(key, str):
            # assume already a bit string (0/1)
            return key
        elif isinstance(key, int):
            # minimal binary representation (no leading zeros)
            if key == 0:
                return "0"
            return format(key, 'b')
        else:
            raise TypeError("Key must be str (bit string) or int")

 
    def _get_index(self, key_bits):
        '''
        Docstring for _get_index
        
        :param self: Description
        :param key_bits: Description
        '''
        if self._globalDepth == 0:
            return 0
        if len(key_bits) >= self._globalDepth:
            suffix = key_bits[-self._globalDepth:]
        else:
            suffix = key_bits.zfill(self._globalDepth)[-self._globalDepth:]
        
        return int(suffix, 2)

    # --------------------------
    # Core operations
    # --------------------------
    def search(self, key):
        bits = self._key_to_bits(key)
        idx = self._get_index(bits)
        leaf = self.directory[idx]
        return bits in leaf.items

    def remove(self, key):
        bits = self._key_to_bits(key)
        idx = self._get_index(bits)
        leaf = self.directory[idx]
        if bits in leaf.items:
            leaf.items.remove(bits)
            return True
        return False

    def insert(self, key):
        bits = self._key_to_bits(key)
        idx = self._get_index(bits)
        leaf = self.directory[idx]

        # duplicate?
        if bits in leaf.items:
            self.duplicateCount += 1
            return

        # if no overflow, just insert
        if len(leaf.items) < self.maxBucketSize:
            leaf.items.append(bits)
            return

        # overflow: need to split (and maybe double directory)
        self._split_insert(leaf, bits)

    # --------------------------
    # Splitting logic
    # --------------------------
    def _split_insert(self, leaf: Leaf, new_key_bits: str):
        """
        Handle insertion into a full leaf:
        1) If local depth == globalDepth -> double directory, then continue.
        2) Split leaf into two leaves with localDepth+1, redistribute keys.
        """
        # Step 1: ensure local depth < globalDepth, otherwise double directory
        if leaf.depth == self.globalDepth:
            self._double_directory()

        # Now globalDepth > leaf.depth
        # Create new leaf
        new_depth = leaf.depth + 1
        old_items = leaf.items + [new_key_bits]
        leaf.items = []

        # The directory entries that used to point to this leaf
        # are those indices in leaf.directories
        # After splitting, they will be divided based on the new bit at position new_depth.
        # First, create two leaves:
        # leaf keeps its index but with updated depth
        leaf.depth = new_depth

        new_leaf = Leaf(index=leaf.index, depth=new_depth)

        # Which indices should go to which leaf?
        # For each directory index that pointed to leaf,
        # check the (globalDepth - new_depth)-th bit (from left) or simpler:
        # For each index i in 0..2^globalDepth-1: if i was in leaf.directories,
        # we decide based on the last new_depth bits of i.
        old_dir_indices = list(leaf.directories)
        leaf.directories.clear()
        new_leaf.directories.clear()

        for idx in old_dir_indices:
            # Look at last new_depth bits of directory index
            pattern = format(idx, f'0{self.globalDepth}b')[-new_depth:]
            if pattern[-1] == '0':
                self.directory[idx] = leaf
                leaf.directories.add(idx)
            else:
                self.directory[idx] = new_leaf
                new_leaf.directories.add(idx)

        # Redistribute all keys
        for kbits in old_items:
            idx = self._get_index(kbits)
            target_leaf = self.directory[idx]
            target_leaf.items.append(kbits)

        # Check if the leaf we tried to insert into is still overfull
        idx_new_key = self._get_index(new_key_bits)
        target = self.directory[idx_new_key]
        if len(target.items) > self.maxBucketSize:
            # Need another split (possibly cascades)
            self._split_insert(target, new_key_bits)

    def _double_directory(self):
        """
        Double directory size and update references.
        """
        old_dir = self.directory
        old_size = 2 ** self.globalDepth
        self.globalDepth += 1
        new_size = 2 ** self.globalDepth
        self.directory = {}

        for i in range(new_size):
            original = i & (old_size - 1)  # lower bits
            leaf = old_dir[original]
            self.directory[i] = leaf
            leaf.directories.add(i)

        self.rehashCount += 1

    # --------------------------
    # Display utilities
    # --------------------------
    def show_directory(self):
        print(f"Global depth: {self.globalDepth}")
        seen_leaves = set()
        for idx in range(2 ** self.globalDepth):
            leaf = self.directory[idx]
            if id(leaf) not in seen_leaves:
                seen_leaves.add(id(leaf))
            idx_bits = format(idx, f'0{self.globalDepth}b')
            print(f"Dir[{idx_bits}] -> Leaf(id={id(leaf) % 10000}, depth={leaf.depth}, items={[(k, int(k,2)) for k in leaf.items]})")
        print(f"Total unique leaves: {len(seen_leaves)}")
        print("-" * 60)

    def get_leaf_count(self):
        return len({id(v) for v in self.directory.values()})


# --------------------------------------------------------
# Helper: run scenario & print result for a list of keys
# --------------------------------------------------------
def insert_bit_strings_and_show(keys, M):
    print(f"\n=== Inserting bit-string keys with M = {M} ===")
    eht = ExtendibleHashTable(globalDepth=1, maxBucketSize=M)
    for k in keys:
        eht.insert(k)
    eht.show_directory()
    return eht


def insert_ints_and_show(int_keys, M):
    print(f"\n=== Inserting integer keys with M = {M} ===")
    eht = ExtendibleHashTable(globalDepth=1, maxBucketSize=M)
    for k in int_keys:
        eht.insert(k)
    eht.show_directory()
    return eht


# --------------------------------------------------------
# Random experiment for N=500 64-bit integers
# --------------------------------------------------------
def random_experiment(N=500, M=4, initD=6):
    print(f"\n=== Random experiment: N={N}, M={M}, initial D={initD} ===")
    eht = ExtendibleHashTable(globalDepth=initD, maxBucketSize=M)

    # generate N random unsigned 64-bit ints
    keys = [random.getrandbits(64) for _ in range(N)]

    seen = set()
    for k in keys:
        if k in seen:
            eht.duplicateCount += 1
            continue
        seen.add(k)
        eht.insert(k)

    leaf_count = eht.get_leaf_count()
    expected_leaves = (N / M) * math.log2(math.e)

    print(f"Final global depth: {eht.globalDepth}")
    print(f"Directory size: {2 ** eht.globalDepth}")
    print(f"Actual # unique leaves: {leaf_count}")
    print(f"Expected # leaves (N/M * log2 e): {expected_leaves:.2f}")
    print(f"Rehash (directory doubling) count: {eht.rehashCount}")
    print(f"Duplicate keys observed: {eht.duplicateCount}")
    return eht


def main():
    # Part 1: given bit strings, M = 4
    bit_keys = [
        "10111101", "00000010", "10011011", "10111110",
        "01111111", "01010001", "10010110", "00001011",
        "11001111", "10011110", "11011011", "00101011",
        "01100001", "11110000", "01101111", "00000101",
        "01000101", "01000000"
    ]
    eht_bits = insert_bit_strings_and_show(bit_keys, M=4)

#     # Part 2: given integers, M = 3
#     int_keys = [16, 4, 6, 22, 24, 10, 31, 7, 9, 20, 26, 3, 1]
#     eht_ints = insert_ints_and_show(int_keys, M=3)

#     # Part 3: random experiment
#     eht_rand1 = random_experiment(N=500, M=4, initD=6)
#     eht_rand2 = random_experiment(N=500, M=8, initD=7)

#     # Sample 100–200 word summary (generic)
#     print("\n=== Sample Summary ===")
#     summary = (
#         "Using extendible hashing, both configurations (M = 4, D = 6) and "
#         "(M = 8, D = 7) produced a number of leaves close to the theoretical "
#         "expectation (N/M * log2(e)). The table with smaller buckets (M = 4) "
#         "created more leaves overall and experienced more directory doublings, "
#         "since splits occurred sooner and more frequently. In contrast, the "
#         "M = 8 table held more items per leaf, so splits were less common and "
#         "the directory stayed smaller for longer, at the cost of slightly higher "
#         "bucket load. The rehash count reflects this trade-off: tighter buckets "
#         "give better distribution but require more structural updates. Duplicate "
#         "keys were rare under uniform random generation; when they occurred, "
#         "they were simply detected and not reinserted. Overall, the experiment "
#         "illustrates how bucket capacity directly impacts the number of leaves "
#         "and the growth rate of the directory in an extendible hash table."
#     )
#     print(summary)

test = ExtendibleHashTable()
test.insert(1)
test.insert(2)
test.insert(3)
test.insert(4)
test.insert(5)
test.insert(6)
test.insert(7)
test.insert(8)
test.insert(9)


# if __name__ == "__main__":
    # main()
