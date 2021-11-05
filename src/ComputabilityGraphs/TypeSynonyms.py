
from typing import List, Set, Tuple, Callable, FrozenSet
Node = FrozenSet[type] #fixme mm 11-04-2021: all references should be replaced by Node class
Decomp = Tuple[Node]   #fixme mm 11-04-2021: all references should be replaced by Decomp class
Computer = Callable[[Tuple[type]], type]
