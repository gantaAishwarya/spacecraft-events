Object-Oriented Programming (OOP) principles used in the provided CPP code are:


1. Abstraction: Data abstraction is a crucial concept of OOPS where we only provide teh necessary information about the data while
hiding the actual implemnetation behind. For example: the class SpaceObject and Orbit contains fileds name and semi_major_axis, eccentricity which
are protected and private to the respective classes i.e, no other class has access to these data fields but other classes can access the
public member functions such as get_name and get_semi_major_axis(), get_eccentricity() respectively.
In summary, this example demonstrates abstraction through the use of private data fields, public interfaces, inheritance, and 
encapsulation, adhering to key principles of object-oriented programming. It allows users to interact with the
objects at a higher level of abstraction without being concerned with the internal complexities of the implementation.


2. Encapsulation: Encapsulation is the concept of combining member functions and member fields into a single class unit.
In the provided example the three classes are used which are 1)SpaceObject, 2) Orbit, and 3) Satellite. Here, each class comprises of
respective data fields and member functions which also includes constructors, getters and setters.

- Furthermore, the data fields of the classes are well defined as private or protected and the public member functions provide controlled
access to this private data. For instance: Both the Satellite and Orbit classes encapsulate their respective attributes and behaviors.
The internal state of the objects (coordinates, orbit details) is encapsulated within the classes, and external code accesses this
information through well-defined methods.

3. Inheritance: Inheritance is one of the crucial properties in OOPS where the children class inherits member fields or functions from 
One or more parent classes. In the provided code we can see that Satellite class is derived from the SpaceObject class which demonstrates
inhertance. To be specific, Satellite class inherits the name data field from SpaceObject and extends it with additional members and methods.

4. Polymorphism: Polymorphism is a concept where a function or an operator is present with more than one definition. In given example:
polymorphism is used in the provided code through inheritance and function overriding. In this code:
auto get_name() const -> std::string override { return name; } : Function overriding is done where the Satellite class overrides
the get_name function from the SpaceObject class. This enables code reuse and flexibility in handling different types of space objects
while maintaining a common interface.

