from typing import Tuple, List
from collections import deque
from backend.priority_queue import PriorityQueue
from backend.database.model.pivot import PIVOT_COUNT, Pivot
from backend.database.model.photo import Photo
from backend.distance import distance
from backend.database.alchemy import alchemy
import numpy as np
import itertools as it
from sqlalchemy import select


class ClusterTree:
    L_MAX = 5
    LEAF_SPLIT_AT = PIVOT_COUNT ** 2

    @classmethod
    def reset(cls, pivots: List[Pivot]):
        cls.root = _InternalNode(0, tuple())
        cls.pivots = pivots
        cls.root.children = [_LeafNode(1, (p.id - 1, )) for p in cls.pivots]

    @classmethod
    def insert_object(cls, obj: Photo):
        """
        this will compute (and set) obj.key, posibly rehashing some other object keys
        """
        cls.root.accept(_InsertVisitor(obj, cls.pivots))

    @classmethod
    def range_search(cls, query: np.ndarray, radius: float):
        p_dists = [distance(query, p.clip_features) for p in cls.pivots]
        p_perm = np.argsort(p_dists)
        queue = deque((cls.root, ))
        results = set()
        while len(queue) > 0:
            node = queue.pop()
            if node.lvl > 0 and (
                p_dists[node.pivot_prefix[-1]] -
                p_dists[cls.__min_valid_p(p_perm, node)]
            ) > 2 * radius:
                continue
            if isinstance(node, _InternalNode):
                queue.extendleft(node.children)
                continue

            dist_to_pp0 = p_dists[node.pivot_prefix[0]]
            if dist_to_pp0 + radius < (node.min % 1) or dist_to_pp0 - radius > (node.max % 1):
                continue

            for obj in alchemy.session.execute(
                select(Photo).where(Photo.key.between(
                    (node.min // 1) + dist_to_pp0 - radius,
                    (node.min // 1) + dist_to_pp0 + radius,
                ))
            ).scalars():
                if max(
                    abs(pd - getattr(obj, f'p{i}'))
                    for i, pd in enumerate(p_dists)
                ) > radius:
                    continue
                if distance(obj.clip_features, query) <= radius:
                    results.add(obj)
        return results

    @classmethod
    def knn_search(cls, query: np.ndarray, k: int):
        radius = 1
        p_dists = [distance(query, p.clip_features) for p in cls.pivots]
        p_perm = np.argsort(p_dists)
        queue = PriorityQueue['_Node']((cls.root, 0))
        candidates = PriorityQueue[Photo](smallest_first=False)
        while len(queue) > 0:
            node, penalty = queue.dequeue()
            if node.lvl > 0 and (
                p_dists[node.pivot_prefix[-1]] -
                p_dists[cls.__min_valid_p(p_perm, node)]
            ) > 2 * radius:
                continue
            if isinstance(node, _InternalNode):
                for ch in node.children:
                    queue.enqueue(ch, cls.__penalty(p_perm, p_dists, ch))
                continue

            dist_to_pp0 = p_dists[node.pivot_prefix[0]]
            if dist_to_pp0 + radius < (node.min % 1) or dist_to_pp0 - radius > (node.max % 1):
                continue

            for obj in alchemy.session.execute(
                select(Photo).where(Photo.key.between(
                    (node.min // 1) + dist_to_pp0 - radius,
                    (node.min // 1) + dist_to_pp0 + radius,
                ))
            ).scalars():
                if obj in candidates or max(
                    abs(pd - getattr(obj, f'p{i}'))
                    for i, pd in enumerate(p_dists)
                ) > radius:
                    continue
                actual_dist = distance(obj.clip_features, query)
                if actual_dist <= radius:
                    if len(candidates) == k:
                        candidates.en_dequeue(obj, actual_dist)
                    else:
                        candidates.enqueue(obj, actual_dist)
                    if len(candidates) == k:
                        radius = candidates.peek()[1]
        return [c[0] for c in candidates.to_reverse_list()]

    @staticmethod
    def __min_valid_p(p_perm: List[int], node: '_Node') -> int:
        skip = node.pivot_prefix[:-1]
        for i in p_perm:
            if i not in skip:
                return i

    @staticmethod
    def __penalty(p_perm: List[int], p_dists: List[float], node: '_Node') -> float:
        penalty = 0
        for ideal, p in zip(p_perm, node.pivot_prefix):
            penalty += max(0, p_dists[p] - p_dists[ideal])
        return penalty / node.lvl


class _Node:
    def __init__(self, lvl: int, pivot_prefix: Tuple[int]):
        self.lvl = lvl
        self.pivot_prefix = pivot_prefix

    def accept(self, visitor: '_Visitor'):
        pass


class _InternalNode(_Node):
    def __init__(self, lvl: int, pivot_prefix: Tuple[int]):
        super().__init__(lvl, pivot_prefix)
        self.children: List[_Node] = [None] * PIVOT_COUNT

    def accept(self, visitor: '_Visitor'):
        return visitor.visit_internal(self)


class _LeafNode(_Node):
    def __init__(self, lvl: int, pivot_prefix: Tuple[int]):
        super().__init__(lvl, pivot_prefix)
        self.min = 0
        self.max = self.min
        self.obj_count = 0

    def accept(self, visitor: '_Visitor'):
        return visitor.visit_leaf(self)


class _Visitor:
    def visit_internal(self, node: _InternalNode):
        pass

    def visit_leaf(self, node: _LeafNode):
        pass


class _InsertVisitor(_Visitor):
    def __init__(self, obj: Photo, pivots: List[Pivot]):
        self.obj = obj
        self.obj_permutation = np.argsort([
            getattr(obj, f'p{i}') for i in range(PIVOT_COUNT)
        ])
        self.obj.key = 0
        self.parent = None
        self.pivots = pivots

    def visit_internal(self, node: _InternalNode):
        next_id = self.obj_permutation[node.lvl]
        self.obj.key *= PIVOT_COUNT
        self.obj.key += next_id
        self.parent = node
        if node.children[next_id] is None:
            node.children[next_id] = _LeafNode(
                node.lvl + 1, (*node.pivot_prefix, next_id))
        node.children[next_id].accept(self)

    def visit_leaf(self, node: _LeafNode):
        if node.lvl < ClusterTree.L_MAX and node.obj_count == ClusterTree.LEAF_SPLIT_AT:
            self.__split_leaf(node)
            return

        frac = getattr(self.obj, f'p{node.pivot_prefix[0]}')
        self.obj.key += frac
        if node.obj_count == 0:
            node.min = node.max = self.obj.key
        elif self.obj.key < node.min:
            node.min = self.obj.key
        elif self.obj.key > node.max:
            node.max = self.obj.key
        node.obj_count += 1

    def __split_leaf(self, node: _LeafNode):
        junction = _InternalNode(node.lvl, node.pivot_prefix)
        self.parent.children[node.pivot_prefix[-1]] = junction
        to_insert = self.obj
        query = select(Photo).where(Photo.key.between(node.min, node.max))
        if to_insert.id != None:
            query = query.where(Photo.id < to_insert.id)
        for obj in it.chain(alchemy.session.execute(query).scalars(), (to_insert, )):
            obj.key = to_insert.key
            self.obj = obj
            self.parent = junction
            junction.accept(self)
