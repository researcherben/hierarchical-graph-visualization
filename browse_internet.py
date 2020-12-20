#!/usr/bin/env python3

def user_types_on_keyboard():
    return [
      ("keyboard key","presses","mechanical switch"),
      ("mechanical switch","shorts","electrical circuit")
    ]

def user_moves_mouse():
    return [
      ("mouse hardware","moves across","surface"),
      ("mouse hardware light sensor","detects movement using","light"),
      ("mouse hardware","sends signal across","USB cable"),
      ("operating system","translates signal from","USB cable"),
      ("operating system","moves pointer on","computer screen")
    ]

def user_clicks_mouse():
    return [
      ("mouse hardware","depress","mechanical switch"),
      ("mouse hardware","sends signal across","USB cable"),
      ("operating system","translates signal from","USB cable"),
      ("operating system","acts on","desktop icon")
    ]

list_of_dicts = [
{"user story": [
  ("state:","computer","is off"),
  ("action:","user","turns on","computer"),
  ("state:","computer","is turning on"),
  ("action:","user","browses","the web"),
  ("state:","computer","is idle"),
  ("action:","user","turns off","the computer")
]},
{("state:","computer","is idle"):[
  ("operating system","waiting for","interrupt")
]},
{("action:","user","turns on","computer"):[
  ("while computer is off","user","pushes","power button")
]},
{("state:","computer","is turning on"):[
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
{("action:","user","browses","the web"):[
  ("user","opens","web browser"),
  ("user","types","URL of website"),
  ("web browser","shows","webpage"),
  ("user","reads","webpage"),
  ("user","clicks","on link"),
  ("user","closes","web browser"),
]},
{("user","clicks","on link"):user_clicks_mouse()},
{("user","closes","web browser"):[
  ("user","types","alt-f4")
]},
{("user","types","alt-f4"):user_types_on_keyboard()},
{("user","closes","web browser"):[
  ("user","moves pointer on desktop to browser close icon using","mouse"),
  ("user","clicks on","browser close icon"),
  ("operating sytem","closes","web browser")
]},
{("user","types","alt-f4"):user_types_on_keyboard()},
# TODO: the following intersects with "user types REISUB"
{("user","types", "URL of website"):user_types_on_keyboard()},
{("web browser","shows","webpage"):[
  ("web browser","separate path from domain name from protocol"),
  ("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL"),
  ("web browser","initiates TCP connection with","the remote server"),
  ("web browser","sends an HTTP request to","the remote server"),
  ("server","handles","the request"),
  ("server","sends back an","HTTP response"),
  ("web browser","renders the","HTML content"),
  ("web browser","sends additional requests for objects embedded in the html file - CSS files, images, javascript"),
  ("server","sends back additional content"),
  ("web browser","process CSS markup and build the CSSOM tree"),
  ("web browser","combine the DOM and CSSOM into a render tree"),
  ("web browser","run the layout on the render tree to compute the geometry of each node aka layout  aka reflow"),
  ("web browser","paint the individual nodes to the screen")
]},
{("web browser","renders the","HTML content"):[
  ("web browser","creates","DOM tree")
]},
{("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL"):[
  ("web browser","checks the","browser's in-memory cache"),
  ("web browser","checks the","operating system cache"),
]},
{("web browser","checks the","operating system cache"):[
  ("web browser", "make a system call to", "operating system"),
  ("operating system","checks the","local cache in OS"),
  ("operating system","checks the","router cache")
]},
{("operating system","checks the","router cache"):[
  ("operating system","sends request to","router"),
  ("router","checks","local cache on router"),
  ("router","checks the","ISP cache")
]},
{("operating system","sends request to","router"):[
  ("operating system","implements TCP connection to","router")#{} osilayer="4 = transport">
]},
{("operating system","implements TCP connection to","router"):[
  ("NIC","sends SYN packet to","router"),
  ("router","sends SYN-ACK packet to","NIC"),
  ("NIC","sends ACK packet to","router")
]},
{("NIC","sends SYN packet to","router"):[
  ("NIC","creates","IP dataframe"),
  ("NIC","sends IP dataframe to","router NIC")
]},
{("NIC","sends IP dataframe to","router NIC"):[
  ("NIC firmware","sends signal to","ethernet")
]},
{("NIC firmware","sends signal to","ethernet"):[
  ("NIC hardware","sends electrical signal to","wire")
]},
{("user","opens","web browser"):[
  ("user","moves pointer on desktop to browser icon using","mouse"),
  ("user","clicks on","desktop browser icon"),
  ("operating sytem","launches","web browser")
]},
{("user","moves pointer on desktop to browser icon using","mouse"):user_moves_mouse()},
{("user","clicks on","desktop browser icon"):user_clicks_mouse()},
{("action:","user","turns off","the computer"):[
  ("while computer is on","user","pushes","power button"),
  ("while computer is on","power button","short circuits","wire"),
  ("while computer is on","motherboard","does something to","CPU"),
]},
{("action:","user","turns off","the computer"):[
  ("user","selects","shutdown menu option on desktop"),
  ("operating system","terminates","desktop"),
]},
{("action:","user","turns off","the computer"):[
  ("user","types", "REISUB"),
]},
{("user","types", "REISUB"): user_types_on_keyboard()},
{("state:","computer","is off"):[
   ("motherboard","uses power from","battery")
]}
]


# https://github.com/pygraphviz/pygraphviz/issues/93
cross_phase_transitions = [
 {"from subgraph":("action:","user","turns on","computer"),"from node":("while computer is off","user","pushes","power button"),
  "to subgraph":("state:","computer","is turning on"),"to node":("while computer is off","power button","short circuits","wire"),
  "lhead":True, "ltail":True},
 {"from subgraph":("state:","computer","is turning on"),"from node":("operating system","starts","desktop"),
  "to subgraph":("state:","computer","is idle"),"to node":("operating system","waiting for","interrupt"),
  "lhead":True, "ltail":True},
 {"from subgraph":("state:","computer","is idle"),"from node":("operating system","waiting for","interrupt"),
  "to subgraph":("action:","user","browses","the web"),"to node":("user","opens","web browser"),
  "lhead":True, "ltail":True},
 {"from subgraph":("action:","user","browses","the web"),"from node":("user","closes","web browser"),
  "to subgraph":("state:","computer","is idle"),"to node":("operating system","waiting for","interrupt"),
  "lhead":True, "ltail":True},
 {"from subgraph":("action:","user","browses","the web"),"from node":("user","closes","web browser"),
  "to subgraph":("action:","user","turns off","the computer"),"to node":("while computer is on","user","pushes","power button"),
  "lhead":True, "ltail":True},
 {"from subgraph":("action:","user","turns off","the computer"),"from node":("while computer is on","user","pushes","power button"),
  "to subgraph":("state:","computer","is off"),"to node":("motherboard","uses power from","battery"),
  "lhead":True, "ltail":True},
 {"from subgraph":("state:","computer","is off"),"from node":("motherboard","uses power from","battery"),
  "to subgraph":("action:","user","turns on","computer"),"to node":("while computer is off","user","pushes","power button"),
  "lhead":True, "ltail":True}
]
