#!/usr/bin/env python3

# need "pip install pygraphviz"
# which requires a local installation of graphviz
from pygraphviz import AGraph
# https://pygraphviz.github.io/documentation/latest/reference/agraph.html
import random
from typing import Tuple

# import the data structures from a separate file
from browse_internet import list_of_task_dicts#, cross_phase_transitions

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



def recurse_generate_svg(list_of_subtasks: list,
                         output_filename: str,
                         list_of_task_dicts: list,
                         recursive_depth: int,
                         parent: str) -> None:
    """
    recursively create hyperlinked SVGs using GraphViz
    input data structure is a list of dicts
    """

    # need the filename prefix for both this file and the child files
    fnamel = "auto_"+str(recursive_depth)+"_"
    fnamel1 = "auto_"+str(recursive_depth+1)+"_"

    # initialize a new graph for this layer
    use_case = AGraph(directed=True, comment=output_filename)#, compound=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")
    for task in list_of_subtasks:
        #print(task)
        for this_dict in list_of_task_dicts:
            if list(this_dict.keys())[0] == task:

                #unique_subgraph_name = task_without_spaces#+"_"+str(random.randint(1000,9999))
                if (task_has_children_in_list_of_task_dicts(task, list_of_task_dicts)):
                    sg = use_case.subgraph(name="cluster_"+smush(task),
                                           label=with_spaces(task),
                                           href=fnamel1+smush(task)+".svg")
                else: # no href to SVG because there are no child nodes
                    sg = use_case.subgraph(name="cluster_"+smush(task),
                                           label=with_spaces(task))

                sg.add_node(smush(task), style="invis")


                #print(task)
                #print(list(this_dict.keys())[0])
                subitem_list = list(this_dict.values())[0]
#                print(subitem_list)

                if len(subitem_list)<2: # no edges to connect
                    if (task_has_children_in_list_of_task_dicts(subitem_list[0], list_of_task_dicts)):
                        sg.add_node(smush(task)+smush(subitem_list[0]),
                                                               label=with_spaces(subitem_list[0]),
                                                               href=fnamel1+smush(task)+".svg",
                                                               color="blue",
                                                               shape="rectangle")
                    else:
                        sg.add_node(smush(task)+smush(subitem_list[0]),
                                                               label=with_spaces(subitem_list[0]),
                                                               shape="rectangle")
                    sg.add_edge(smush(task)+smush(subitem_list[0]),smush(task),style="invis")

                else:
                    for index,subitem in enumerate(subitem_list[1:]):
                        #print('   ',subitem)
                        if (task_has_children_in_list_of_task_dicts(subitem_list[index], list_of_task_dicts)):
                            sg.add_node(smush(task)+smush(subitem_list[index]),
                                                                   label=with_spaces(subitem_list[index]),
                                                                   href=fnamel1+smush(task)+".svg",
                                                                   color="blue",
                                                                   shape="rectangle")
                        else: # no children to link to
                            sg.add_node(smush(task)+smush(subitem_list[index]),
                                                                   label=with_spaces(subitem_list[index]),
                                                                   shape="rectangle")
                        if (task_has_children_in_list_of_task_dicts(subitem, list_of_task_dicts)):
                            sg.add_node(smush(task)+smush(subitem),
                                                                   label=with_spaces(subitem),
                                                                   href=fnamel1+smush(task)+".svg",
                                                                   color="blue",
                                                                   shape="rectangle")
                        else:
                            sg.add_node(smush(task)+smush(subitem),
                                                                   label=with_spaces(subitem),
                                                                   shape="rectangle")

                        # every sequence of tasks is ordered, so link task with prior task
                        sg.add_edge(smush(task)+smush(subitem_list[index]),
                                    smush(task)+smush(subitem))
                        if index==len(subitem_list): # last item links to invisible node in order to force invisible node to bottom of subgraph
                            sg.add_edge(smush(task)+smush(subitem_list[index]),smush(task),style="invis")

    for index,task_tup in enumerate(list_of_subtasks[1:]):
        # use_case.add_node(smush(list_of_subtasks[index]),label=with_spaces(task_tup),shape="rectangle")
        # use_case.add_node(smush(task_tup),label=with_spaces(task_tup),shape="rectangle")
        use_case.add_edge(smush(list_of_subtasks[index]),
                          smush(task_tup),
                          ltail="cluster_"+smush(list_of_subtasks[index]),
                          lhead="cluster_"+smush(task_tup))

    if recursive_depth>0:
        use_case.add_node("zoom out", href=parent+".svg", color="red", shape="triangle")
    #use_case.write()
    use_case.draw(fnamel+output_filename+".svg", format="svg", prog="dot")
    #print("drew SVG for ", output_filename)

    for task_tuple in list_of_subtasks:
        for index, this_dict in enumerate(list_of_task_dicts):
            if task_tuple in this_dict.keys():
                recurse_generate_svg(list_of_task_dicts[index][task_tuple], smush(task_tuple), list_of_task_dicts, recursive_depth+1,
                fnamel+output_filename)
    return

def generate_single_svg(list_of_task_dicts: list,
                        list_of_toplevel_steps: list,
                        file_name: str) -> None:
    """
    make a single graph with a bunch of subgraphs
    in contrast to the layered SVG approach, here each node name must be unique
    """
    use_case = AGraph(directed=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")
    add_subgraph(list_of_task_dicts, use_case, list_of_toplevel_steps, parent="")
    use_case.write(file_name+".dot")
    use_case.draw(file_name+".svg", format="svg", prog="dot")
    return

# TODO: how to tell mypy that the type is "AGraph" for input and output?
def add_subgraph(list_of_task_dicts: list, use_case, list_of_task_tuples: list, parent: str):
    """
    recursively add subgraphs
    """
    for task_tup in list_of_task_tuples:
        #print(task_tup)
        if task_has_children_in_list_of_task_dicts(task_tup, list_of_task_dicts):
            #print("    has child, so create a subgraph")
            sg = use_case.subgraph(name="cluster_"+parent+smush(task_tup),
                                   label=with_spaces(task_tup))
            sg.add_node(parent+smush(task_tup), style="invis") # where to connect edges
            for task_dist in list_of_task_dicts:
                if task_tup in task_dist.keys():
                    #for task_tup in task_dist[task_tup]:
                    add_subgraph(list_of_task_dicts, sg, task_dist[task_tup], parent=parent+smush(task_tup))
        else:
            #print("    no children, so create node")
            use_case.add_node(parent+smush(task_tup), label=with_spaces(task_tup))

    for index, task_tup in enumerate(list_of_task_tuples[1:]):
        use_case.add_edge(parent+smush(list_of_task_tuples[index]),
                          parent+smush(task_tup),
                          ltail="cluster_"+parent+smush(list_of_task_tuples[index]),
                          lhead="cluster_"+parent+smush(task_tup))
    return


# import generate_graphviz as gg
if __name__ == "__main__":
    recurse_generate_svg(list_of_task_dicts[0]["user story"], "how_to_use_the_internet", list_of_task_dicts, recursive_depth=0, parent=None)

    #the following generates warnings
    generate_single_svg(list_of_task_dicts,
                        list_of_toplevel_steps=list_of_task_dicts[0]["user story"],
                        file_name = "all_in_one")

    print("done!")
