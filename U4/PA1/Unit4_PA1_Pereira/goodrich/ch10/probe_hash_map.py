# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .hash_map_base import HashMapBase

class ProbeHashMap(HashMapBase):
  """Hash map implemented with linear probing for collision resolution."""
  _AVAIL = object()       # sentinal marks locations of previous deletions

  def __init__(self,probingMethod="linear",**kwargs):
    '''
    Description:
      - Hash table Constructor. Not initially present, but added to allow the ProbeHasMap to use differen probing methods
    Inputs:
      - Takes all inputs from HashMapBase and allow them to be adjusted
      - probingMethod defines which probing will be used to handle collisions. Options: "linear", "quadratic", "double"
    Outputs:
      - _probingMethod: private data attribute that stores the probing method for the instatiated object
      - _collisionCounter: a private counter to track the number of collisions when adding items to the hash tables
    '''
    super().__init__(**kwargs)
    self._probingMethod = probingMethod
    self._collisionCounter = 0
    
  def _is_available(self, j):
    """Return True if index j is available in table."""
    return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

  def _find_slot(self, j, k,flagSetItem=0):
    """
    Description:
      - Search for key k in bucket at index j using the appropriate probing technique defined during the object construction 
        (linear, quadratic, or double). Also, increments _collisionCounter for each collision triggered by _bucket_setitem()           
    Inputs:
      - j: the index for the key after taking the key through the hash function
      - k: the original key
      - flagSetItem: 0 or 1 to be used by SetItem methods calling _find_slot and increment collisions as they happen
    Outputs:
      - Return (success, index) tuple, described as follows:
          If match was found, success is True and index denotes its location.
          If no match found, success is False and index denotes first available slot.
    """
    
    if self._probingMethod.lower() == "quadratic":
      # Quadratic Probing Setup #
      i = 1                                   # quadratic probing distance variable    
      h = j
      
 
    elif self._probingMethod.lower() == "double":
      # Quadratic Probing Setup #
      i = 1                                   # double hashing probing distance variable    
      h = j
      j2 = self._hash_function2(k)        
      
    firstAvail = None
    while True:                               
      if self._is_available(j):
        if firstAvail is None:
          firstAvail = j                      # mark this as first avail
        if self._table[j] is None:
          return (False, firstAvail)          # search has failed
      elif k == self._table[j]._key:
        return (True, j)                      # found a match
      
      # This part only runs if there is a collision (either to set or to get an item)
      # For this algorithm, I have considered a collision to be defined as each time the probe passes through an occupied slot.
      if self._probingMethod.lower() == "linear":
        ##################
        # LINEAR HASHING #
        ##################     
        j = (j + 1) % len(self._table)          # keep looking (cyclically)
        
        
      elif self._probingMethod.lower() == "quadratic":
        #####################
        # Quadratic Probing #
        #####################        
        j = (h + i*i) % len(self._table)          # performs the quadratic probing
        i += 1
        

      elif self._probingMethod.lower() == "double":
        #####################
        # DOUBLE HASHING #
        #####################
        
        j = (h + i*j2) % (len(self._table))
        i += 1
        
      # If collision when setting the item, increment collision counter 
      if flagSetItem ==1:
        self.increase_count_collision()
      #####################
      #####################
      #####################      
        
  def increase_count_collision(self):
    '''
    Description: Increments the collision counter
    '''
    self._collisionCounter += 1
    
  def get_collision_count(self):
    '''
    Description: Returns the current count of collisions in the hash table
    '''
    return self._collisionCounter
  
  def _bucket_getitem(self, j, k):
    found, s = self._find_slot(j, k)
    if not found:
      raise KeyError('Key Error: ' + repr(k))        # no match found
    return self._table[s]._value

  def _bucket_setitem(self, j, k, v):
    '''
    Description: 
      - Finds the appropriate slot for a key,value pair, making sure the _collisionCounter will be 
        incremented when collisions happen (flagSetItem=1)
    Inputs:
      - j: hash index 
      - k: key
      - v: value
    Outputs:
      - Inserts or overwrites value ate the key
    '''
    found, s = self._find_slot(j, k,flagSetItem=1)
    if not found:
      self._table[s] = self._Item(k,v)               # insert new item
      self._n += 1                                   # size has increased
    else:
      self._table[s]._value = v                      # overwrite existing

  def _bucket_delitem(self, j, k):
    found, s = self._find_slot(j, k)
    if not found:
      raise KeyError('Key Error: ' + repr(k))        # no match found
    self._table[s] = ProbeHashMap._AVAIL             # mark as vacated

  def __iter__(self):
    for j in range(len(self._table)):                # scan entire table
      if not self._is_available(j):
        yield self._table[j]._key
