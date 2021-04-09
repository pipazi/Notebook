[返回目录](../README.md)
# Python class

## class life
```python
class Test(object):
    # 类的固有属性，可以不实例化直接调用
    before = 6
    
    # 初始化时执行
    def __init__(self):  # self means Instantiated class
        self.value = 5
    
    # 类的固有属性，可以不实例化直接调用
    @classmethod
    def map(cls):  # cls means class
        print(cls.before)  # cls can only get class attribute
    
    # 销毁时执行
    def __del__(self):
        print("destroy")
```

## cls/self
* self: Instantiated class
* cls: class before Instantiate

## classmethod
* use class method for Polymorphism
```python
class Test(object):
    before = 6
    def __init__(self):
        self.value = 5
    
    @classmethod
    def map(cls):
        print(cls.before)

class Test_(Test):
    @classmethod
    def map(cls):
        print(cls.before + 1)
```

## inherit
* always use super for inheritation
* super().\_\_init\_\_(value) == super(\_\_class\_\_, self).\_\_init\_\_(value)

## Magic Methods 
* 描述符 \_\_set\_\_ & \_\_get\_\_:
```python
class Grade(object):
    def __init__(self):
        self._value = 0

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError
        self._value = value

    def __get__(self, instance, instance_type):
        return self._value


class Exam(object):
    math = Grade()
    write = Grade()
    science = Grade()


first_exam = Exam()
first_exam.math = 90
first_exam.write = 89
first_exam.science = 99
```
* \_\_setitem\_\_ & \_\_getitem\_\_: 
```python
class Building(object):
     def __init__(self, floors):
         self._floors = [None]*floors
     def __setitem__(self, floor_number, data):
          self._floors[floor_number] = data
     def __getitem__(self, floor_number):
          return self._floors[floor_number]

building1 = Building(4) # Construct a building with 4 floors
building1[0] = 'Reception'
building1[1] = 'ABC Corp'
building1[2] = 'DEF Inc'
```
* property: @property / @property.setter
* \_\_setattr__ & \_\_getattribute\_\_ & \_\_getattr\_\_: 
  <br>(1) \_\_getattr\_\_ is only invoked if the attribute wasn't found the usual ways. It's good for implementing a fallback for missing attributes, and is probably the one of two you want.
  <br>(2) \_\_getattribute\_\_ is invoked before looking at the actual attributes on the object, and so can be tricky to implement correctly. You can end up in infinite recursions very easily.


