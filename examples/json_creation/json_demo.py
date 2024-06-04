from flighthouse import create_json

''' 
There is no demo here yet, but you can use the create_json method
to create a json file that is compatible with the visualisers. 
The method takes a list of vehicle paths and a list of building vertices.
eg: 
contents = create_json(vehicles:list[list], obstacles:list[list], file_path:str)

vehicles is a list of lists of vehicle paths: ie [path1, path2, path3]
each path is itself a list: path1 = [[x,y,z], [x,y,z] etc...]
buildings is a list of lists of building vertices: ie [vertices1, vertices2 etc]
each vertices entry is itself a list: vertices1 = [[x,y,z], [x,y,z] etc...]
if file_path is given, the case is saved to that path

'''
