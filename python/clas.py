class Menu(object):
    menu=[]
    i=0
    def __init__(self,mn):
        self.menu.append(mn)

    def show_menu(self):
        print('your menu is:')
        for i in self.menu:
            print( i)
print('Please order your food!')
while True:
    food=raw_input()
    if food=='ok':
        m.show_menu()
        break
    else:
       # food=raw_input()
        m=Menu(food)

