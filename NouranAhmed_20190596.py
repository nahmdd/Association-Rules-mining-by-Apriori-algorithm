import pandas as pd


df = pd.read_excel("/Users/shoroukeladawy/Desktop/CoffeeShopTransactions.xlsx", usecols=[2, 3, 4, 5])
# Stack the item columns on top of each other and create a new column containing the item values
df = df.set_index('Transaction Number').stack().reset_index().rename(columns={'level_1': 'Item Number', 0: 'Item'})
# Group the items by transaction ID
grouped = df.groupby('Transaction Number')['Item'].apply(lambda x: ' '.join(x)).reset_index()
# Convert the grouped data to list format
data = []
for _, row in grouped.iterrows():
    transaction_id = row['Transaction Number']
    items = row['Item'].split()
    transaction_list = [transaction_id, items]
    data.append(transaction_list)


initial_items = []
for transaction in data:
    for item in transaction[1]:
        if item not in initial_items:
            initial_items.append(item)
initial_items = sorted(initial_items)
minimum_support = float(input("Enter minimum support: "))
minimum_support_count = int(minimum_support * len(initial_items))

from collections import Counter
c1 = Counter()
for item in initial_items:
    for transaction in data:
        if item in transaction[1]:
            c1[item] += 1

print("C1:")
for item in c1:
    print(str([item]) + ": " + str(c1[item]))
print()

l1 = Counter()
for item in c1:
    if c1[item] >= minimum_support_count:
        l1[frozenset([item])] += c1[item]

print("L1:")
for item in l1:
    print(str(list(item)) + ": " + str(l1[item]))
print()

previous_l = l1
set_count = 1

#getting frequent sets
for count in range (2, 1000):
    new_candidates = set()
    previous_l_list = list(previous_l)
    for i in range(0, len(previous_l_list)):
        for j in range(i+1, len(previous_l_list)):
            new_set = previous_l_list[i].union(previous_l_list[j])
            if len(new_set) == count:
                new_candidates.add(previous_l_list[i].union(previous_l_list[j]))
    new_candidates = list(new_candidates)
    candidate_counter = Counter()
    for candidate in new_candidates:
        candidate_counter[candidate] = 0
        for transaction in data:
            transaction_items = set(transaction[1])
            if candidate.issubset(transaction_items):
                candidate_counter[candidate] += 1
    print("C" + str(count) + ":")
    for candidate in candidate_counter:
        print(str(list(candidate)) + ": " + str(candidate_counter[candidate]))
    print()
    new_l = Counter()
    for candidate in candidate_counter:
        if candidate_counter[candidate] >= minimum_support_count:
            new_l[candidate] += candidate_counter[candidate]
    print("L" + str(count) + ":")
    for itemset in new_l:
        print(str(list(itemset)) + ": " + str(new_l[itemset]))
    print()
    if len(new_l) == 0:
        break
    previous_l = new_l
    set_count = count

print("Result: ")
print("L" + str(set_count) + ":")
for itemset in previous_l:
    print(str(list(itemset)) + ": " + str(previous_l[itemset]))
print()

from itertools import combinations
minconf = float(input ("enter minimum confidence:"))
for l in previous_l:
    c = [frozenset(q) for q in combinations(l,len(l)-1)]
    for a in c:
        b = l-a
        ab = l
        sab = 0
        sa = 0
        sb = 0
        for q in data:
            temp = set(q[1])
            if(a.issubset(temp)):
                sa+=1
            if(b.issubset(temp)):
                sb+=1
            if(ab.issubset(temp)):
                sab+=1
        temp1 = sab/sa*100
        if(temp1 >= minconf):
          print(str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%")
        temp2 = sab/sb*100
        if(temp2 >= minconf):
            print(str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%")