class animal():
    def __init__(self,category="open",name="Missing"):
        self._category = category
        self._name = name
    
    def get_category(self):
        return self._category
    
    def get_name(self):
        return self._name
    
class dog(animal):
    def __init__(self,breed="bulldog"):
        super().__init__(category,name)
        self._breed = breed
        
    def get_breed(self):
        return self._breed
    

doggy = animal(category="dog",name="Tod")
print(doggy)
print(doggy.get_name())

tedd = dog()
print(tedd.get_name())