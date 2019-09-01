with open('files\mumber.txt') as f:
    content=f.readlines()
content=[x.strip() for x in content]
print(content)
if '12' in content:
    print('yes')
    content.remove('12')
    print(content)