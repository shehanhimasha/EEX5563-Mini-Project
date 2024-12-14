class MemoryBlock:
    def __init__(self, start, end, is_free, block_id):
        self.start = start
        self.end = end
        self.is_free = is_free
        self.size = end - start
        self.block_id = block_id
        self.allocated_size = 0  # To track the allocated size

    def __repr__(self):
        return f"Block {self.block_id}: {self.size} KB"


class BestFitMemoryAllocator:
    def __init__(self, blocks):
        self.memory_blocks = blocks

    def allocate(self, request_size):
        best_fit_index = -1
        best_size = float('inf')

        # Find the best-fit block
        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= request_size:
                if block.size < best_size:
                    best_fit_index = i
                    best_size = block.size

        if best_fit_index != -1:
            block = self.memory_blocks[best_fit_index]
            original_size = block.size
            block.size -= request_size  # Reduce free size
            block.allocated_size += request_size  # Update allocated size

            # Update the block with remaining space
            if block.size == 0:
                block.is_free = False  # Fully allocated
            print(f"Allocated {request_size} KB to Block {block.block_id}")
            return True

        print(f"Failed to allocate {request_size} KB. Not enough space.")
        return False

    def display_memory(self):
        print("Memory State:")
        for block in self.memory_blocks:
            if block.allocated_size > 0:
                print(f"Block {block.block_id}: {block.size} KB (Free, Allocated {block.allocated_size} KB)")
            else:
                status = "Free" if block.is_free else "Allocated"
                print(f"Block {block.block_id}: {block.size} KB ({status})")


# Predefined memory blocks
memory_blocks = [
    MemoryBlock(0, 200, True, 1),
    MemoryBlock(200, 500, True, 2),
    MemoryBlock(500, 900, True, 3),
    MemoryBlock(900, 1000, True, 4),
    MemoryBlock(1000, 1150, True, 5)
]

# Initialize allocator
allocator = BestFitMemoryAllocator(memory_blocks)

# Display initial memory state
print("Initial Memory State:")
allocator.display_memory()

while True:
    request = input("\nEnter memory request size (in KB) or 'exit' to quit: ")
    if request.lower() == 'exit':
        break
    try:
        request_size = int(request)
        allocator.allocate(request_size)
        allocator.display_memory()
    except ValueError:
        print("Please enter a valid integer.")

print("\nFinal Memory State:")
allocator.display_memory()
