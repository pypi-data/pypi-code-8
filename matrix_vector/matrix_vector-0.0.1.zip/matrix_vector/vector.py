
class DifferentDimensionVectors(BaseException):
	pass
"""
  class implementing vectors
"""

class Vector:
    """
     Initialize a Vector object.
     
     Example:
       >> Vector(1, 2, 3)
       => <matrix_vector.vector.Vector object>
    
     Arguments:
       N numbers

    """
    def __init__(self, *args):
        self.coordinates = list(args)

    # Returns the size of the vector(number of coordinates).
    # 
    # Example:
    #   >> Vector(1, 2, 3).size
    #   => 3
    #
    # Arguments:
    #   No arguments

    @property
    def size(self):
        return len(self.coordinates)

    def __len__(self):
        return self.size

    # Adds two vectors or adds a number to the elements of vector. Returns a new object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) + Vector(4, 5, 6)
    #   => Vector(5, 7, 9)
    #
    # Example:
    #   >> Vector(1, 2, 3) + 3
    #   => Vector(4, 5, 6)
    #
    # Arguments:
    #   vector : (Vector)
    #   or
    #   number : (Numeric)

    def __add__(self, other):
        if type(other) is Vector:
            if other.size == self.size:
                return Vector(*[x + y for x, y in
                                zip(self.coordinates, other.coordinates)])
            else:
                raise DifferentDimensionVectors
        else:
            return Vector(*[x + other for x in self.coordinates])
    
    # Substracts two vectors or substracts a number from the elements of the vector. Returns a new object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) - Vector(4, 5, 6)
    #   => Vector(-3, -3, -3)
    #
    # Example:
    #   >> Vector(1, 2, 3) - 3
    #   => Vector(-2, -1, 0)
    #
    # Arguments:
    #   vector : (Vector)
    #   or
    #   number : (Numeric)

    def __sub__(self, other):
        if type(other) is Vector:
            if other.size == self.size:
                return Vector(*[x - y for x, y in
                                zip(self.coordinates, other.coordinates)])
            else:
                raise DifferentDimensionVectors
        else:
            return Vector(*[_ - other for _ in self.coordinates])

    # Adds two vectors or adds a number to the elements of the vector. Changes the object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) += Vector(4, 5, 6)
    #   => Vector(5, 7, 9)
    #
    # Example:
    #   >> Vector(1, 2, 3) += 3
    #   => Vector(4, 5, 6)
    #
    # Arguments:
    #   vector : (Vector)
    #   or
    #   number : (Numeric)

    def __iadd__(self, other):
        self = self + other
        return self

    # Substracts two vectors or substracts a number from the elements of the vector. Changes the object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) -= Vector(4, 5, 6)
    #   => Vector(-3, -3, -3)
    #
    # Example:
    #   >> Vector(1, 2, 3) -= 3
    #   => Vector(-2, -1, 0)
    #
    # Arguments:
    #   vector : (Vector)
    #   or
    #   number : (Numeric)

    def __isub__(self, other):
        self = self - other
        return self

    # Access elements of the vector with [] operator
    # 
    # Example:
    #   >> Vector(1, 2, 3)[2]
    #   => 3
    #
    # Arguments:
    #   number : (int)

    def __getitem__(self, key):
    	return self.coordinates[key]

    # Depending on the argument either multiplies a number with the elements of the vector or finds the scalar product of two vectors.
    # 
    # Example:
    #   >> Vector(1, 2, 3) * 2
    #   => Vector(2, 4, 6)
    #
    # Example(scalar product):
    #   >> Vector(1, 2, 3) * Vector(2, 2, 2)
    #   => 12
    #
    # Arguments:
    #   number : (Numeric)
    #   or
    #   vector : (Vector)

    def __mul__(self, other):
        if type(other) is Vector:
            if other.size == self.size:
                return sum(x * y for x, y in
                               zip(self.coordinates, other.coordinates))
            else:
                raise DifferentDimensionVectors("Can't multipy vectors with different dimensions")
        else:
            return Vector(*[_ * other for _ in self.coordinates])

    # Multiplies a number with the elements of the vector changing the object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) * 2
    #   => Vector(2, 4, 6)
    #
    # Arguments:
    #   number : (Numeric)

    def __imul__(self, other):
    	if type(self * other) is Vector:
    		self = self * other
    		return self
    	else:
    		raise TypeError("Can't assign number to Vector class object")

    # Returns the scalar product of two 3-dimension vectors. Returns new object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) ^ Vector(4, 5, 6)
    #   => Vector(-3, 6, -3)
    #
    # Arguments:
    #   vector : (Vector)

    def __xor__(self, other):
        if self.size == other.size == 3:
            coordinate_x = self[1] * other[2] - self[2] * other[1]
            coordinate_y = self[2] * other[0] - self[0] * other[2]
            coordinate_z = self[0] * other[1] - self[1] * other[0]
            return Vector(coordinate_x, coordinate_y, coordinate_z)
        else:
        	raise TypeError("Vector product only defined for 3 dimensional vectors")
    
    # Returns the scalar product of two 3-dimension vectors. Changes the object.
    # 
    # Example:
    #   >> Vector(1, 2, 3) ^ Vector(4, 5, 6)
    #   => Vector(-3, 6, -3)
    #
    # Arguments:
    #   vector : (Vector)

    def __ixor__(self, other):
        self = self ^ other
        return self

    # Divides the elements of the vector by a nubmer. Returns new object.
    # 
    # Example:
    #   >> Vector(3, 9, 6) / 3
    #   => Vector(1, 3, 2)
    #
    # Arguments:
    #   number : (Numeric)

    def __truediv__(self, other):
    	try:
    	    return Vector(*[ _ / other for _ in self.coordinates])
    	except ZeroDivisionError:
    		raise
    
    # Divides the elements of the vector by a nubmer. Changes the object.
    # 
    # Example:
    #   >> Vector(3, 9, 6) / 3
    #   => Vector(1, 3, 2)
    #
    # Arguments:
    #   number : (Numeric)

    def __itruediv__(self, other):
    	self = self / other
    	return self
    
    # Returns the length of the vector.
    # 
    # Example:
    #   >> Vector(1, 2, 3).length
    #   => 3.7416
    #
    # Arguments:
    #   No arguments

    @property
    def length(self):
    	return sum(_ ** 2 for _ in self.coordinates) ** 0.5
    
    # Returns the normalized vector of the vector.
    # 
    # Example:
    #   >> Vector(1, 2, 3).normalized()
    #   => Vector(0.2672, 0.5345, 0.8017)
    #
    # Arguments:
    #   No arguments

    def normalized(self):
    	return self / self.length
    
    # Normalizes the vector. Changes the object.
    # 
    # Example:
    #   >> Vector(1, 2, 3).normalize()
    #   => Vector(0.2672, 0.5345, 0.8017)
    #
    # Arguments:
    #   No arguments

    def normalize(self):
    	self = self.normalized()
    	return self


    def __eq__(self, vector):
        return self.coordinates == vector.coordinates


    def print_vector(self):
    	for _ in self.coordinates:
    		print(_, end='   ')
    	print()
