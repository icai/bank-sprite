class Base(object):
    def __init__(self):
        print "Base created"

class ChildA(Base):
    def __init__(self):
    	print "Child A run!"
        Base.__init__(self)
        

class ChildB(Base):
    def __init__(self):
    	print "Child B run!"
        super(ChildB, self).__init__()


print ChildA(),ChildB()
# def main():
# 	print ChildA(),ChildB()

# if __name__ == '__main__':
# 	main()
	