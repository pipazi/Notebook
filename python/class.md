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

class Test(object):
    before = 6
    def __init__(self):
        self.value = 5
    
    @classmethod
    def map(cls):
        print(cls.before + 1)
```

## inherit
* always use super for inheritation
* super().__init__(value) == super(__class__, self).__init__(value)
