from dataclasses import dataclass,field
import random
import string
from typing import List

def generate_id()->str:
    return "".join(random.choices(string.ascii_uppercase,k=12))

@dataclass(frozen=False)
# cannot change if frozen true
class Person:
    name:str=None
    address:str=None
    active:bool=True
    email_addresses: List[str]=field(default_factory=list)
    id:str=field(init=False,default_factory=generate_id)
    search_string :str = field(init=False) 

    def __post_init__(self)->None:
         self.search_string=f"{self.name} {self.address}"
       


def main()->None:
    person=Person(name="John",address="123 Main St")
    person.name="Test"
    print(person)

if __name__=="__main__":
    main()