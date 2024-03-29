def heappop(heap,reverse=False):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0,reverse)
        return returnitem
    return lastelt

def _siftup(heap, pos,reverse=False):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if reverse:
            if rightpos < endpos and not heap[childpos].reverse_dist < heap[rightpos].reverse_dist:
                childpos = rightpos
        else:
            if rightpos < endpos and not heap[childpos].dist < heap[rightpos].dist:
                childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown(heap, startpos, pos,reverse)   

def heappush(heap, item,reverse=False):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1,reverse)

def _siftdown(heap, startpos, pos,reverse=False):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if reverse:
            if newitem.reverse_dist < parent.reverse_dist:
                heap[pos] = parent
                pos = parentpos
                continue
            break
        else:
            if newitem.dist < parent.dist:
                heap[pos] = parent
                pos = parentpos
                continue
            break
    heap[pos] = newitem

def decrease_key(heap, node,reverse=False):
    i = heap.index(node)
    while i:
#       # calculate the offset of the parent       
        parentpos = (i - 1) >> 1
        if reverse:
            if heap[parentpos].reverse_dist < heap[i].reverse_dist:
                break
        else:
            if heap[parentpos].dist < heap[i].dist:
                break
        _swap(heap,i, parentpos)
        i = parentpos

def _swap(heap, i, j):
    heap[i], heap[j] = heap[j], heap[i]

