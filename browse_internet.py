#!/usr/bin/env python3

# assumptions:
# * each tuple is represents a unique event or action or state

def user_types_on_keyboard():
    """everytime the user uses the keyboard, this graph is implemented"""
    return [
      (("keyboard key","presses","mechanical switch"),
       ("mechanical switch","shorts","electrical circuit"))
    ]

def user_moves_mouse():
    return [
      (("mouse hardware","moves across","surface"),
       ("mouse hardware light sensor","detects movement using","light")),
      (("mouse hardware light sensor","detects movement using","light"),
       ("mouse hardware","sends signal across","USB cable")),
      (("mouse hardware","sends signal across","USB cable"),
       ("operating system","translates signal from","USB cable")),
      (("operating system","translates signal from","USB cable"),
       ("operating system","moves pointer on","computer screen"))
    ]

def user_clicks_mouse():
    return [
      (("mouse hardware","depress","mechanical switch"),
       ("mouse hardware","sends signal across","USB cable")),
      (("mouse hardware","sends signal across","USB cable"),
       ("operating system","translates signal from","USB cable")),
      (("operating system","translates signal from","USB cable"),
       ("operating system","acts on","desktop icon"))
    ]

list_of_task_dicts = [
{"user story": [
  (("computer","has state","off"),
   ("user","turns on","computer")),
  (("user","turns on","computer"),
   ("computer","has state","turning on")),
  (("computer","has state","turning on"),
   ("user","browses","the web")),
  (("user","browses","the web"),
   ("computer","has state","idle")),
  (("computer","has state","idle"),
   ("user","turns off","the computer")),
  (("user","turns off","the computer"),
   ("computer","has state","off"))
]},
{("computer","has state","idle"):[
  ("operating system","waiting for","interrupt")
]},
{("user","turns on","computer"):[
  ("user","pushes","power button")
]},
{("computer","has state","turning on"):[
  (("power button","short circuits","wire"),
   ("motherboard","does something to","CPU")),
  (("motherboard","does something to","CPU"),
   ("CPU","executes BIOS code at bottom of","memory map")),
  (("CPU","executes BIOS code at bottom of","memory map"),
   ("BIOS","boots","computer")),
  (("BIOS","boots","computer"),
   ("operating system","starts","desktop"))
]},
{("BIOS","boots","computer"):[
  (("BIOS","detects","RAM"),
   ("BIOS","detects","hardware")),
  (("BIOS","detects","hardware"),
   ("BIOS","loads","boot sequence"))
]},
{("BIOS","loads","boot sequence"):[
  (("BIOS","boots","devices directly into your OS-specific bootloader"),
   ("BIOS","boots","devices (any hard disk, or anything emulating a hard disk) into an MBR"))
]},
{("user","browses","the web"):[
  (("user","opens","web browser"),
   ("user","types","URL of website")),
  (("user","types","URL of website"),
   ("web browser","shows","webpage")),
  (("web browser","shows","webpage"),
   ("user","reads","webpage")),
  (("user","reads","webpage"),
   ("user","clicks","on link")),
  (("user","clicks","on link"),
   ("user","closes","web browser"))
]},
{("user","clicks","on link"):user_clicks_mouse()},
{("user","closes","web browser"):[
  ("user","types","alt-f4")
]},
{("user","types","alt-f4"):user_types_on_keyboard()},
{("user","closes","web browser"):[
  (("user","moves pointer on desktop to browser close icon using","mouse"),
   ("user","clicks on","browser close icon")),
  (("user","clicks on","browser close icon"),
  ("operating sytem","closes","web browser"))
]},
{("user","types","alt-f4"):user_types_on_keyboard()},
{("user","types", "URL of website"):user_types_on_keyboard()},
{("web browser","shows","webpage"):[
  (("web browser","separate path from domain name from protocol"),
   ("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL")),
  (("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL"),
   ("web browser","initiates TCP connection with","the remote server")),
  (("web browser","initiates TCP connection with","the remote server"),
   ("web browser","sends an HTTP request to","the remote server")),
  (("web browser","sends an HTTP request to","the remote server"),
   ("server","handles","the request")),
  (("server","handles","the request"),
   ("server","sends back an","HTTP response")),
  (("server","sends back an","HTTP response"),
   ("web browser","renders the","HTML content")),
  (("web browser","renders the","HTML content"),
   ("web browser","sends additional requests for objects embedded in the html file - CSS files, images, javascript")),
  (("web browser","sends additional requests for objects embedded in the html file - CSS files, images, javascript"),
   ("server","sends back additional content")),
  (("server","sends back additional content"),
   ("web browser","process CSS markup and build the CSSOM tree")),
  (("web browser","process CSS markup and build the CSSOM tree"),
   ("web browser","combine the DOM and CSSOM into a render tree")),
  (("web browser","combine the DOM and CSSOM into a render tree"),
   ("web browser","run the layout on the render tree to compute the geometry of each node aka layout  aka reflow")),
  (("web browser","run the layout on the render tree to compute the geometry of each node aka layout  aka reflow"),
   ("web browser","paint the individual nodes to the screen"))
]},
{("web browser","renders the","HTML content"):[
  ("web browser","creates","DOM tree")
]},
{("web browser","browser checks the cache for a DNS record to find the corresponding IP address of URL"):[
  (("web browser","checks the","browser's in-memory cache"),
  ("web browser","checks the","operating system cache"))
]},
{("web browser","checks the","operating system cache"):[
  (("web browser", "make a system call to", "operating system"),
   ("operating system","checks the","local cache in OS")),
  (("operating system","checks the","local cache in OS"),
   ("operating system","checks the","router cache"))
]},
{("operating system","checks the","router cache"):[
  (("operating system","sends request to","router"),
   ("router","checks","local cache on router")),
  (("router","checks","local cache on router"),
   ("router","checks the","ISP cache"))
]},
{("operating system","sends request to","router"):[
  ("operating system","implements TCP connection to","router")#{} osilayer="4 = transport">
]},
{("operating system","implements TCP connection to","router"):[
  (("NIC","sends SYN packet to","router"),
   ("router","sends SYN-ACK packet to","NIC")),
  (("router","sends SYN-ACK packet to","NIC"),
   ("NIC","sends ACK packet to","router"))
]},
{("NIC","sends SYN packet to","router"):[
  (("NIC","creates","IP dataframe"),
   ("NIC","sends IP dataframe to","router NIC"))
]},
{("NIC","sends IP dataframe to","router NIC"):[
  ("NIC firmware","sends signal to","ethernet")
]},
{("NIC firmware","sends signal to","ethernet"):[
  ("NIC hardware","sends electrical signal to","wire")
]},
{("user","opens","web browser"):[
  (("user","moves pointer on desktop to browser icon using","mouse"),
   ("user","clicks on","desktop browser icon")),
  (("user","clicks on","desktop browser icon"),
   ("operating sytem","launches","web browser"))
]},
{("user","moves pointer on desktop to browser icon using","mouse"):user_moves_mouse()},
{("user","clicks on","desktop browser icon"):user_clicks_mouse()},
{("user","turns off","the computer"):[
  (("user","pushes","power button"),
   ("power button","short circuits","wire")),
  (("power button","short circuits","wire"),
   ("motherboard","does something to","CPU"))
]},
{("user","turns off","the computer"):[
  (("user","selects","shutdown menu option on desktop"),
   ("operating system","terminates","desktop"))
]},
{("user","turns off","the computer"):[
  ("user","types", "REISUB"),
]},
{("user","types", "REISUB"): user_types_on_keyboard()},
{("computer","has state","off"):[
   ("motherboard","uses power from","battery")
]}
]
