# first-projects
I am using the Python Arcade Library and POO for  implement a version of the classic arcade game Asteroids.

REQUIREMENTS.

You will need to install the Python Arcade Library if you want to test this project. Here's the official website: https://api.arcade.academy/en/latest/

and here's is the dowload instruction: https://api.arcade.academy/en/latest/install/windows.html

Enjoy it!



DESCRIPTION OF I WAS LOKING FOR. 

Asteroid Game Project

I am using the Python Arcade Library and POO for  implement a version of the classic arcade game Asteroids. Below are the description about the different emotions and behavior of the elements and object in the game.

Ship

The ship obeys the laws of motion. When in motion, the ship will tend to stay in motion.

The ship can be different than the direction it is traveling.

The right and left arrows rotate the ship 3 degrees to either direction.

The up arrow will increase the velocity in the direction the ship is pointed by 0.25 pixels/frame.

For collision detection, I  assumed the ship is a circle of radius 30.

Bullets

Pressing space bar will shoot a bullet.

Bullets are should start with the same velocity of the ship (speed and direction) plus 10 pixels per frame in the direction the ship is pointed. This means if the ship is traveling straight up, but pointed directly to the right, the bullet will have a velocity that is at an angle up and to the right (starting with an upward velocity from the ship, and adding to it a velocity to the right because of the direction the ship is pointed).

Bullets only live for 60 frames, after which they should "die" and be removed from the game.

For collision detection, I assumed that bullets have a radius of 30

Asteroids

There are 3 types of asteroids in the game:

Large Asteroids

Moves at 1.5 pixels per frame, at a random initial direction.

Rotates at 1 degree per frame.

For collision detection, I assumed as a circle with radius 15.

If a large asteroid gets hit, it breaks apart and becomes two medium asteroids and one small one.

The first medium asteroid has the same velocity as the original large one plus 2 pixel/frame in the up direction.

The second medium asteroid has the same velocity as the original large one plus 2 pixel/frame in the down direction.

The small asteroid has the original velocity plus 5 pixels/frame to the right.

Medium Asteroid

Rotates at -2 degrees per frame.

For collision detection, I assumed as a circle with radius 5.

If hit, it breaks apart and becomes two small asteroids.

The small asteroid has the same velocity as the original medium one plus 1.5 pixels/frame up and 1.5 pixels/frame to the right.

The second, 1.5 pixels/frame down and 1.5 to the left.

Small Asteroid

Rotates at 5 degrees per frame.

For collision detection,I assumed as a circle with radius 2.

If a small asteroid is hit, it is destroyed and removed from the game.

THINGS TO DO: 

Develop a Start and Restart Menu. 
