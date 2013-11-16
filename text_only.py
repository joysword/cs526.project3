from map_generator import *


new_dungeon = Dungeon((15, 10), "Neverland", 0, (3, 3), (4, 4), (8, 8))

new_dungeon.generate_dungeon()

new_dungeon.print_info(True)
