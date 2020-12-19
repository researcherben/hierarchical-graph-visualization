#!/usr/bin/env python3

# need "pip install pygraphviz"
# which requires a local installation of graphviz
from pygraphviz import AGraph
# https://pygraphviz.github.io/documentation/latest/reference/agraph.html
import random
from typing import Tuple

# import the data structures from a separate file
from browse_internet import list_of_dicts, cross_phase_transitions

def smush(tup: Tuple[str, str, str]) -> str:
    """
    since I'm using tuples and need to get strings, merge the tuple items with underscores
    """
    return '_'.join(tup).replace(" ","_").replace(':','').replace('-','').replace('.','').replace(',','').replace('(','').replace(')','').replace('__','_').replace("'","")

def with_spaces(tup: Tuple[str, str, str]) -> str:
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

def item_is_key_in_list_of_dicts(item_to_test: Tuple[str, str, str], list_of_dicts: list) -> bool:
    """
    is a tuple present as a key in the list of dicts?
    """
    for item_dict in list_of_dicts:
        if item_to_test in item_dict.keys():
            return True
    return False

def recurse_generate_svg(list_of_subgraphs: list,
                         output_filename: str,
                         list_of_dicts: list,
                         recursive_depth: int,
                         parent: str) -> None:
    """
    recursively create hyperlinked SVGs using GraphViz
    input data structure is a list of dicts
    """
    #print('list of subgraphs:', list_of_subgraphs)
    #print('output filename = ', output_filename)
    fnamel = "auto_"+str(recursive_depth)+"_"
    fnamel1 = "auto_"+str(recursive_depth+1)+"_"
    use_case = AGraph(directed=True, comment=output_filename)#, compound=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")
    for item in list_of_subgraphs:
        #item_without_spaces = smush(item)
        for this_dict in list_of_dicts:
            if list(this_dict.keys())[0] == item:
                #unique_subgraph_name = item_without_spaces#+"_"+str(random.randint(1000,9999))
                if (item_is_key_in_list_of_dicts(item, list_of_dicts)):
                    sg = use_case.subgraph(name="cluster_"+smush(item),
                                           label=with_spaces(item),
                                           href=fnamel1+smush(item)+".svg")
                else:
                    sg = use_case.subgraph(name="cluster_"+smush(item),
                                           label=with_spaces(item))

                #print(item)
                #print(list(this_dict.keys())[0])
                subitem_list = list(this_dict.values())[0]
                for index,subitem in enumerate(subitem_list[1:]):
                    #print('   ',subitem)
                    if (item_is_key_in_list_of_dicts(subitem_list[index], list_of_dicts)):
                        sg.add_node(smush(item)+smush(subitem_list[index]),
                                                               label=with_spaces(subitem_list[index]),
                                                               href=fnamel1+smush(item)+".svg",
                                                               color="blue",
                                                               shape="rectangle")
                    else: # no children to link to
                        sg.add_node(smush(item)+smush(subitem_list[index]),
                                                               label=with_spaces(subitem_list[index]),
                                                               shape="rectangle")
                    if (item_is_key_in_list_of_dicts(subitem, list_of_dicts)):
                        sg.add_node(smush(item)+smush(subitem),
                                                               label=with_spaces(subitem),
                                                               href=fnamel1+smush(item)+".svg",
                                                               color="blue",
                                                               shape="rectangle")
                    else:
                        sg.add_node(smush(item)+smush(subitem),
                                                               label=with_spaces(subitem),
                                                               shape="rectangle")

                    sg.add_edge(smush(item)+smush(subitem_list[index]),
                                smush(item)+smush(subitem))

    for cpt_dict in cross_phase_transitions:
        #print('cpt_dict["from subgraph"]',cpt_dict["from subgraph"])
        #print(list_of_subgraphs)
        #print('cpt_dict["to subgraph"]',cpt_dict["to subgraph"])
        if cpt_dict["from subgraph"] in list_of_subgraphs and cpt_dict["to subgraph"] in list_of_subgraphs:
            if (not cpt_dict["lhead"]) and (not cpt_dict["ltail"]):
                use_case.add_edge(smush(cpt_dict["from subgraph"])+smush(cpt_dict["from node"]),
                                  smush(cpt_dict["to subgraph"])+smush(cpt_dict["to node"]))
            if cpt_dict["lhead"] and (not cpt_dict["ltail"]):
                use_case.add_edge(smush(cpt_dict["from subgraph"])+smush(cpt_dict["from node"]),
                                  smush(cpt_dict["to subgraph"])+smush(cpt_dict["to node"]),
                                  lhead="cluster_"+smush(cpt_dict["to subgraph"]))
            elif (not cpt_dict["lhead"]) and cpt_dict["ltail"]:
                use_case.add_edge(smush(cpt_dict["from subgraph"])+smush(cpt_dict["from node"]),
                                  smush(cpt_dict["to subgraph"])+smush(cpt_dict["to node"]),
                                  ltail="cluster_"+smush(cpt_dict["from subgraph"]))
            else:
                use_case.add_edge(smush(cpt_dict["from subgraph"])+smush(cpt_dict["from node"]),
                                  smush(cpt_dict["to subgraph"])+smush(cpt_dict["to node"]),
                                  lhead="cluster_"+smush(cpt_dict["to subgraph"]),
                                  ltail="cluster_"+smush(cpt_dict["from subgraph"]))

    if recursive_depth>0:
        use_case.add_node("zoom out", href=parent+".svg", color="red", shape="triangle")
    #use_case.write()
    use_case.draw(fnamel+output_filename+".svg", format="svg", prog="dot")
    #print("drew SVG for ", output_filename)

    for item in list_of_subgraphs:
        for index, this_dict in enumerate(list_of_dicts):
            if item in this_dict.keys():
                recurse_generate_svg(list_of_dicts[index][item], smush(item), list_of_dicts, recursive_depth+1,
                fnamel+output_filename)
    return

def generate_single_svg(list_of_dicts: list,
                        list_of_toplevel_steps: list,
                        file_name: str) -> None:
    """
    make a single graph with a bunch of subgraphs
    """
    use_case = AGraph(directed=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")
    for item_tup in list_of_toplevel_steps:
        #print(item_tup)
        use_case = add_subgraphs(list_of_dicts, use_case, item_tup)

    #use_case.write()
    for cpt_dict in cross_phase_transitions:
        use_case.add_edge(smush(cpt_dict["from node"]),
                          smush(cpt_dict["to node"]),
                          lhead="cluster_"+smush(cpt_dict["to subgraph"]),
                          ltail="cluster_"+smush(cpt_dict["from subgraph"]))

    #use_case.write()
    use_case.draw(file_name+".svg", format="svg", prog="dot")

# TODO: how to tell mypy that the type is "AGraph" for input and output?
def add_subgraphs(list_of_dicts: list, use_case, item_tup: Tuple(str, str, str)):
    """
    recursively add subgraphs
    """
    for item_dict in list_of_dicts:
        if item_tup in item_dict.keys():
            #print('item_tup', item_tup)
            #print("has children:")
            #print(item_dict[item_tup])
            sg = use_case.subgraph(name="cluster_"+smush(item_tup),
                                   label=with_spaces(item_tup))
            # TODO: invisible nodes take up space, making the aesthetics ugly
            sg.add_node(smush(item_tup), style="invis") # where to connect edges

            for index, child_node in enumerate(item_dict[item_tup][1:]):
                use_case.add_node(smush(item_dict[item_tup][index]),
                                  label=with_spaces(item_dict[item_tup][index]))
                use_case.add_node(smush(child_node),
                                  label=with_spaces(child_node))
               # TODO: A bunch of warnings about missing clusters are currently displayed. Use something like
               # for this_sg in use_case.subgraphs():
               #     this_sg.to_string()
               # to determine whether cluster exists for ltail, lhead
                use_case.add_edge(smush(item_dict[item_tup][index]),
                                  smush(child_node),
                                  ltail="cluster_"+smush(item_dict[item_tup][index]),
                                  lhead="cluster_"+smush(child_node))

            #print('item_dict:', item_dict)
            for sg_tup in item_dict[item_tup]:
                #print('sg_tup:', sg_tup)
                add_subgraphs(list_of_dicts, sg, sg_tup)
        else: # no children, so create a node instead of a subgraph
            use_case.add_node(smush(item_tup))


    return use_case


# import generate_graphviz as gg
if __name__ == "__main__":
    recurse_generate_svg(list_of_dicts[0]["user story"], "how_to_use_the_internet", list_of_dicts, recursive_depth=0, parent=None)

    # the following generates warnings
    generate_single_svg(list_of_dicts,
                                   list_of_toplevel_steps=list_of_dicts[0]["user story"],
                                   file_name = "all_in_one")
