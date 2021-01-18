#!/usr/bin/env python3

# need "pip install pygraphviz"
# which requires a local installation of graphviz
from pygraphviz import AGraph
# https://pygraphviz.github.io/documentation/latest/reference/agraph.html
import random
from typing import Tuple

# import the data structures from a separate file
from browse_internet import list_of_task_dicts

def smush(tup: Tuple[str, str, str]) -> str:
    """
    since I'm using tuples and need to get strings, merge the tuple items with underscores
    """
    return '_'.join(tup).replace(" ","_").replace(':','').replace('-','').replace('.','').replace(',','').replace('(','').replace(')','').replace('__','_').replace("'","")

def with_spaces(tup: Tuple[str, str, str]) -> str:
    """
    convert tuple to a string with spaces
    if the line is long, insert line breaks
    """
    tup_as_str = ' '.join(tup)
    if len(tup_as_str)>60: # insert line breaks in long strings to reduce width of nodes
        ary = tup_as_str.split(" ")
        new_str = ""
        for index, wrd in enumerate(ary):
            new_str+=wrd+" "
            if index == int(len(ary)/2):
                new_str += "\n"
        return new_str.strip()
    return tup_as_str

def task_has_children_in_list_of_task_dicts(task_tuple_to_test: Tuple[str, str, str], list_of_task_dicts: list) -> bool:
    """
    is a tuple present as a key in the list of dicts?

    returns True if task_tuple_to_test has child tasks in list_of_task_dicts
    otherwise returns False (when there are no child tasks in list_of_task_dicts)
    """
    for task_dist in list_of_task_dicts:
        if task_tuple_to_test in task_dist.keys():
            return True
    return False

def subgraph(task_tuple_to_test: Tuple[str, str, str], list_of_task_dicts: list) -> list:
    """

    """
    for task_dist in list_of_task_dicts:
        if task_tuple_to_test in task_dist.keys():
            return list(task_dist.values())[0]
    return None

if __name__ == "__main__":
    use_case = AGraph(directed=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")

    for edge_pair in list_of_task_dicts[0]["user story"]:
        #print(with_spaces(edge_pair[0]),"to", with_spaces(edge_pair[1]))

        if task_has_children_in_list_of_task_dicts(edge_pair[0], list_of_task_dicts):
            sg = use_case.subgraph(name="cluster_"+smush(edge_pair[0]),
                                   label=with_spaces(edge_pair[0]))
            sg.add_node(smush(edge_pair[0]), style="invis")
            for sg_edge_pair in subgraph(edge_pair[0],list_of_task_dicts):
                if(len(sg_edge_pair)==3): # single node
                    sg.add_node(smush(sg_edge_pair),label=with_spaces(sg_edge_pair))
                else:
                    print(sg_edge_pair)
        else: # node does not have children
            use_case.add_node(smush(edge_pair[0]),label=with_spaces(edge_pair[0]))

        if task_has_children_in_list_of_task_dicts(edge_pair[1], list_of_task_dicts):
            sg = use_case.subgraph(name="cluster_"+smush(edge_pair[1]),
                                   label=with_spaces(edge_pair[1]))
            sg.add_node(smush(edge_pair[1]), style="invis")
        else:
            use_case.add_node(smush(edge_pair[1]),label=with_spaces(edge_pair[1]))
        use_case.add_edge(smush(edge_pair[0]),smush(edge_pair[1]))


    use_case.write("single_layer.dot")
    use_case.draw("single_layer.svg", format="svg", prog="dot")
