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

def allinone(graph,edge_pair,list_of_task_dicts:list,parent_name:str):
    """
    """
    if task_has_children_in_list_of_task_dicts(edge_pair[0], list_of_task_dicts):
        sg = graph.subgraph(name="cluster_"+smush(parent_name)+smush(edge_pair[0]),
                               label=with_spaces(edge_pair[0]))
        sg.add_node(smush(parent_name)+smush(edge_pair[0]), style="invis")
        for sg_edge_pair in get_subgraph(edge_pair[0],list_of_task_dicts):
            if(len(sg_edge_pair)==3): # single node
                sg.add_node(smush(parent_name)+smush(sg_edge_pair),label=with_spaces(sg_edge_pair))
            else:
                allinone(sg,sg_edge_pair,list_of_task_dicts,smush(edge_pair[0]))
    else: # node does not have children
        graph.add_node(smush(parent_name)+smush(edge_pair[0]),label=with_spaces(edge_pair[0]))

    if task_has_children_in_list_of_task_dicts(edge_pair[1], list_of_task_dicts):
        sg = graph.subgraph(name="cluster_"+smush(parent_name)+smush(edge_pair[1]),
                               label=with_spaces(edge_pair[1]))
        sg.add_node(smush(parent_name)+smush(edge_pair[1]), style="invis")
        for sg_edge_pair in get_subgraph(edge_pair[1],list_of_task_dicts):
            if(len(sg_edge_pair)==3): # single node
                sg.add_node(smush(parent_name)+smush(sg_edge_pair),label=with_spaces(sg_edge_pair))
            else:
                allinone(sg,sg_edge_pair,list_of_task_dicts,smush(edge_pair[1]))
    else:
        graph.add_node(smush(parent_name)+smush(edge_pair[1]),label=with_spaces(edge_pair[1]))
    graph.add_edge(smush(parent_name)+smush(edge_pair[0]),
                   smush(parent_name)+smush(edge_pair[1]))
    return


def get_subgraph(task_tuple_to_test: Tuple[str, str, str], list_of_task_dicts: list) -> list:
    """

    """
    for task_dist in list_of_task_dicts:
        if task_tuple_to_test in task_dist.keys():
            return list(task_dist.values())[0]
    return None

def create_allinone():
    use_case = AGraph(directed=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")

    for edge_pair in list_of_task_dicts[0]["user story"]:
        #print(with_spaces(edge_pair[0]),"to", with_spaces(edge_pair[1]))
        allinone(graph=use_case,
                     edge_pair=edge_pair,
                     list_of_task_dicts=list_of_task_dicts,
                     parent_name="user story")

    use_case.write("allinone.dot")
    use_case.draw("allinone.svg", format="svg", prog="dot")

def create_linked_layers():
    use_case = AGraph(directed=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")

    for edge_pair in list_of_task_dicts[0]["user story"]:
        parent_name="user_story"
        if task_has_children_in_list_of_task_dicts(edge_pair[0], list_of_task_dicts):
            sg = use_case.subgraph(name="cluster_"+parent_name+smush(edge_pair[0]),
                                   label=with_spaces(edge_pair[0]))
            sg.add_node(parent_name+smush(edge_pair[0]), style="invis")
            for sg_edge_pair in get_subgraph(edge_pair[0],list_of_task_dicts):
                if len(sg_edge_pair)==3:
                    if task_has_children_in_list_of_task_dicts(sg_edge_pair, list_of_task_dicts):
                        sg.add_node(parent_name+smush(edge_pair[0])+smush(sg_edge_pair),
                                    label=with_spaces(sg_edge_pair),
                                    shape="rectangle",
                                    color="blue")
                    else:
                        sg.add_node(parent_name+smush(edge_pair[0])+smush(sg_edge_pair),
                                    label=with_spaces(sg_edge_pair))

                else: # actually a pair
                    if task_has_children_in_list_of_task_dicts(sg_edge_pair[0],list_of_task_dicts):
                        sg.add_node(parent_name+smush(edge_pair[0])+smush(sg_edge_pair[0]),
                                    label=with_spaces(sg_edge_pair[0]),
                                    shape="rectangle",
                                    color="blue")
                    else:
                        sg.add_node(parent_name+smush(edge_pair[0])+smush(sg_edge_pair[0]),
                                    label=with_spaces(sg_edge_pair[0]))
                    if task_has_children_in_list_of_task_dicts(sg_edge_pair[1],list_of_task_dicts):
                        sg.add_node(parent_name+smush(edge_pair[0])+smush(sg_edge_pair[1]),
                                    label=with_spaces(sg_edge_pair[1]),
                                    shape="rectangle",
                                    color="blue")
                    else:
                        sg.add_node(parent_name+smush(edge_pair[0])+smush(sg_edge_pair[1]),
                                    label=with_spaces(sg_edge_pair[1]))
                    sg.add_edge(parent_name+smush(edge_pair[0])+smush(sg_edge_pair[0]),
                                parent_name+smush(edge_pair[0])+smush(sg_edge_pair[1]),constraint=False)
        else: # node does not have children
            use_case.add_node(parent_name+smush(edge_pair[0]),
                              label=with_spaces(edge_pair[0]))
        if task_has_children_in_list_of_task_dicts(edge_pair[1], list_of_task_dicts):
            sg = use_case.subgraph(name="cluster_"+parent_name+smush(edge_pair[1]),
                                   label=with_spaces(edge_pair[1]))
            sg.add_node(parent_name+smush(edge_pair[1]), style="invis")
            for sg_edge_pair in get_subgraph(edge_pair[1],list_of_task_dicts):
                if len(sg_edge_pair)==3:
                    if task_has_children_in_list_of_task_dicts(sg_edge_pair, list_of_task_dicts):
                        sg.add_node(parent_name+smush(edge_pair[1])+smush(sg_edge_pair),
                                    label=with_spaces(sg_edge_pair),
                                    shape="rectangle",
                                    color="blue")
                    else:
                        sg.add_node(parent_name+smush(edge_pair[1])+smush(sg_edge_pair),
                                    label=with_spaces(sg_edge_pair))
                else:
                    if task_has_children_in_list_of_task_dicts(sg_edge_pair[0], list_of_task_dicts):
                        sg.add_node(parent_name+smush(edge_pair[1])+smush(sg_edge_pair[0]),
                                    label=with_spaces(sg_edge_pair[0]),
                                    shape="rectangle",
                                    color="blue")
                    else:
                        sg.add_node(parent_name+smush(edge_pair[1])+smush(sg_edge_pair[0]),
                                    label=with_spaces(sg_edge_pair[0]))
                    if task_has_children_in_list_of_task_dicts(sg_edge_pair[1], list_of_task_dicts):
                        sg.add_node(parent_name+smush(edge_pair[1])+smush(sg_edge_pair[1]),
                                    label=with_spaces(sg_edge_pair[1]),
                                    shape="rectangle",
                                    color="blue")
                    else:
                        sg.add_node(parent_name+smush(edge_pair[1])+smush(sg_edge_pair[1]),
                                    label=with_spaces(sg_edge_pair[1]))
                    sg.add_edge(parent_name+smush(edge_pair[1])+smush(sg_edge_pair[0]),
                                parent_name+smush(edge_pair[1])+smush(sg_edge_pair[1]),constraint=False)
        else: # node does not have children
            use_case.add_node(parent_name+smush(edge_pair[1]),
                              label=with_spaces(edge_pair[1]))
        use_case.add_edge(parent_name+smush(edge_pair[0]),
                          parent_name+smush(edge_pair[1]))
    use_case.write("linked_layers.dot")
    use_case.draw("linked_layers.svg", format="svg", prog="dot")


if __name__ == "__main__":
    create_allinone()

    create_linked_layers()
