import itertools as it
from enum import Enum
from typing import List
from pathlib import Path


class DisplayTypes(Enum):
    topk = 'topk'
    triangle = 'topk_triangle'


def triangle(fnames: List[str], w: int, h: int) -> List[str]:
    out = [[None] * w for _ in range(h)]
    x, y = 0, 0
    up = True
    for fname in fnames:
        out[y][x] = fname
        if up:
            if x + 1 == w:
                y += 1
                up = False
            elif y == 0:
                x += 1
                up = False
            else:
                x += 1
                y -= 1
        else:
            if y + 1 == h:
                x += 1
                up = True
            elif x == 0:
                y += 1
                up = True
            else:
                y += 1
                x -= 1
    return list(it.chain.from_iterable(out))


def get_filename(fname: str) -> str:
    static_dir = Path(__file__).joinpath('../static').resolve()
    # this is for serving the whole web using flask
    # return str(fname).relative_to(static_dir)
    # this is for serving the frontend using angular dev server
    return 'http://127.0.0.1:5000/' + str(Path(fname).relative_to(static_dir))
