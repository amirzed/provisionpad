import re

a = r''' 
Example
### Amir This is a very annoying string
that takes up multiple lines
bbb
and h@s a// kind{s} of stupid symbols in it
### Amir ok String'''

# with open('text.in', 'r') as f:
#     a = f.read()

c = re.sub('\n### Amir.*?### Amir','',a, flags=re.DOTALL)

print (a.strip())