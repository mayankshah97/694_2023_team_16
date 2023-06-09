import pickle

class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self):
        self.capacity = 20 # Capacity of the cache is currently set to 20 elements
        
        self.filename = 'cache.pickle' # Local file name which will be written to the disc
        
        self.dic = {} # Initializing the dictionary
        
        # Creating the Doubly Linked List
        self.head = ListNode(None, None) 
        self.tail = ListNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.load_cache_from_file()
    
    # remove the key node.
    # insert the key node after the head.
    # return the value of the key.
    def get(self, key):
        if key not in self.dic:
            return None
        
        node = self.dic[key]
        self.remove_node(node)
        self.add_to_head(node)
        return node.value
    
    # if the key is already in the cache, we update the value, remove the key node and insert the key node after the head;
    # if the key is not in cache, if the cache is not full,we insert the new key node after the head. 
    # if the cache is full, we delete the node before the tail to make room for the new key node, and insert the new key node after the head.
    def put(self, key, value):
        if key in self.dic:
            node = self.dic[key]
            node.value = value
            self.remove_node(node)
            self.add_to_head(node)
        else:
            node = ListNode(key, value)
            self.dic[key] = node
            self.add_to_head(node)
            if len(self.dic) > self.capacity:
                tail_node = self.tail.prev
                self.remove_node(tail_node)
                del self.dic[tail_node.key]
        self.save_cache_to_file()
        print(self.dic.keys())
    
    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def add_to_head(self, node):
        head_next = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = head_next
        head_next.prev = node
    
    def save_cache_to_file(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.dic, f)
    
    def load_cache_from_file(self):
        try:
            with open(self.filename, 'rb') as f:
                self.dic = pickle.load(f)
                for node in self.dic.values():
                    self.add_to_head(node)
        except FileNotFoundError:
            pass
