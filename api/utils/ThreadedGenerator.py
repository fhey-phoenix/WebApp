import queue

class ThreadedGenerator:
    """A class to create a generator running in a separate thread."""
    
    def __init__(self):
        """Initialize the ThreadedGenerator with a queue."""
        self.queue = queue.Queue()

    def __iter__(self):
        """Iterate over the items in the queue."""
        while True:
            item = self.queue.get()
            if item is StopIteration:
                return
            yield item

    def __next__(self):
        """Get the next item from the queue."""
        item = self.queue.get()
        if item is StopIteration:
            raise item
        return item

    def send(self, data):
        """Put data into the queue."""
        self.queue.put(data)

    def close(self):
        """Put a StopIteration signal into the queue."""
        self.queue.put(StopIteration)
