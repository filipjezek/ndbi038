from typing import Tuple, Iterable, Any, List, TypeVar, Generic
from heapq import heappop, heappush, heappushpop

Priority = int | float
T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self, *items: Iterable[Tuple[T, Priority]], smallest_first=True):
        self.__prio_mod = 1 if smallest_first else -1
        self.__items: List[Tuple[Priority, int, T]] = []
        self.__insert_order = 0
        for item in items:
            self.enqueue(*item)

    def __len__(self):
        return len(self.__items)

    def peek(self):
        return (self.__items[0][2], self.__items[0][0] * self.__prio_mod)

    def enqueue(self, item: T, priority: Priority):
        heappush(self.__items, (priority * self.__prio_mod,
                 self.__insert_order, item))
        self.__insert_order += 1

    def dequeue(self):
        prio, _, item = heappop(self.__items)
        return item, prio * self.__prio_mod

    def en_dequeue(self, item: T, priority: Priority):
        """first enqueues, then dequeues"""
        prio, _, item = heappushpop(
            self.__items, (priority * self.__prio_mod, self.__insert_order, item))
        self.__insert_order += 1
        return item, prio * self.__prio_mod

    def __contains__(self, val: T):
        for _, _, item in self.__items:
            if item == val:
                return True
        return False

    def tolist(self):
        items = self.__items[:]
        return [
            (item, prio * self.__prio_mod) for prio, _, item in
            [heappop(items) for _ in self.__items]
        ]

    def to_reverse_list(self):
        listed = self.tolist()
        listed.reverse()
        return listed
