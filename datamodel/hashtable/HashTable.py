
class HashTable:
    def __init__(self, n_buckets):
        self.n_buckets = n_buckets
        self.length = 0

        # build indexing array  [None], [None], ... [None]
        self.array = [[] for i in range(n_buckets)]

    def insert(self, item, *key):
        # if key provided, convert to integer for use as hashed key
        if key[0]:
            key = int(key[0])
            hashkey = hash(key)
        else:  # else use the item itself as key
            if isinstance(item, list):
                item = str(item)
            hashkey = hash(item)

        index = hashkey % self.n_buckets
        keyvalue = (hashkey, item)
        self.array[index].append(keyvalue)
        self.length += 1

    def find(self, key):
        if isinstance(key, list):
            item = str(key)
        hashkey = hash(key)
        index = hashkey % self.n_buckets
        for item in self.array[index]:
            if item[0] == hashkey:
                return item[1]
            else:
                return None
        return None

    def remove(self, key):
        hashkey = hash(key)
        index = hashkey % self.n_buckets
        for n, item in enumerate(self.array[index]):
            if item[0] == hashkey:
                del self.array[index][n]
                self.length -= 1
            else:
                return None
        return None

    def __str__(self):
        string = ""
        for i in self.array:
            string += str(i) + "\n"
        return string

    def __len__(self):
        return self.length

