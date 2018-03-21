class LocalizationManager():
  def __init__(self, path):
    self.path = path

  def get_route(self, a, b):
    return self.dijkstra(self.path, a, b);

  # Cite
  # http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
  def dijkstra(self, graph,src,dest,visited=[],distances={},predecessors={}):
    # Ending condition, build shortest path
    if src == dest:
      path=[]
      pred=dest
      while pred != None:
        path.append(pred)
        pred=predecessors.get(pred,None)
      return (distances[dest], path[::-1])
    else :     
      # if it is the initial  run, initializes the cost
      if not visited: 
        distances[src]=0

      # visit the neighbors
      src_vertex = graph.get_vertex(src)

      for neighbor_vertex in src_vertex.get_connections():
        neighbor = neighbor_vertex.id
        if neighbor not in visited:
          new_distance = distances[src] + src_vertex.get_weight(neighbor_vertex)
          if new_distance < distances.get(neighbor,float('inf')):
            distances[neighbor] = new_distance
            predecessors[neighbor] = src
      # mark as visited
      visited.append(src)
      # now that all neighbors have been visited: recurse                         
      # select the non visited node with lowest distance 'x'
      # run Dijskstra with src='x'
      unvisited={}
      for k_vert in graph:
        k = k_vert.id
        if k not in visited:
          unvisited[k] = distances.get(k,float('inf'))        
      x=min(unvisited, key=unvisited.get)
      return self.dijkstra(graph,x,dest,visited,distances,predecessors)