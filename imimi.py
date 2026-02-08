import re
string = 'as32.4..Fh.d6kJ3.94asd'
pattern = r'.\.\D\d\w{2}'
print(re.findall(pattern,string))