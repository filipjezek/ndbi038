from typing import Tuple, List

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

    def __init__(self, pivots: List[Pivot]):
        self.root = _InternalNode(0, tuple())
        self.pivots = pivots
        self.root.children = [_LeafNode(1, (p.id - 1, )) for p in self.pivots]

    def insert_object(self, obj: Photo):
        """
        this will compute (and set) obj.key, posibly rehashing some other object keys
        """
        self.root.accept(_InsertVisitor(obj, self.pivots))


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

        frac = distance(self.obj.clip_features,
                        self.pivots[node.pivot_prefix[0]].clip_features)
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
