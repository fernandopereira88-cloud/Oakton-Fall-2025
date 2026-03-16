'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 11/24/2025
############################################################################################################################
ASSIGNMENT: Extendible Hash Table

Pseudocode:
    - Leaf Class - OK
    - ExtendibleHashTable Class - 
TO DOS:
    - Figure out how  to handle when input could be either binary or decimal
    - Implement split and directory expansion

    
Include functionality for displaying the table, and inserting, finding, and removing items. [20
points]

Show the result of inserting the items: 10111101, 00000010, 10011011, 10111110,
01111111, 01010001, 10010110, 00001011, 11001111, 10011110, 11011011,
00101011, 01100001, 11110000, 01101111, 00000101, 01000101, 01000000 into an
initially empty ExtendibleHashTable with M = 4. [10 points]

Also, show the result of inserting the items 16, 4, 6, 22, 24, 10, 31, 7, 9, 20, 26, 3, 1 into an
initially empty ExtendibleHashTable with M = 3. [10 points]

ASSIGNMENT QUESTSIONS:

Insert 500 uniformly distributed, random, unsigned 64-bit integers (i.e., the keys) into the
extendible hash table. In this case N = 500 and each integer would be converted to its binary
form. Build the extendible hash table using M = 4 and D = 6; and, using M = 8 and D = 7.
Compare the size of each directory and write a 100 to 200-word summary of your findings. Your
summary should consider the actual number of leaves, the expected number of leaves which is
(N/M)∙ 𝑙𝑜𝑔2𝑒, the number of times the keys are rehashed into new directories, and the number
of duplicate keys, if any. [20 points]

############################################################################################################################
'''
import copy
class Leaf: # bucket
        def __init__(self,index,depth):
            '''
            Initialize the leaf node with the given index and depth
            
            :param self: Description
            :param index: Description
            :param depth: Description
            '''
            self._index = index # binary bucket address
            self._depth = depth # local depth
            self._directories = set() # Tracks the directories referencing this lead
            self._items = list() # Store key-value pairs within the leaf
            
        # Bucket Accessors      
        def getDepth(self):
            return self._depth
        
        def getIndex(self):
            return self._index

        def getDirectories(self):
            return self._directories
        
        def getItems(self):
            return self._items        
                
        # Conversion helpers
        def _convertToString(self,item):
            '''
            Docstring for _convertToString                        
            :param item: data to be converted to string
            '''
            return str(item)
        
        def _binaryToDecimal(self,item):
            '''
            Docstring for _binaryToDecimal
            
            :param self: Description
            :param item: Description
            '''
            decimal = 0
            j = len(item)-1
            for i in item:        
                decimal += + int(i)*(2**int(j))
                j -= 1
            return decimal
        
        def _toString(self):
            '''
            Return a string representation of the leaf
            
            
            '''
            str_representation = "depth: " + self._convertToString(item=self._depth) + ", "
            str_representation += "reference dirs: "
            
            if len(self._directories) == 0:
                str_representation += "None"
            else:
                str_representation += self._convertToString(self._directories)
            
            str_representation += ", items: "
            
            for item in self._items:
                str_representation += "(" + self._convertToString(item) + ", " + self._convertToString(self._binaryToDecimal(item)) + "), "
            
            return str_representation
        
        def __setitem__(self,key,value):
            '''
            Docstring for add
            
            :param self: Description
            :param itemToAdd: Description
            '''
            for index in range(len(self._items)):
                if key == self._items[index][0]:
                    self._items = (key,value)
                    return
            self._items.append((key,value))
        
        def __getitem__(self,key):
            for item in self._items:
                if key == item[0]:
                    decimal = self._binaryToDecimal(item[0])
                    value = (decimal,item[1])
                    return value
                    
            raise KeyError("Key Error:"+repr(key))
        
        def _remove(self,key):
            self._items.remove(key)
            
        def __len__(self):
            return len(self._items)                
        

class ExtendibleHashTable:
    def __init__(self,globalDepth = 1, maxBucketSize = 4):
        '''
        Initialize the hash table with default depth and bucket size
        
        :param self: Description
        :param globalDepth: Description
        :param maxBucketSize: Description
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
        
    # HELPERS FOR BINARY CONVERSION     
    def _convert_key_to_binary(self,n):
        '''
        '''
        # Base case n = 0
        if n == 0:
            return "0"
        else:
            binaryPrev = self._convert_decimal_to_binary(n//2)
            remainder = n % 2
            binary = binaryPrev + str(remainder)
            
            return binary
        
    
    def _adjustToBinaryNk(self,k):
        '''
        ##################################
        ## ADJUST DESCRIPTION! 
        Description: This function adjusts a binary number representation to have a multiple of 4 number of digits
        Input:  a binary representation of a natural number
        Output: a binary representation of a natural number that has a multiple of 4 number of digits with zeroes added to the left side when needed    
        '''    
        binaryStr = self._convert_decimal_to_binary(k)
        n = self._globalDepth
            
        if binaryStr == "" or binaryStr =="0":
            binaryStr ="0"
        else:
            binaryStr = binaryStr[1:]
        
        zeroesNeeded = (-len(binaryStr)) % n
        
        binaryNk = ("0"*zeroesNeeded) + binaryStr
        
        
        return binaryNk

    
    def _binaryToDecimal(self,item):
        '''
        Docstring for _binaryToDecimal
        
        :param self: Description
        :param item: Description
        '''
        decimal = 0
        j = len(item)-1
        for i in item:        
            decimal += + int(i)*(2**int(j))
            j -= 1
        return decimal
    
    def _toString(self):
        for key,value in self._directory.items:
            return value._toString()
    
    def __getitem__(self,key):
        binaryKeyStr = self._adjustToBinaryNk(key)
        binaryKeyLBS = binaryKeyStr[-self._globalDepth:]
        bucket = self._directory[binaryKeyLBS]
        if bucket is None:
            raise KeyError("Key Error: " + repr(key))
        return bucket[binaryKeyStr]
    
    def insert(self,key,value):
        '''
        Insert a key-value pair into the hash table.
        
        :param key: Description        
        '''        
        # key: bit string representation
        # 1) Get the number of digits from key to map to the directory
        #       - This will be the number of digits from right to left based on the global depth
        # 2) Find directory to insert the key-value pair
                # - Is this a sequential search over the list of directories? Feels like there should be something smarter...maybe calling the corresponding Leaf object?

        binaryKeyStr = self._adjustToBinaryNk(key)
        binaryKeyLBS = binaryKeyStr[-self._globalDepth:]
        
        if self._directory[binaryKeyLBS] is None:
            raise KeyError('Key Error:' + repr(key))
                            
        leafCurrentBucketSize =len(self._directory[binaryKeyLBS].getItems())
        if leafCurrentBucketSize < self._maxBucketSize:
            self._directory[binaryKeyLBS][binaryKeyStr] = value
        # Need to include case when leafCurrentBucketSize = self._maxBucketSize AND 
        elif leafCurrentBucketSize == self._maxBucketSize and self._directory[binaryKeyLBS]._depth == self._globalDepth:
            self._doubleDirectorySize()
            newBinaryKeyStr = self._adjustToBinaryNk(key)
            newBinaryKeyLBS = newBinaryKeyStr[-self._globalDepth:]
            self._split(self._directory[newBinaryKeyLBS])
            self._directory[newBinaryKeyLBS][binaryKeyStr] = value
            
        elif leafCurrentBucketSize == self._maxBucketSize and self._directory[binaryKeyLBS]._depth < self._globalDepth:
            # localDepth < globalDepth            
            self._split(self._directory[binaryKeyLBS])            
        
    
    def _split(self,leaf):
        '''
        Split the bucket when it exceeds maxBucketSize
        
        :param self: Description
        :param leaf: Description
        '''
        for item in leaf.getItems():
            keyToLeaf = self._binaryToDecimal(item[0])
            valueToLeaf = item[1]
            self.remove()
            self.insert(keyToLeaf,valueToLeaf)            
        
    def _doubleDirectorySize(self):
        '''
        Double the directory size by duplicating entries
        '''
        # Needs to be adjusted because keys need to receive one more binary digit to the left
        # old = copy.deepcopy(self._directory )
        # self._directory.clear()
        oldKLBS = self._globalDepth
        self._globalDepth = self._globalDepth*2
        
        # Issue: this creates one leaf for every new directory key, 
        # BUT we actually only want to create one new bucket to add the new item, 
        # and keep the old mapping for the rest
        for index in range(2**self._globalDepth):            
            binaryIndexStr = self._adjustToBinaryNk(k=index)
            newKLBS = binaryIndexStr[-self._globalDepth:]
            if len(self._directory[oldKLBS]) > 0:
                self._directory[newKLBS] = self._directory[oldKLBS]
            else:
                self._directory[newKLBS] = Leaf(newKLBS,self._globalDepth)
        
        # print(old.items())
        # for key,value in old.items():
        #     print(key)
        #     print(value)
        #     print(value.getItems())
        #     for item in value.getItems():                
        #         keyToLeaf = self._binaryToDecimal(item[0])
        #         valueToLeaf = item[1]
        #         self.insert(keyToLeaf,valueToLeaf)
                
            
    
    def _updateDirectory(leaf,newLeaf):
        '''
        Update the directory to point to the new leaf
        
        :param leaf: Description
        :param newLeaf: Description
        '''
        
    def search(self,key):
        '''
        Search for a key in the hash table
        
        :param self: Description
        :param key: Description
        '''
        binaryKeyStr = self._adjustToBinaryNk(key,self._globalDepth)
        binaryKeyLBS = binaryKeyStr[-self._globalDepth:]
        bucket = self._directory[binaryKeyLBS]
        if bucket is None:
            raise KeyError("Key Error: " + repr(key))
        return bucket[binaryKeyStr]
    
############
############
test = ExtendibleHashTable()
# test.insert(11,"v")
# print(test[11])
# print(test._directory)
# test.insert(13,"v")
# test.insert(15,"v")
# test.insert(9,"v")
# test.insert(3,"v")
# test.insert(1,"v")
# print(test._directory)
# print(test.search(11))

# test.add(32)
# print(test._directories)
# print(test._index)
# print(test._depth)
# print(test._items)
# print(test._toString())

test.insert(1,"v")
test.insert(2,"v")
test.insert(3,"v")
test.insert(4,"v")
test.insert(5,"v")
test.insert(6,"v")
test.insert(7,"v")
test.insert(8,"v")
test.insert(10,"v")
test.insert(11,"v")
test.insert(12,"v")
test.insert(13,"v")
test.insert(14,"v")
test.insert(15,"v")
test.insert(16,"v")
test.insert(17,"v")
test.insert(18,"v")
test.insert(19,"v")
test.insert(20,"v")