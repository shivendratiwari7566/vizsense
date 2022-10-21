file=r'../../modelserving/models.config.e'

text_file = open(file, "r")

#read whole file to a string
data = text_file.read()

#close file
text_file.close()

print(data)



