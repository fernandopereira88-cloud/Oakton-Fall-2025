'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 11/24/2025
############################################################################################################################
ASSIGNMENT: Collisions

Adjustments performed in supporting files:
    - probe_hash_map.py
        class: ProbeHashMap
            methods: __init__(),_find_slot(),increase_count_collision(),get_collision_count(),_bucket_setitem()
    - hash_map_base.py
        class HashMapBase
            methods: _hash_function2()

ASSIGNMENT QUESTIONS: Write a 100-word report summarizing the results found in part ii. Why does one technique of insertion work better than the others? [20 points]

Double Hashing probing had 1041 average collisions (fewest), followed by Quadratic probing with 1,183 average collisions. 
Linear probing had 2,144 average collisions (highest) as it is more prone to clustering (caused by collisions that store keys consecutively), triggering more collisions and decreasing efficiency. 
Quadratic probing addresses that issue by increasing the spacing between keys in the hash table, but it is still subject to secondary clustering that also causes concentration for collided items and inefficiencies. 
Double Hashing had the least clustering given the two hashing functions used, so it makes sense that it would have relatively fewer collisions.

====================
= COLLISION REPORT =
====================

Linear: 2144.9 collisions on average
Collisions per simulation: [2014, 2692, 1754, 2006, 2042, 2329, 1988, 2254, 2075, 2295]

Quadratic: 1183.5 collisions on average
Collisions per simulation: [1126, 1281, 1159, 1157, 1173, 1209, 1201, 1166, 1192, 1171]

Double Hashing:  1041.1 collisions on average
Collisions per simulation: [1054, 1096, 1035, 1027, 1044, 1032, 1015, 970, 1083, 1055]

############################################################################################################################
############################################################################################################################
############################################################################################################################
'''

from goodrich.ch10.probe_hash_map import ProbeHashMap as phm
import random




def confirm_4kPlus3Int(numberInt):
    '''
    Description:
        - This function evaluates whether a given integer is a PRIME number of the form 4k+3
    Inputs:
        - An integer (int) to be testes
    Outputs:
        - A message confirming or denying that the input integer is a PRIME number of the form 4k+3
    '''
    remainder = (numberInt-3) % 4
    
    # Check whether numberInt is prime
    countDivisors = 0
    for item in range(numberInt):
        if item != 0 and item != 1:            
            remainedPrimeTest = numberInt % item
            if remainedPrimeTest == 0:
                countDivisors += 1
                
    if countDivisors == 0:
        flagPrime = 1
    else:
        flagPrime = 0
        
    if remainder == 0 and flagPrime == 1:
        return print(f"{numberInt} IS PRIME of the form 4k + 3")
    else:
        return print(f"{numberInt} IS NOT PRIME of the form 4k + 3")
  
def test_hashing_techniques(data,hashTableSize):
    '''
    Description:
        - This function tests the hash table insert and find methods using all 3 requested probing methods to evaluate algorithmic correctness
    Inputs:
        - A list with key,value tuple pairs 
    Outputs:
        - Prints a message finding the inserted values in the Hash Table
    '''       
    testHashTableLinear = phm(cap=hashTableSize,probingMethod="linear")
    for item in data:
        testHashTableLinear[item[0]] = item[1]
    print("Linear Probing Key Look Up:")
    print('12:',testHashTableLinear[12])
    print('24:',testHashTableLinear[24])
    print("36:",testHashTableLinear[36])
    print("60:",testHashTableLinear[60])
    
    
    testHashTableQuadratic = phm(cap=hashTableSize,probingMethod="quadratic")
    for item in data:
        testHashTableQuadratic[item[0]] = item[1]
    
    print("Quadratic Probing Key Look Up:")
    print('12:',testHashTableQuadratic[12])
    print('24:',testHashTableQuadratic[24])
    print("36:",testHashTableQuadratic[36])
    print("60:",testHashTableQuadratic[60])
    
    testHashTableDouble = phm(cap=hashTableSize,probingMethod="double")
    for item in data:
        testHashTableDouble[item[0]] = item[1]
    
    print("Double Hashing Probing Key Look Up:")
    print('12:',testHashTableDouble[12])
    print('24:',testHashTableDouble[24])
    print("36:",testHashTableDouble[36])
    print("60:",testHashTableDouble[60])
        
def compute_hash_table_collisions(data,hashTableSize,probingMethod):
    '''
    Description:
    Inputs:
    Outputs:
    
    Compute the number of collisions required to insert random integers in the
    range of 1 to 2^63− 1 into an array-based, fixed size hash table using linear probing, quadratic
    probing, and double hashing techniques.
    '''
    if probingMethod == "linear":
        hashTable = phm(cap=hashTableSize,probingMethod=probingMethod)
    elif probingMethod == "quadratic":
        hashTable = phm(cap=hashTableSize,probingMethod=probingMethod)
    elif probingMethod == "double":
        hashTable = phm(cap=hashTableSize,probingMethod=probingMethod)
    else:
        return print("No probing method provided")
        
    for item in data:
            hashTable[item[0]] = item[1]
        
    return int(hashTable.get_collision_count())
        
def main():
    '''
    Description:
        - This main() function performs the many tasks requested in the assignment. 
          First, it call test_hashing_techniques() to test whether insert and find are working when using the three different hashing techniques.
          Second, it testes wether the proposed Hash Table size for part 2 is of the form 4k+3
          Third, it creates a list of random unique integers and add them to three different objects using each of the probing methods, and storing the number of collisions form each method.
          This last process is repeated 10 times with simulation results being stores in lists that are used to calculate the average number of iterations in using each method and print a report back to the user.
    Inputs:
        - 
    Outputs:
        - Outputs key,value tuple part to visualize algorithmic correctness
        - Outputs whether 1231 is of the form 4k+3
        - Out puts average number of collisions for Linear, Quadratic, and DOuble Hashing probing, plus a list with collisions per iteration
    '''    
    # Assigniment i) Confirm the correctness of the hashing techniques by testing the insertion and
    # retrieval member functions (e.g., find, insert). [20 points]        
    test_hashing_techniques(data=[(12,'a'),(24,'b'),(36,'c'),(60,'d')],hashTableSize=12) 
    
    # Assignment ii) Test the hashing techniques with 1000 insertions on a hash table of size 1231*.
    #Repeat at least ten (10) times and find the average number of collisions using each of
    #the hashing techniques. [10 points]
    #*The size of an array-based, fixed size hash table should be a prime number for several reasons.
    #The quadratic probing technique performs better when that prime number is of the form 4𝑘 + 3.
    
    #Confirm 1231 is a prime number of the form 4𝑘 + 3. 
    assignmentPart2HashTableSize = 1231
    print()
    print(f"Is {assignmentPart2HashTableSize} of the form 4k+3?")    
    confirm_4kPlus3Int(assignmentPart2HashTableSize)
    
    # Generate a list with unique 1,000 random integers
    # First, create a set as it allows only for unique elements
    # Create lists to store collisions for each probing method
    setSize = 1000
    randomIntSet = set()
    randomIntList = list()
    
          

    # Instantiate has table data structures
    linearCollisions = list()
    quadraticCollisions = list()
    doubleCollisions = list()  
                  
    for index in range(10):
        # Add items to a set
        while len(randomIntSet) < setSize:
            number = random.randint(1,(2**63-1))        
            randomIntSet.add(number)
            
        # Populate a list with the randomly generated integers in the top. The list order is random given set properties.        
        while len(randomIntSet) > 0:
            randomIntList.append((randomIntSet.pop(),'v'))    
        # Add values to Hash Tables using the three probing methods, and append the number of collisions in each iteration back to a list        
        linearCollisions.append(compute_hash_table_collisions(data=randomIntList,hashTableSize=assignmentPart2HashTableSize,probingMethod="linear"))
        quadraticCollisions.append(compute_hash_table_collisions(data=randomIntList,hashTableSize=assignmentPart2HashTableSize,probingMethod="quadratic"))
        doubleCollisions.append(compute_hash_table_collisions(data=randomIntList,hashTableSize=assignmentPart2HashTableSize,probingMethod="double"))
        
        randomIntList.clear()
        randomIntSet.clear()
        
    # After running all simulations, calculate average
    avgLinearCollisions = sum(linearCollisions)/len(linearCollisions)
    avgQuadraticCollisions = sum(quadraticCollisions)/len(quadraticCollisions)
    avgDoubleCollisions = sum(doubleCollisions)/len(doubleCollisions)
    
    # Report results
    print("\n====================")
    print("= COLLISION REPORT =")
    print("====================")
    print(f"\nLinear: {avgLinearCollisions} collisions on average")
    print("Collisions per simulation:",linearCollisions)
    print(f"\nQuadratic: {avgQuadraticCollisions} collisions on average")
    print("Collisions per simulation:",quadraticCollisions)
    print(f"\nDouble Hashing:  {avgDoubleCollisions} collisions on average")
    print("Collisions per simulation:",doubleCollisions)

if __name__ == "__main__":
    main()