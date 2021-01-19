#!/usr/bin/env python3

"""
This data structure is intended to support a hypernode graph.


assumptions:
 * each tuple is a "node" in the graph and represents a unique event or action or state
 * pairs of tuples form an edge
 * a list of pairs-of-tuples form a graph
 * each graph is named as a dictionary where key=name, value=list of edge pairs
 * the overarching data structure is a list of dictionaries.
"""


list_of_dicts = [
{("sst"): [
  (("birth"),("life - time begins")),
  (("life - time begins"),("death"))
]},
{("birth"): [
  (("SST parses arguments"),
   ("SST Python interpreter parses confguration file")),
  (("SST Python interpreter parses confguration file"),
   ("Create graph of components from Python configuration file on MPI rank 0")),
  (("Create graph of components from Python configuration file on MPI rank 0"),
   ("Partition graph")),
  (("Partition graph"),
   ("assign components to MPI ranks")),
  (("assign components to MPI ranks"),
   ("Instantiate components")),
  (("Instantiate components"),
   ("Connect components via links")),
  (("Connect components via links"),
   ("initialize components"))
]},
{("life - time begins"): [
  (("Send events"),
   ("Manage clock and event handlers")),
  (("Manage clock and event handlers"),
   ("Continue until a set time, or all components agree to finish")),
  (("Continue until a set time, or all components agree to finish"),
   ("Send events"))
]},
{("death"): [
  (("complete - 'post-time'"),
   ("finalize components - end of simulation"))
]},
{("initialize components"):[
   (("Initialize components using their init() functions"),
    ("Setup components using their setup() functions")),
   (("Setup components using their setup() functions"),
    ("Components send 'init' events to each other over links")),
   (("Components send 'init' events to each other over links"),
    ("Discover neighbors")),
   (("Discover neighbors"),
    ("negotiate parameters")),
   (("negotiate parameters"),
    ("initialize data structures")),
   (("initialize data structures"),
    ("communication until no more “init” events are sent")),
   (("communication until no more “init” events are sent"),
    ("Components send 'init' events to each other over links"),)
]},
{("Setup components using their setup() functions"):[
   (("Each component does its final setup"),
    ("Each component schedules initial events"))
]},
{("complete - 'post-time'"):[
   (("Components can send 'init' events to each other over links​"),
    ("Multiple rounds, until no more 'init' events are sent"))
]},
{("finalize components - end of simulation"):[
   (("Finalize components using their finish() functions"),
    ("write statistics")),
   (("write statistics"),
    ("free memory")),
   (("free memory"),
    ("delete components"))
]}
]
