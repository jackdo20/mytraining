print('input your height in meters')
height=input()
print('input your weight in kg')
weight=input()

bmi=weight/(height*height)

print('your bmi is:',bmi)

if bmi<18.5:
	print('you just like a paper!')
elif bmi<25:
	print('perfect gay!!')
elif bmi<28:
	print('over weight')
elif bmi<32:
	print('fat man')
else:
	print("you are such a pig!")
