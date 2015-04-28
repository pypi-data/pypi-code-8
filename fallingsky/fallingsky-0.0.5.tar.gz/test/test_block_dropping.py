"""Testing the collision/reexplosion detection for block falling."""

import mock
import pytest
import pygame
from collections import defaultdict
from fallingsky.game import GameBoard

def print_xydict(xydict):

    for row in range(min(xydict), max(xydict), 16):
        print("Y AXIS {}: X MEMBERS: {}".format(
            row,
            " ".join([str(x) for x in sorted(xydict.get(row, []))]),
        ))


def test_buggy_fall():

    # setup
    destroyed_lines = [496, 544]
    input_coords = [
        (432, 464), (480, 416), (496, 480), (528, 432), (448, 416), (400, 432),
        (464, 512), (480, 576), (416, 400), (512, 464), (528, 416), (400, 464),
        (416, 448), (432, 368), (464, 592), (432, 576), (496, 512), (448, 512),
        (400, 512), (416, 336), (496, 592), (432, 480), (400, 592), (528, 448),
        (432, 432), (448, 480), (448, 464), (480, 560), (496, 528), (528, 528),
        (512, 528), (544, 560), (448, 432), (496, 432), (496, 448), (464, 448),
        (544, 512), (400, 416), (432, 528), (416, 416), (512, 416), (432, 336),
        (400, 448), (496, 464), (416, 464), (432, 352), (464, 576), (480, 592),
        (480, 432), (464, 528), (480, 512), (432, 512), (496, 560), (432, 448),
        (448, 528), (416, 352), (496, 576), (432, 400), (400, 576), (432, 416),
        (512, 576), (464, 400), (528, 560), (512, 560), (464, 480), (528, 592),
        (544, 576), (480, 480), (528, 512), (528, 480), (400, 400), (416, 384),
        (512, 448), (400, 480), (416, 432), (512, 432), (432, 320), (416, 480),
        (432, 592), (528, 464), (464, 560), (448, 560), (400, 528), (480, 528),
        (416, 320), (432, 560), (512, 480), (416, 368), (416, 560), (432, 384),
        (448, 592), (448, 448), (416, 592), (512, 592), (416, 512), (464, 464),
        (480, 448), (528, 576), (544, 528), (464, 416),
    ]

    in_dict = defaultdict(list)
    out_dict = defaultdict(list)

    for x, y in input_coords:
        in_dict[y].append(x)

    game = GameBoard()
    game.blocks = {}
    for coord in input_coords:
        mock_block = mock.MagicMock()
        mock_block.rect.x = coord[0]
        mock_block.rect.y = coord[1]
        mock_block.bonus_points = 0
        game.blocks[coord] = mock_block
    game.blocksize = 16
    game.bonus_blocks = []
    game.width = 10
    game.height = 25
    game.lines_until_speed_up = 20

    # run the actual test
    game.blocks_fall_down(destroyed_lines)

    # inspections...
    for x, y in game.blocks.keys():
        out_dict[y].append(x)

    # assert we've moved correctly
    for coord, block in game.blocks.items():
        assert block.rect.x == coord[0]
        assert block.rect.y == coord[1]

    for line in destroyed_lines:
        # these lines should now have blocks fallen into them
        assert out_dict[line]

    assert game.blocks is None


if __name__ == "__main__":
    pygame.init()
    pytest.main(["-rx", "-v", "--pdb", __file__])
