'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 11/24/2025
############################################################################################################################
ASSIGNMENT: Extendible Hash Table
================================================================================================================================================================================================================        
PART 1: 
Include functionality for displaying the table, and inserting, finding, and removing items. [20 points]

Show the result of inserting the items: 
10111101, 00000010, 10011011, 10111110, 01111111, 01010001, 10010110, 
00001011, 11001111, 10011110, 11011011, 00101011, 01100001, 11110000, 
01101111, 00000101, 01000101, 01000000 
into an initially empty ExtendibleHashTable with M = 4. [10 points]

=== Inserting binary keys into Extendible Hash Table with Bucket Size = 4 ===
Directory index: 000 Info: depth: 2, reference dirs: {0, 4}, items: 11110000 (240), 01000000 (64), 
Directory index: 001 Info: depth: 3, reference dirs: {1}, items: 01010001 (81), 01100001 (97), 
Directory index: 010 Info: depth: 2, reference dirs: {2, 6}, items: 00000010 (2), 10111110 (190), 10010110 (150), 10011110 (158), 
Directory index: 011 Info: depth: 3, reference dirs: {3}, items: 10011011 (155), 1011 (11), 11011011 (219), 00101011 (43), 
Directory index: 100 Info: depth: 2, reference dirs: {0, 4}, items: 11110000 (240), 01000000 (64), 
Directory index: 101 Info: depth: 3, reference dirs: {5}, items: 10111101 (189), 00000101 (5), 1000101 (69), 
Directory index: 110 Info: depth: 2, reference dirs: {2, 6}, items: 00000010 (2), 10111110 (190), 10010110 (150), 10011110 (158), 
Directory index: 111 Info: depth: 3, reference dirs: {7}, items: 01111111 (127), 11001111 (207), 01101111 (111), 

================================================================================================================================================================================================================        
PART 2: Also, show the result of inserting the items 16, 4, 6, 22, 24, 10, 31, 7, 9, 20, 26, 3, 1 into an initially empty ExtendibleHashTable with M = 3. [10 points]

=== Inserting integer keys into Extendible Hash Table with Bucket Size = 3 ===
Directory index: 000 Info: depth: 3, reference dirs: {0}, items: 10000 (16), 11000 (24), 
Directory index: 001 Info: depth: 2, reference dirs: {1, 5}, items: 1001 (9), 1 (1), 
Directory index: 010 Info: depth: 3, reference dirs: {2}, items: 1010 (10), 11010 (26), 
Directory index: 011 Info: depth: 2, reference dirs: {3, 7}, items: 11111 (31), 111 (7), 11 (3), 
Directory index: 100 Info: depth: 3, reference dirs: {4}, items: 100 (4), 10100 (20), 
Directory index: 101 Info: depth: 2, reference dirs: {1, 5}, items: 1001 (9), 1 (1), 
Directory index: 110 Info: depth: 3, reference dirs: {6}, items: 110 (6), 10110 (22), 
Directory index: 111 Info: depth: 2, reference dirs: {3, 7}, items: 11111 (31), 111 (7), 11 (3), 

================================================================================================================================================================================================================        
PART 3: 

Insert 500 uniformly distributed, random, unsigned 64-bit integers (i.e., the keys) into the
extendible hash table. In this case N = 500 and each integer would be converted to its binary
form. Build the extendible hash table using M = 4 and D = 6; and, using M = 8 and D = 7.

Compare the size of each directory and write a 100 to 200-word summary of your findings. Your
summary should consider the actual number of leaves, the expected number of leaves which is
(N/M)∙ 𝑙𝑜𝑔2𝑒, the number of times the keys are rehashed into new directories, and the number
of duplicate keys, if any. [20 points]

Experiment #1 (M=4;D=6) had larger metrics on all report variables. I believe this performance is expected,
because an extendible hash table with smaller bucket size and initial global depth will get full with 
fewer insertions than an extendible hash table with larger bucket size and initial global depth, triggering 
more calls of _doubleDirectorySize() and _split(), and leading to more leaves and rehashes that could take 
the final global depth to be larger than the final global depth of a hash table with both larger bucket size and initial global depth. 
Experiment #1 also had actual number of unique leaves closer to expected, while Experiment #2 produced 44% more actual leaves than expected. 
Both experiments observed zero duplications.


=============
== RESULTS ==
=============
=== Random experiment: N=500, M=4, initial D=6 ===
Final global depth: 10
Directory size: 1024
Actual # unique leaves: 178
Expected # leaves (N/M * log2 e): 180.34
Rehash (directory doubling) count: 4
Duplicate keys observed: 0

=== Random experiment: N=500, M=8, initial D=7 ===
Final global depth: 8
Directory size: 256
Actual # unique leaves: 130
Expected # leaves (N/M * log2 e): 90.17
Rehash (directory doubling) count: 1
Duplicate keys observed: 0
############################################################################################################################
'''

import random
import math

class Leaf: # bucket
        def __init__(self,index,depth):
            '''
            Description: Leaf (bucket) constructor
                        
            Inputs:
                - index: integer that represents the directory
                - depth: Local depth
            Outputs:
                - _index: original leaf index
                - _depth: the local depth of the leaf
                - _directories: this is a set holding the directories that are mapping to this leaf
                - _items: starts empty. This list will hold the key-value pairs assigned to this leaf
            '''
            self._index = index # binary bucket address
            self._depth = depth # local depth
            self._directories = set() # Tracks the directories referencing this lead
            self._items = list() # Store key-value pairs within the leaf    
                
        def __contains__(self,key):
            '''
            Description: Special method to determine whether a key is stored in the leaf.
            Returns a boolean True if the key is found, and False otherwise
            Input: key to be looked up
            Output: True or False
            '''
            return key in self._items
            
        # Conversion helpers
        def _convertToString(self,item):
            '''
            Description: converts an integer item to string
            Input: 
                - item: an integer
            Output:
                - The same item, but in string type
            :param item: data to be converted to string
            '''
            return str(item)
        
        def _binaryToDecimal(self,item):
            '''
            Converts a binary string to decimal
            Input:
                - item: a binary string
            Output:
                - decimal: an integer that represents the binary string from the input
            '''
            decimal = 0
            j = len(item)-1
            for i in item:        
                decimal += + int(i)*(2**int(j))
                j -= 1
            return decimal
        
        def __str__(self):
            '''
            Return a string representation of the leaf for printing back to the use, 
            including local depth, reference directories, and leaf items (in both binary and decimal form)
                                    
            '''
            str_representation = "depth: " + self._convertToString(item=self._depth) + ", "
            str_representation += "reference dirs: "
            
            if len(self._directories) == 0:
                str_representation += "None"
            else:
                str_representation += self._convertToString(self._directories)
            
            str_representation += ", items: "
            
            for item in self._items:
                str_representation +=  self._convertToString(item) + " (" + self._convertToString(self._binaryToDecimal(item)) + "), "
            
            return str_representation        
        
class ExtendibleHashTable:
    def __init__(self,globalDepth = 1, maxBucketSize = 4):
        '''
        Description: Extendible Hash Table Constructor
        
        Inputs:
            - globalDepth: Global Depth (1 by default)
            - maxBucketSize: Max Bucket Size (4 by default)
        Outputs:
            - An ExtendibleHasTable object containing:
                - _globalDepth from inputted globalDepth
                - _maxBucketSize from inputted maxBucketSize
                - empty leaves constructed at initialization equal to 2^(Global Depth)
                - _directory with constructed leaves to store leaves
                - _rehashCount set to 0 
                - _duplicateCounte set to 0                                
        '''
        self._globalDepth = globalDepth
        self._maxBucketSize = maxBucketSize
        self._directory = dict() # Map indices to Leaf objects
        
        # Initialize 2^globalDepth entries in the directory
        for index in range(2**self._globalDepth):
            leaf = Leaf(index,self._globalDepth)            
            leaf._directories.add(index)            
            self._directory[index] = leaf
            
        # Initialize counters
        self._rehashCount = 0
        self._duplicateCount = 0
        
    # Accessors
    def rehashCount(self):
        '''
        Description: Accesor for _rehashCount                
        Input: None
        Output: _reshaCount
        '''
        return self._rehashCount
    
    def duplicateCount(self):
        '''
        Description: Accesor for _duplicateCount    
        Input: None
        Output: _duplicateCount    
        '''
        return self._duplicateCount
    
    def globalDepth(self):
        '''
        Description: Accesor for _globalDepth    
        Input: None
        Output: _globalDepth    
        '''        
        return self._globalDepth
    
    def get_leaf_count(self):
        '''
        Description: Method to count number of leaves stored in the Hash Table
        Input: None
        Output: Number of leaves in the hash table
        '''   
        return len({id(v) for v in self._directory.values()})
    
    # HELPERS FOR BINARY CONVERSION
    def _key_to_bits(self,key):
        '''
        Description: Converts an integer key to a binary number string (bits)
    
        Inputs:
            - key: an integer representing a key 
        Outputs:
            - The binary number string format of the provided key (changes type to string)
        '''
        if isinstance(key,str):
            # If string, assume it's already binary     
            return key
        else:
            if key == 0:
                return "0"
            return format(key,'b')
    
    def _get_index(self, key_bits):
        '''
        Description: Get the integer form of a binary number string
        Inputs:
            - key_bits: a binary number string
        Outputs:        
            - A  integer converted from a binary number string
        '''
        if self._globalDepth == 0:
            return 0
        if len(key_bits) >= self._globalDepth:
            suffix = key_bits[-self._globalDepth:]
        else:
            suffix = key_bits.zfill(self._globalDepth)[-self._globalDepth:]
        return int(suffix,2) 
        
    def insert(self,key):
        '''
        Description: Inserts a key into the hash table, addressing for the need of directory growth and/or splitting.
        
        Inputs:
            - key: a key integer to be added to the hash table
        Outputs:
            - The key is added to one of the hash table leaves (buckets)
        '''        
        binaryKeyStr = self._key_to_bits(key)
        index = self._get_index(binaryKeyStr)
        leaf = self._directory[index]
        
        # Counts insertion of duplicates
        if binaryKeyStr in leaf._items:
            self._duplicateCount += 1
            return
                                                
        if len(leaf._items) < self._maxBucketSize:
            leaf._items.append(binaryKeyStr)
        else:
            # If number of Leaf items > = Max bucket size, need to split,
            # and potentially apply direcotry growth.
            self._split(leaf,binaryKeyStr)
    
    def _split(self,leaf,keyToAdd):
        '''
        Description: 
            - Split the bucket when it exceeds maxBucketSize, 
            - Calls _doubleDirectory to perform directory growth when local depth = global depth
            - Recursively calls insert(key) to add key after splitting and growing directories, 
              and to treat for cascades
        
        Inputs:
            - leaf: leaf object that needs to be split
            - keyToAdd: key that needs to be inserted into the hash table
        Output:
            - Splitted hash table, and key added into the hash table
        '''
        if leaf._depth == self._globalDepth:
            self._doubleDirectorySize()
        
        # Create new leaf
        leaf._depth  = leaf._depth + 1
        oldItems = leaf._items #+ [keyToAdd]
        leaf._items = []                        
        newLeaf = Leaf(index=leaf._index,depth=leaf._depth)
        
        # Determining where indices should go
        self._updateDirectory(leaf=leaf,newLeaf=newLeaf)
                        
        # Redistribute all items
        for item in  oldItems:
            index = self._get_index(item)
            targetLeaf = self._directory[index]
            targetLeaf._items.append(item)
                                        
        # Recursion to treat cascades
        self.insert(int(keyToAdd,2) if isinstance(keyToAdd, str) else keyToAdd)
        
    def _doubleDirectorySize(self):
        '''
        Description: Double the directory size by duplicating entries
        Inputs:
            - None
        Outpus:
            - 2x Number of directories in the hash table 
            - _rehashCount increments by 1
        '''
        
        oldDir = self._directory
        oldSize = 2**self._globalDepth
        self._globalDepth += 1
        newSize = 2**self._globalDepth
        self._directory = {}
        
        for index in range(newSize):
            original = index & (oldSize -1)            
            leaf = oldDir[original]
            self._directory[index] = leaf
            leaf._directories.add(index)
                
        self._rehashCount += 1
                
    def _updateDirectory(self,leaf,newLeaf):
        '''
        Description: Update the directory to point to the new leaf
        
        Inputs:
            - leaf: the original leaf holding the items that are being split and updated
            - newLeaf: the new leaf that will hold part of the items after the split
        '''
        oldDirIndices = list(leaf._directories) 
        leaf._directories.clear()
        newLeaf._directories.clear()
        for index in oldDirIndices:
            pattern = format(index, f'0{self._globalDepth}b')[-leaf._depth:]
            
            if pattern[0] == '0': # Check the newest binary digit added
                self._directory[index] = leaf
                leaf._directories.add(index)
            else:
                self._directory[index] = newLeaf
                newLeaf._directories.add(index)
                            
    def search(self,key):
        '''
        Description: Search for a key in the hash table
        
        Inputs:
            - key: a key to be searched in the hash table
        Outputs:
            - Return whether the key is in the hash table
        '''
        binaryKeyStr = self._key_to_bits(key)        
        index = self._get_index(binaryKeyStr)
        leaf = self._directory[index]
        return binaryKeyStr in leaf
    
    def show_extendible_hash_table(self):
        '''
        Description: prints a report showing directories, local depth, , and items in both binary and decimal form 
          for the current state of the hash table    
        
        Inputs: None
        Outputs:
            - a print report showing directories, local depth, , and items in both binary and decimal form 
          for the current state of the hash table    
        '''
        for index in range(2**self._globalDepth):
            leaf = self._directory[index]
            # self._key_to_bits(index)
            bitIndex = format(index, f'0{self._globalDepth}b')
            print('Directory index:',bitIndex,"Info:",leaf)            


def insert_binary_and_show(binary_keys,M):
    '''
    Description: runs an experiment inserting binary number string keys into a hash table
    Inputs: 
        - binary_keys: a list of binary number string keys to be inserted in the hash table
        - M: the max bucket size for the hash table
    
    Outputs:
        - A report showing directories, local depth, , and items in both binary and decimal form 
          for the final hash table    
    '''
    print(f"\n=== Inserting binary keys into Extendible Hash Table with Bucket Size = {M} ===")
    eht = ExtendibleHashTable(globalDepth=1, maxBucketSize=M)
    
    for item in binary_keys:
        eht.insert(item)
    eht.show_extendible_hash_table()

def insert_int_and_show(int_keys,M):
    '''
    Description: runs an experiment inserting integer keys into a hash table
    Inputs: 
        - int_keys: a list of integer keys to be inserted in the hash table
        - M: the max bucket size for the hash table
    
    Outputs:
        - A report showing directories, local depth, , and items in both binary and decimal form 
          for the final hash table
    '''
    print(f"\n=== Inserting integer keys into Extendible Hash Table with Bucket Size = {M} ===")
    eht = ExtendibleHashTable(globalDepth=1, maxBucketSize=M)
    
    for item in int_keys:
        eht.insert(item)
    eht.show_extendible_hash_table()

def random_experiment(N=500, M=4, initD=6):
    '''
    Description: executes a random number experiment on the hash table
    Inputs: 
        - N: number of random integers to be tested
        - M: hash table max bucket size
        - initD: hash table initial global depth
    Outputs: 
        - A report containinf the final values for
            - Global depth
            - Directory size
            - Actual number of unique leaves
            - Expected number of unique leaves
            - Rehash counts
            - Duplicate keys observed
    '''
    print(f"\n=== Random experiment: N={N}, M={M}, initial D={initD} ===")
    eht = ExtendibleHashTable(globalDepth=initD, maxBucketSize=M)

    # generate N random unsigned 64-bit ints
    keys = [random.getrandbits(64) for n in range(N)]

    for k in keys:        
        eht.insert(k)

    leaf_count = eht.get_leaf_count()
    expected_leaves = (N / M) * math.log2(math.e)

    print(f"Final global depth: {eht.globalDepth()}")
    print(f"Directory size: {2 ** eht.globalDepth()}")
    print(f"Actual # unique leaves: {leaf_count}")
    print(f"Expected # leaves (N/M * log2 e): {expected_leaves:.2f}")
    print(f"Rehash (directory doubling) count: {eht.rehashCount()}")
    print(f"Duplicate keys observed: {eht.duplicateCount()}")
    return eht

def main():
    '''
    Description: executes the three parts requested in the assignment
    Inputs: None
    Outputs: None    
    '''
    # Part 1: Simulation adding binary, M = 4
    binaryKeys = [
        "10111101", "00000010", "10011011", "10111110",
        "01111111", "01010001", "10010110", "00001011",
        "11001111", "10011110", "11011011", "00101011",
        "01100001", "11110000", "01101111", "00000101",
        "01000101", "01000000"
    ]
    ehtBinary = insert_binary_and_show(binaryKeys, M=4)
    
    # Part 2: Simulation adding integers, M = 3
    intKeys = [16, 4, 6, 22, 24, 10, 31, 7, 9, 20, 26, 3, 1]
    ehtInt = insert_int_and_show(intKeys,M=3)
    
#    Part 3: Simulation with (1) 500 Random Numbers, M=4, D=6; and (2) 500 Random Numbers, M=4, D=6
    ehtRandom01 = random_experiment(N=500, M=4, initD=6)
    ehtRandom02 = random_experiment(N=500, M=8, initD=7)
    
if __name__ == "__main__":   
    main()