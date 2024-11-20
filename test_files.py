file = open("test_file.txt", "a")

file.write("Hello World\n")
file.write("1234\n")

for i in range(100):
    file.write("Hello World\n")

file.close()

file = open("test_file.txt", "r")

content = file.read(10)
print(content)

file.close()