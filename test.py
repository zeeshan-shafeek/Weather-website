from re import sub

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


print(camel_case('JavaScript'))
print(camel_case('Foo-Bar'))
print(camel_case('foo_bar'))
print(camel_case('--foo.bar'))
print(camel_case('Foo-BAR'))
print(camel_case('fooBAR'))
print(camel_case('foo bar'))