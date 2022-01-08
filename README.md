# Auto-Whiteboard
A whiteboard that can draw a user's image.

ImageAnalysis.py is a program that converts an image (sent in through the command line) to an outline, and then finds a single path through that outline using the travelling salesman problem. This program can be used soley for this function, but it also determines the movements for the servos and attempts to communicate them to an arduino. If there is an arduino connected to the host computer in the appropriate usb slot, it will recieve the movements and communicate them to the servos on the whiteboard. This will result in the image being drawn by the servos onto the whiteboard.

Whiteboard.ino does a few things. It receives the instructions sent by the program and sends them to the servos, but can also recieve instructions from a joystick, allowing for manual control of the device. 
