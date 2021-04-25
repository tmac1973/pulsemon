Pulsemon allow you to pick a pulseaudio output (sink) and input (source) as
the preferred device. It will then monitor for changes to usb bus. If your preferred
pulseaudio sound device is removed and then re-added later it will auto select that
device as "active". 

I wrote this because I have 3 sound devices (webcam, mic, usb sound card) all plugged
into my KVM monitor so that they get switched to the selected computer. The
problem is when I switch back to my linux box the wrong sound devices would always
get selected as "active". This tool solves the problem. 

This utility saves its settings in ~/.pulsmonrc so it should reliably remember
state between runs. Set it to start at login and you should be good to go (I think.)

The way pulsemon works is it looks for changes to the devices on the usb bus using
the pyudev module. If it sees a change then it enumerates the pulseaudio devices 
and compares them against what you have set as the "preferred" device. If it finds
a match then it goes to work.

I could probably change it to monitor pulseaudio directly instead of the usb bus
though pyudev but that's for another day. Hope this helps someone out. 



