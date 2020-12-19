list_of_dicts = [
{"user story": [
  ("user","turn on","computer"),
  ("user","browses","the web"),
  ("user","turn off","the computer")
]},
{("user","turn on","computer"):[
  ("while computer is off","user","pushes","power button"),
  ("while computer is off","power button","short circuits","wire"),
  ("while computer is off","motherboard","does something to","CPU"),
  ("CPU","executes BIOS code at bottom of","memory map"),
  ("BIOS","boots","computer"),
  ("operating system","starts","desktop")
]},
{("BIOS","boots","computer"):[
  ("BIOS","detects","RAM"),
  ("BIOS","detects","hardware"),
  ("BIOS","loads","boot sequence")
]},
{("BIOS","loads","boot sequence"):[
  ("BIOS","boots","devices directly into your OS-specific bootloader"),
  ("BIOS","boots","devices (any hard disk, or anything emulating a hard disk) into an MBR")
]},
{("user","browses","the web"):[
  ("user","opens","web browser"),
  ("user","types","URL of website"),
  ("web browser","shows","webpage"),
  ("user","reads","webpage"),
  ("user","clicks","on link"),
  ("user","closes","web browser"),
]},
{("user","opens","web browser"):[
  ("user","moves pointer on desktop to browser icon using","mouse"),
  ("user","clicks on","desktop broswer icon"),
  ("operating sytem","launches","web browser")
]},
{("user","moves pointer on desktop to browser icon using","mouse"):[
  ("mouse hardware","moves across","surface"),
  ("mouse hardware light sensor","detects movement using","light"),
  ("mouse hardware","sends signal across","USB cable"),
  ("operating system","translates signal from","USB cable"),
  ("operating system","moves pointer on","computer screen")
]},
{("user","turn off","the computer"):[
  ("while computer is on","user","pushes","power button"),
  ("while computer is on","power button","short circuits","wire"),
  ("while computer is on","motherboard","does something to","CPU"),
  ("motherboard","uses power from","battery")
]},
{("user","turn off","the computer"):[
  ("user","selects","shutdown menu option on desktop"),
  ("operating system","terminates","desktop"),
  ("motherboard","uses power from","battery")
]},
{("user","turn off","the computer"):[
  ("user","types", "REISUB"),
  ("motherboard","uses power from","battery")
]},
{(("user","types", "REISUB")):[
  ("keyboard key","press","mechanical switch"),
  ("mechanical switch","shorts","electrical circuit")
]}]


# https://github.com/pygraphviz/pygraphviz/issues/93
cross_phase_transitions = [
 {"from subgraph": ("user","turn on","computer"),
  "from node": ("operating system","starts","desktop"),
  "to subgraph": ("user","browses","the web"),
  "to node": ("user","opens","web browser"),
  "lhead":True, "ltail":True},
 {"from subgraph": ("user","browses","the web"),
  "from node": ("user","closes","web browser"),
  "to subgraph": ("user","turn off","the computer"),
  "to node": ("while computer is on","user","pushes","power button"),
  "lhead":True, "ltail":True}
]
