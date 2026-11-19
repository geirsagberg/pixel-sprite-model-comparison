# Dots leave the layer underneath visible. Each string is one row.
PALETTE = {
    ".": "000000", "#": "241e32", "n": "383852", "d": "51506a",
    "t": "226464", "g": "338a78", "m": "72bb8c", "o": "b74d38",
    "r": "ef8350", "y": "ffcb78", "s": "be7962", "p": "f5b98a",
    "b": "72434a", "l": "a56a51", "h": "d59b62",
}

# Hat, face, scarf, jacket and belt. Left edge x=8, top y=2.
BODY = '''
..........##.....
.........#ry#....
......####r#.....
....##mmgt#......
...#mgggggt#.....
..#gggggggtt#....
.#gttbbhhbbb##...
.####ggggggggg##.
.....#bbpspp###..
.....#bppsp#p#...
.....#bsp spp##..
......#ssppppp#..
...####orrss##...
.##rrroorrrr#....
#ro###ttgooo#....
###.#gggggtt#....
....#gggggtt#....
....#mggggtt#....
....#bbbyybb#....
....#tttggtt#....
....#########....
'''.replace(' ', '')

PACK = '''
..####.
.#hllb#
#hhllb#
#llhbb#
#bbybb#
#llhlb#
.#bbb#.
..###..
'''

# Poses are registered to the ground at y=29. Coordinates precede each grid.
LEGS = [
    (7,20, '''.........####
........#ddd#
.......#ddd#.
......#ndd#..
.....#ndd#...
....#bdd#....
...#lbb#.....
..#lbb#......
.#bbhb#......
..####.......'''),
    (9,21, '''......####
......#dd#
......#dd#
.....#dd#.
...###dd#.
..#bldd#..
.#lbb##...
#lbb#.....
.###......'''),
    (12,20, '''...####
...#dd#
....#dd#
....#ddd#
....##dd#
..##lbdd#
.#lbb###
..###'''),
    (15,19, '''####
#ddd##
.#dddd#
..##ddd#
...#dd#
..#lb#
.#lb#
..#bh#
...##'''),
    (15,20, '''####
#ddd##
.#dddd#
..##ddd#
....#dd#
.....#dd#
......#lb#
.......#lb##
........#bhh#
.........####'''),
    (15,21, '''####
#ddd##
.#dddd#
..##dd#
....#dd#
....#dd#
.....#lb#
.....#lbh##
.....######'''),
    (15,20, '''####
#ddd#
.#dd#
.#dd#
..#d#
..#dd#
..#dd#
..#lb#
..#lbh##
..######'''),
    (13,19, '''..####
..#dd#
..#dd#
..#dd#
..#dd#
..#dd#
.#dd#
.#lb#
#lbb#
#bbhh#
######'''),
]

# Near arm in eight swing positions. Shoulder height is relative to the torso.
ARMS = [
 (15, '''.####
.#mgg#
..#ggg#
...#ttg#
....#bb##
.....#ppp#
......###'''),
 (15, '''.####
.#mgg#
..#gg#
..#gtg#
...#bb#
....#pp#
....###'''),
 (15, '''.####
.#mgg#
.#ggg#
..#gt#
..#bb#
..#pp#
...##'''),
 (13, '''...####
...#mgg#
..#ggg#
..#gt#
.#bb#
.#pp#
..##'''),
 (10, '''......####
.....#mgg#
....#ggg#
...#ggt#
..#bb##
.#pp#
..##'''),
 (11, '''.....####
.....#mgg#
....#ggg#
...#ggt#
..#bb##
..#pp#
...##'''),
 (13, '''...####
...#mgg#
...#ggg#
..#ggt#
..#bb#
..#pp#
...##'''),
 (15, '''.####
.#mgg#
.#ggg#
..#gg#
..#bb##
...#ppp#
....###'''),
]
# (far leg, near leg, torso vertical offset, near arm)
FRAMES = [(4,0,0,0),(5,1,1,1),(6,2,0,2),(7,3,-1,3),
          (0,4,0,4),(1,5,1,5),(2,6,0,6),(3,7,-1,7)]
