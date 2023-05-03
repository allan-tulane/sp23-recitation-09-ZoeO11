from collections import deque
import heapq
from heapq import heappush, heappop 
from functools import reduce

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    result = {}
  
    for v in graph:
      result[v] = float('inf'), float('inf')
      
    result[source] = (0, 0)
    heap = [(0, 0, source)]
  
    while len(heap) != 0:
        weight, edges, node = heapq.heappop(heap)
        if (weight, edges) > result[node]:
            continue
        for neighbor, edge_weight in graph[node]:
            new_weight = weight + edge_weight
            new_edges = edges + 1
            if new_weight < result[neighbor][0] or (new_weight == result[neighbor][0] and new_edges < result[neighbor][1]):
                result[neighbor] = (new_weight, new_edges)
                heapq.heappush(heap, (new_weight, new_edges, neighbor))
    return result
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
  
    parents = {source: source}
    list = [source]
  
    while len(list) != 0:
        current = list.pop(0)
        for neighbor in graph[current]:
            if neighbor not in parents:
                list.append(neighbor)
                parents[neighbor] = current
              
    return parents

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    path = []
    result = "s"
    destination = parents[destination]
  
    while destination != parents[destination]:
        path.append(destination)
        destination = parents[destination]
      
    path.reverse()
  
    for i in path:
      result = result + i
      
    return result

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'