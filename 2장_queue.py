class Queue(object):
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)

queue = Queue()
queue.enqueue('Red')
queue.enqueue('Green')
queue.enqueue('Blue')
queue.enqueue('Yellow')

print(queue.size())