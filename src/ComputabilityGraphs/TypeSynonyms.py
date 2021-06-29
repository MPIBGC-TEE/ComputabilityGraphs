
from typing import List, Set, Tuple, Callable, FrozenSet
Node = FrozenSet[type]
Decomp = Tuple[Node]
Computer = Callable[[Tuple[type]], type]
ComputerSet = FrozenSet[Computer]
