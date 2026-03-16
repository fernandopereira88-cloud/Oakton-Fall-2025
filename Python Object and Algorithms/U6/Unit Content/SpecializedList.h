#ifndef SPECIALIZED_LIST_H
#define SPECIALIZED_LIST_H
// Specialized List that goes in both directions
struct NodeType;
#include <cstddef>
#include <iostream>
using namespace std;

class SpecializedList
{
public:
  SpecializedList();                    // Class constructor
//  ~SpecializedList();                   // Class destructor
//  SpecializedList(const SpecializedList& someList);   // Copy constructor

  void ResetForwardPeek();

  void PeekNextItem(int& item , bool& finished);

  void ResetForward();
  // Initializes current position for an iteration 
  //  through the list from first item to last item.

  void GetNextItem(int& item, bool& finished);
  // Gets the next item in the structure.
  //  finished is true if all the items have been accessed.
  //  GetNextItem and GetPriorItem are independent; a forward 
  //  iteration and a backward iteration may be in progress 
  //  at the same time.

  void ResetBackward();
  // Initializes current position for an iteration
  //  through the list from last item to first item.

  void GetPriorItem(int& item, bool& finished);
  // Gets the previous item in the structure.
  //  finished is true if all the items have been accessed.
 
  void PutFront(int item);
  // Inserts item as the first item in the structure.

  void PutEnd(int item);
  // Inserts item as the last item in the structure.
  
  int GetLength() const;
  // Returns the number of items in the structure.

  bool IsListNull() const;

  void SetList(NodeType*);

  SpecializedList& operator=(const SpecializedList& list);
  SpecializedList(const SpecializedList& slist);

private:
  NodeType* list;
  NodeType* currentNextPosPeek;
  NodeType* currentNextPos;
  NodeType* currentBackPos;
  int length;
};


struct NodeType
{
  NodeType* next;
  NodeType* back;
  int info;
};

SpecializedList::SpecializedList()
{
  length = 0;
  currentNextPos = NULL;
  currentBackPos = NULL;
  currentNextPosPeek = NULL;
  list = NULL;
}

//IT 5/8/2019
SpecializedList::SpecializedList(const SpecializedList& slist){
	length = 0;
	currentNextPos = NULL;
	currentBackPos = NULL;
	currentNextPosPeek = NULL;
	list = NULL;
	NodeType* iter;
	iter = slist.list;
	while(length < slist.length){
		NodeType* newNode = new NodeType;
		newNode->info = iter->info;
		if (list == NULL) //first node
		{
			newNode->back = newNode;
			newNode->next = newNode;
			list = newNode;
		}
		else
		{
			newNode->back = list->back;
			newNode->next = list;
			list->back->next = newNode;
			list->back = newNode;
		}
		iter = iter->next;
		length++;
	}
}

//IT 5/8/2019
SpecializedList& SpecializedList::operator=(const SpecializedList& slist){
	if(this != &slist){
		NodeType* iter;

		if(list != NULL){
			//delete old contents of this
			while(length != 0){
				iter = list;
				list = list->next;
				delete iter;
				length--;
			}
		}

		//copy new contents over to this from rhs
		iter = slist.list;
		list = NULL;
		while(length < slist.length){
			NodeType* newNode = new NodeType;
			newNode->info = iter->info;
			if (list == NULL)  //first node
			{ // list is empty.
				newNode->back = newNode;
				newNode->next = newNode;
			    list = newNode;
			}
			else
			{
				newNode->back = list->back;
			    newNode->next = list;
			    list->back->next = newNode;
			    list->back = newNode;
			}
			iter = iter->next;
			length++;
		}
	}
	return *this;
}

void SpecializedList::SetList(NodeType* node){
	list = node;
}

bool SpecializedList::IsListNull() const{
	return (list == NULL);
}


void SpecializedList::ResetForwardPeek()
// Post: currentNextPosPeek has been initialized for a forward
//       traversal.
{
  currentNextPosPeek = NULL;
}

void SpecializedList::ResetForward()
// Post: currentNextPos has been initialized for a forward
//       traversal.
{
  currentNextPos = NULL;
}

void SpecializedList::PeekNextItem(int& item,
	     bool& finished)
// Pre:  ResetForwardPeek has been called before the first call to
//       this function.
// Post: item is a copy of the first item in the list.
//       finished is true if item is the last item in the list;
//       false otherwise.
{
	if (currentNextPosPeek == NULL)
	    currentNextPosPeek = list->next;
	  else
	    currentNextPosPeek = currentNextPosPeek->next;
	  item = currentNextPosPeek->info;
	  finished = (currentNextPosPeek == list);
}


void SpecializedList::GetNextItem(int& item,
     bool& finished)
// Pre:  ResetForward has been called before the first call to
//       this function.
// Post: item is a copy of the next item in the list.
//       finished is true if item is the last item in the list;
//       false otherwise.
{
  if (currentNextPos == NULL)
    currentNextPos = list->next;
  else
    currentNextPos = currentNextPos->next;
  item = currentNextPos->info;
  finished = (currentNextPos == list);
}

void SpecializedList::ResetBackward()
// Post: currentBackPos has been initialized for a backward
//       traversal.
{
  currentBackPos = NULL;
}

void SpecializedList::GetPriorItem(int& item, bool& finished)
// Pre: ResetBakward has been called.
// Post: item is a copy of the previous item in the list.
//       finished is true if item is the first item in the list;
//       false otherwise.
{
  if (currentBackPos == NULL)
    currentBackPos = list;
  else
    currentBackPos = currentBackPos->back;
  item = currentBackPos->info;
  finished = (currentBackPos == list->next);
}

void SpecializedList::PutFront(int item)
// Post: item has been inserted at the front of the list.
{
  NodeType* newNode;

  newNode = new NodeType;
  newNode->info = item;
  if (list == NULL)
  { // list is empty.
    newNode->back = newNode;
    newNode->next = newNode;
    list = newNode;
  }
  else
  {
    newNode->back = list;
    newNode->next = list->next;
    list->next->back = newNode;
    list->next = newNode;
  }
  length++;
}

void SpecializedList::PutEnd(int item)
// Post: item has been inserted at the end of the list.
{
  PutFront(item);
  list = list->next;
}

int SpecializedList::GetLength() const{
	return length;
}

#endif
