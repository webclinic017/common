class C:
    '''
    test
    '''
    count = 0
    
a = C()
b = C()
c = C()
print(a.count, b.count, c.count)

a.count += 10
print(a.count, b.count, c.count)

print(C.__name__)
print(C.__doc__)
print(C.__bases__)
print(C.__dict__)
print(C.__module__)
print(C.__class__)