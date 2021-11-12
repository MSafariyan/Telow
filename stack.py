your_list = []

for i in range(5):

    x = str(input(f'Enter a string {i}/10:'))

    your_list.append(x)


for j in range(len(youdigitsr_list)-1,-1,-1):
    print(f"String {j}/10:{your_list[j]}")