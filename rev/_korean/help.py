with open('program.txt', 'r') as f:
    map_data = [list(row) for row in f.read().split('\n')]

width, height = len(map_data[0]), len(map_data)-1
visited = [[False for j in range(width)] for i in range(height)]

def backtrack(x, y):
    if visited[y][x]:
        return
    visited[y][x] = True

    val = ord(map_data[y][x]) - 0xAC00
    if val // 588 == 17:
        return
    
    is_conditional = (val // 588) in [15, 16]
    vowel = (val // 28) % 21

    print(x, y, vowel)

    if vowel == 2:
        dx, dy = 2, 0
    elif vowel == 0:
        dx, dy = 1, 0
    elif vowel == 6:
        dx, dy = -2, 0
    elif vowel == 4:
        dx, dy = -1, 0
    elif vowel == 12:
        dx, dy = 0, -2 
    elif vowel == 8:
        dx, dy = 0, -1 
    elif vowel == 17:
        dx, dy = 0, 2
    elif vowel == 13:
        dx, dy = 0, 1 
    else:
        print(x, y, vowel)
        exit(0)

    backtrack(x+dx, y+dy)
    if is_conditional:
        backtrack(x-dx, y-dy)

backtrack(0, 0)
print(f"height: {height}, width: {width}")

for i in range(height):
    for j in range(width):
        if not visited[i][j]:
            map_data[i][j] = '  '

with open('program_deobf.txt', 'w') as f:
    for i in range(height):
        f.write(''.join(map_data[i]) + '\n')
