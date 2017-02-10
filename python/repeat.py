'''name = ['Micheal','Bob','Luther']
for i in name:
	print(i)
'''
numbers=[]
i=0
nums=int(input('how many numbers you want?'))
summ=0
while i<nums:
    print('input number %d: ' % i)
    numbers.append(int(input()))
    i=i+1

print('-------------')
print('your number is:')
print(numbers)
print('-------------')
print('their sum is:')

#print(type(numbers[1]))
for el in numbers:
    summ=summ+el

print(summ)
