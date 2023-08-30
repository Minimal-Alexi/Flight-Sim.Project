1.
user = input('Enter your name: ')
print('Hello, ' + user +"!")

2.
radius = int(input("Enter the radius of a circle: "))
circle_area = radius * radius * 3.14
print("Area of the circle is: " , circle_area)

3.
width = int(input("Enter the length of the rectangle: "))
height = int(input("Enter the height of the rectangle: "))
perimeter = width*2+height*2
area = width* height
print("Perimeter of rectangle is: ", perimeter)
print("area of rectangle is: ", area)

4.
n1=int(input("Insert number 1: "))
n2=int(input("Insert number 2: "))
n3=int(input("Insert number 3: "))
print("Sum of the numbers is:", n1+n2+n3)
print("Product of the numbers is:", n1*n2*n3)
print("Average of the numbers is:", (n1+n2+n3)/3)

5.
import math
talents = float(input("Enter talents: "))
pounds = float(input("Enter pounds: "))
lots = float(input("Enter lots: "))
mweight = talents*20*32*13.3+pounds*32*13.3+lots*13.3
mgram = mweight%1000
print("The weight in modern units is:/n")
print(int(mweight/1000),f" kilograms and {mgram:.3f}")

6.
