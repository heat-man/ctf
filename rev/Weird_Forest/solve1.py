from z3 import *
import re


for bp in range(0, 256):
    print(bp)
    s = Solver()

    d = open('./output', 'r').read()
    test = re.split('🌴', d)[1:-1]
    cnt = len(test) + d.count('🎄')+2
    # print(cnt, test)

    x = [BitVec(f'x_{i}', 8) for i in range(cnt)]
    bs = {'🌲':'>', '🌳':'<'}
    tree = {'':0}
    i = 1
    test_i = 0
    m = 0
    next = True
    while i < cnt:
        s.add(Or(And(x[i] ^ bp >= 48, x[i] ^ bp <= 58), And(65 <= x[i] ^ bp, x[i] ^ bp <= 90), And(97 <= x[i] ^ bp, x[i] ^ bp <= 123), x[i] ^ bp == 125, x[i] ^ bp == 46, x[i] ^ bp == 44,  x[i] ^ bp == 45, x[i] ^ bp == 32))
        # s.add(x[i] >= 0)
        # s.add(x[i] <= 255)
        j = 0

        # print(m, len(test[test_i]), test[test_i][m:])
        
        node = ''
        while j < len(test[test_i][m:]):
            k = test[test_i][j+m]
            if k == '🎄':
                # print(f's.add(x[{i}] == x[{tree[node]}])')
                s.add(x[i] == x[tree[node]])
                m += j + 1
                break
            # print(f's.add(x[{i}] {bs[k]} x[{tree[node]}])')
            exec(f's.add(x[i] {bs[k]} x[tree[node]])')
            node += bs[k]        
            j += 1        

        if next:        
            m = 0
            test_i += 1
            next = False

        if test_i == len(test):
            break
        if '🎄' not in test[test_i][m:]:
            next = True

        if node not in tree:
            tree[node] = i
        i += 1
    # print(i)
    # print(tree)

    models = []
    
    while s.check() != unsat:
        model = s.model()
        result = [int(str(model[x[i]])) for i in range(cnt-1)]
        flag = bytes(x ^ bp for x in result).decode()
        models.append(result)
        exec(f"s.add({'Not(And(' + ','.join([f'{result[i]} == x[{i}]' for i in range(len(result))]) + '))'})")
        if 'DH{' in flag:
            print('************', flag)
