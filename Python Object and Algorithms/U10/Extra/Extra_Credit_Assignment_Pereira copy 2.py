'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 11/23/2025
############################################################################################################################
ASSIGNMENT: Heap Insertion Analysis

ASSIGNMENT QUESTIONS:

(1) Display the heap: 2, 45, 12, 1, 56, 78, 13, 14, 5, 8, 9, 3, 11, 34

    Percolate UP result:
    1 2 3 5 8 11 13 45 14 56 9 78 12 34 
    Percolate DOWN result:
    1 2 3 5 8 11 13 14 45 56 9 78 12 34  

(2) Write a 100 to 200-word report analyzing the three ordered insertions while contrasting the two
methods used (percolate up or percolate down) to build the heap. Include in your analysis a case
example of when building a heap using percolate up would be more efficient in building a heap.
[15 points]   

Observed runtime showed that Percolate Down (PD) was faster for ascendingly or descendingly ordered inputs, while Percolate Up (PU) was faster on randomly ordered inputs. Some runtimes were close, possibly impacted by CPU prioritization.

Algorithmically, descendingly sorted arrays represent the worst case scenario for PU as every insertion triggers upheaps, causing O(nlogn). 
When input is ascendingly ordered, PU has no upheaps, performing at O(n). 

PD also has no downheaps for ascendingly ordered input, but the algorithm still performs and identifies small child. Asyntotically, even if both are O(n), 
PD performs worse than PU, which only has an append task in this scenario. PD triggers fewer downheaps on descendingly sorted data, than PU upheaps.
        
Given the above, PU performs faster for larger sorted ascending matrices. The n = 500k runtime report below empirically confirms that statement.

A walk-in urgent care priority queue application fits the case as information about patients is unavailable upfront, and priorities could differ, for instance, depending on health severity or age. 
It is impossible to use PD heapify in this case, because there is no predetermined list. Incoming items will go through heap.add(), which appends and upheaps elements based on their key.


====================================
======RUNTIME REPORT================
====================================
Runtime (n = 5,000)
ASCENDING percolate UP:     0.00208s
ASCENDING percolate DOWN:   0.00152s
DESCENDING percolate UP:    0.01091s
DESCENDING percolate DOWN:  0.00301s
RANDOM percolate UP:        0.00294s
RANDOM percolate DOWN:      0.00341s

Runtime (n = 500,000)
ASCENDING percolate UP:     0.19542s
ASCENDING percolate DOWN:   0.22052s
DESCENDING percolate UP:    1.72392s
DESCENDING percolate DOWN:  0.37425s
RANDOM percolate UP:        0.39766s
RANDOM percolate DOWN:      0.40793s

############################################################################################################################
############################################################################################################################
'''

from goodrich.ch09.heap_priority_queue import HeapPriorityQueue as hpq
from goodrich.ch09.heap_priority_queue import HeapPriorityQueuePercolateDown as hpqPercolateDown

import time
import random

def percolateUP(intList,display=0):
    '''
    Description: 
        - Builds a min heap using percolating up
    Inputs:
        - intList: a tuple with key (non-negative integer), and value
        - display: 0 as default. Prints the final heap as a sequential list of keys when assigned to 1.
    Outputs:
        - A heap constructed using percolate up algorithm, and the time the computer took to build the heap
    '''        
    start = time.time()                   
    labHeapPercolateUp = hpq()
    for item in intList:
        labHeapPercolateUp.add(item[0],item[1])            
    end = time.time()
    durationHeap = end - start
    
    if display ==1:    
        print("\nPercolate UP result:")
        for key,value in labHeapPercolateUp:
            print(key,end=" ")
            
    return labHeapPercolateUp,durationHeap
            
def percolateDOWN(intListDown,display=0):    
    '''
    Description: 
        - Builds a min heap using percolate down (heapify + downheap)
    Inputs:
        - intListDown: a tuple with key (non-negative integer), and value
        - display: 0 as default. Prints the final heap as a sequential list of keys when assigned to 1.
    Outputs:
        - A heap constructed using percolate down algorithm, and the time the computer took to build the heap    
    '''       
    start = time.time()
    labHeapPercolateDown = hpqPercolateDown(contents=intListDown)    
    end = time.time()
    durationHeap = end - start 
      
    if display == 1:
        print("\nPercolate DOWN result:")
        for key,value in labHeapPercolateDown:
            print(key,end=" ")
        print()   
        
    return labHeapPercolateDown,durationHeap
    
def main():
    '''
    Description:
        - Prepares the inputs to test heap building algorithms and build a runtime report for the percolate up and percolate down algorithms.
    Inputs:
        - No inputs provided to the main function, but testIntegers have been added to test the correctness of percolateUP() and percolateDown(), and sorted lists with integers 1 to size are generated for runtime analysis
    Outputs:
        - No outputs returned to the user, except for reports on the final heaps from testIntegers using percolate up and percolate down, and a runtime analysis for the arrays size 5k
    '''
    # Part 1 - Create heap with percolate up and percolate down for a predefined list
    testIntegers = [2, 45, 12, 1, 56, 78, 13, 14, 5, 8, 9, 3, 11, 34]
    for index in range(len(testIntegers)):
        testIntegers[index] = (testIntegers[index],"v") 
        
    heapResult01 = percolateUP(testIntegers,display=1)
    heapResult02 = percolateDOWN(testIntegers,display=1)
    
    # Part 2 - Create heap with percolate up and percolate down for integers 1 to 5,000 sorted ascending, descending, and randomly
    size = 5000
    result ="Runtime Analysis Results"
    
    # Preparing lists    
    aSortedListAsc = list(range(1,size+1))
    aSortedListDesc = list(range(size,0,-1))
    aSortedListRand = list(range(1,size+1))
    random.shuffle(aSortedListRand)
    
    for index in range(len(aSortedListAsc)):
        aSortedListAsc[index] = (aSortedListAsc[index],"v")     
        aSortedListDesc[index] = (aSortedListDesc[index],"v")     
        aSortedListRand[index] = (aSortedListRand[index],"v")                     
        
    
    # Ascending 
    heapResult03,duration = percolateUP(aSortedListAsc)    
    result = result+ "\nSorted list ASCENDING percolate UP:\t{:.20f}".format(duration)+" seconds"
    
    heapResult04,duration = percolateDOWN(aSortedListAsc)
    result = result+ "\nSorted list ASCENDING percolate DOWN:\t{:.20f}".format(duration)+" seconds"
    
    # Descending    
    heapResult05,duration = percolateUP(aSortedListDesc)        
    result = result+ "\nSorted list DESCENDING percolate UP:\t{:.20f}".format(duration)+" seconds"
    
    heapResult06,duration = percolateDOWN(aSortedListDesc)
    result = result+ "\nSorted list DESCENDING percolate DOWN:\t{:.20f}".format(duration)+" seconds"

    # Random    
    heapResult07,duration = percolateUP(aSortedListRand)
    result = result+ "\nSorted list RANDOM percolate UP:\t{:.20f}".format(duration)+" seconds"    

    heapResult08,duration = percolateDOWN(aSortedListRand)
    result = result+ "\nSorted list RANDOM percolate DOWN:\t{:.20f}".format(duration)+" seconds"
    
    print()
    print(result)
              
if __name__ == '__main__':
    print()
    main()