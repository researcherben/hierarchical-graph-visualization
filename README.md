
The nodes of the hyper graph can be expanded into graphs.


# research progression


I realized that the nested nature of a sequence of steps could be described using XML with nested `<task>` tags. 
--> I found that with a high nested depth the navigation was burdensome, even with the ability for XML nodes to be collapsed in Firefox
--> I found that some chunks of tasks are used repeatedly. However, XML does not support reuse of encapsulated snippets (without a more complicated schema).
--> I found that XML's linear sequence did not reflect the branching decision tree flow

I moved to Graphviz (using dreampuf.github.io) and manually created nodes and edges, then converting the top-level nodes into subgraphs. 
--> I found that every node eventually becomes a subgraph, which triggers relabeling of nodes and connections
--> Every node requires a unique name
--> reusing sequences meant copy-pasting snippets and manually renaming every variable

I started fresh with Graphviz and experimented with "everything is a subgraph". 
--> problem: invisible nodes (necessary for edges) take up space 

In a new Graphviz I manually split the hierarchy to limit the depth to 2. Each layer only contains subgraphs and nodes; no nested subgraphs.
--> Hyperlinking the nodes to other layers works well.
--> Automation is necessary to scale

Using Python with `import pygraphviz` is an obvious transition, but I don't have experience with which data structure 
would be appropriate for a hypergraph. 
--> Nested dictionaries would work for a tree, but do not for a graph
--> Although I can enter redundant keys in a dictionary, only the last key is actually used.

    >>> my_dict = {4: 94, 5:99, 4: 4942}
    >>> my_dict.keys()
    dict_keys([4, 5])
    >>> my_dict
    {4: 4942, 5: 99}

