import itertools

keys = list(itertools.combinations('CCSSTT', r=2))
# for entry in keys:
#     print(entry)
print(f"Keys count: {len(keys)}")

possible_list = list(itertools.combinations_with_replacement(keys, r=3))
print(f"Possible count: {len(possible_list)}")
combination_list = []
for entry in possible_list:
    c_total = 0
    s_total = 0
    t_total = 0
    for key in entry:
        for bit in key:
            if bit == 'C': c_total = c_total + 1
            if bit == 'S': s_total = s_total + 1
            if bit == 'T': t_total = t_total + 1
    if c_total == 2 and s_total == 2 and t_total == 2 and entry not in combination_list:
        combination_list.append(entry)

for e in combination_list:
    print(e)