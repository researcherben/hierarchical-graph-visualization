#!/usr/bin/env python3

# need "pip install pygraphviz"
# which requires a local installation of graphviz
from pygraphviz import AGraph
# https://pygraphviz.github.io/documentation/latest/reference/agraph.html
import random
from typing import Tuple

from browse_internet import list_of_dicts, cross_phase_transitions

def smush(tup):
    return '_'.join(tup).replace(" ","_")



def item_is_key_in_list_of_dicts(item_to_test: Tuple[str, str, str], list_of_dicts: list) -> bool:
    """
    is a tuple present as a key in the list of dicts?
    """
    for item_dict in list_of_dicts:
        if item_to_test in item_dict.keys():
            return True
    return False

def generate_svg(list_of_subgraphs: list, output_filename: str, list_of_dicts: list, level: int, parent: str):
    """
    GraphViz from list of dicts
    """
    #print('list of subgraphs:', list_of_subgraphs)
    #print('output filename = ', output_filename)
    fnamepre = "AUTO_"
    fnamepost = "_"+str(level)
    fnamepostp1 = "_"+str(level+1)
    use_case = AGraph(directed=True, comment=output_filename)#, compound=True)
    use_case.clear()
    use_case.graph_attr.update(compound="true")
    for item in list_of_subgraphs:
        item_without_spaces = smush(item)
        for this_dict in list_of_dicts:
            if list(this_dict.keys())[0] == item:
                #unique_subgraph_name = item_without_spaces#+"_"+str(random.randint(1000,9999))
                if (item_is_key_in_list_of_dicts(item, list_of_dicts)):
                    sg = use_case.subgraph(name="cluster_"+item_without_spaces,
                                           label=' '.join(item),
                                           href=fnamepre+item_without_spaces+fnamepostp1+".svg")
                else:
                    sg = use_case.subgraph(name="cluster_"+item_without_spaces,
                                           label=' '.join(item))

                #print(item)
                #print(list(this_dict.keys())[0])
                subitem_list = list(this_dict.values())[0]
                for index,subitem in enumerate(subitem_list[1:]):
                    #print('   ',subitem)
                    if (item_is_key_in_list_of_dicts(subitem_list[index], list_of_dicts)):
                        sg.add_node(item_without_spaces+smush(subitem_list[index]),
                                                               label=' '.join(subitem_list[index]),
                                                               href=fnamepre+item_without_spaces+fnamepostp1+".svg",
                                                               color="blue",
                                                               shape="rectangle")
                    else: # no children to link to
                        sg.add_node(item_without_spaces+smush(subitem_list[index]),
                                                               label=' '.join(subitem_list[index]),
                                                               shape="rectangle")
                    if (item_is_key_in_list_of_dicts(subitem, list_of_dicts)):
                        sg.add_node(item_without_spaces+smush(subitem),
                                                               label=' '.join(subitem),
                                                               href=fnamepre+item_without_spaces+fnamepostp1+".svg",
                                                               color="blue",
                                                               shape="rectangle")
                    else:
                        sg.add_node(item_without_spaces+smush(subitem),
                                                               label=' '.join(subitem),
                                                               shape="rectangle")

                    sg.add_edge(item_without_spaces+smush(subitem_list[index]),
                                item_without_spaces+smush(subitem))

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

    if level>0:
        use_case.add_node("zoom out", href=parent+".svg", color="red", shape="invtriangle")
    #use_case.write()
    use_case.draw(fnamepre+output_filename+fnamepost+".svg", format="svg", prog="dot")
    #print("drew SVG for ", output_filename)

    for item in list_of_subgraphs:
        for index, this_dict in enumerate(list_of_dicts):
            if item in this_dict.keys():
                item_without_spaces = smush(item)
                generate_svg(list_of_dicts[index][item], item_without_spaces, list_of_dicts, level+1,
                fnamepre+output_filename+fnamepost)


# import generate_graphviz as gg
if __name__ == "__main__":
    generate_svg(list_of_dicts[0]["user story"], "how_to_use_the_internet", list_of_dicts, level=0, parent=None)
