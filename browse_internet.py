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
# TODO: the following intersects with "user types REISUB"
# {(("user","types", "URL of website")):[
#   ("keyboard key","press","mechanical switch"),
#   ("mechanical switch","shorts","electrical circuit")
# ]},
{("web browser","shows","webpage"):[
  ("web browser","separate path from domain name from protocol"),
  ("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL"),
  ("web browser","initiates a TCP connection with the server"),
  ("web browser","sends an HTTP request to the server"),
  ("server","handles the request"),
  ("server","sends back an HTTP response"),
  ("web browser","renders the HTML content"),
  ("web browser","sends additional requests for objects embedded in the html file - CSS files, images, javascript"),
  ("server","sends back additional content"),
  ("web browser","Process CSS markup and build the CSSOM tree"),
  ("web browser","Combine the DOM and CSSOM into a render tree"),
  ("web browser","Run the layout on the render tree to compute the geometry of each node - layout/reflow"),
  ("web browser","Paint the individual nodes to the screen")
]},
{("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL"):[
  ("web browser","checks the","browser's in-memory cache"),
  ("web browser","checks the","operating system cache"),
]},
{("web browser","checks the","operating system cache"):[
  ("web browser", "make a system call to", "operating system"),
  ("operating system","checks the","local cache in OS"),
  ("operating system","check the","router cache")
]},
{("operating system","check the router cache"):[
  ("operating system","sends request to","router"),
  ("router","checks","local cache on router"),
  ("router","checks the","ISP cache")
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
]}
]


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
