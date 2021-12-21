import arcade
import math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

LARGE_ASTEROIDS_SPIN = 1
LARGE_ASTEROIDS_SPEED = 1.5
LARGE_ASTEROIDS_RADIUS = 15

MEDUM_ASTEROIDS_SPIN = -2
MEDUM_ASTEROIDS_RADIUS = 5

class Point:
    def __init__(self):
        self.x= 0.00
        self.y=0.00
        
class Velocity:
    def __init__(self):
        self.dx= 0.00
        self.dy=0.00
        
class Flying_object:
    def __init__(self):
        self.center=Point()
        self.center.y=random.randint(1,150)
        self.center.x=random.randint(1,150)
        self.velocity=Velocity()
        self.screen_width = SCREEN_WIDTH
        self.screen_heigth = SCREEN_HEIGHT
        self.radius=0
        self.alive = True
        self.hits=0
        self.angle= 0.00

    def draw(self):
        texture = arcade.load_texture(self.image)
        width = texture.width
        height = texture.height
        alpha = 255 # For transparency, 1 means not transparent


        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle, alpha)
        
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
        #rotation
        self.angle += self.frame_rotate
        
        self.is_on_screen()
        
    def hit(self):
        """
        Every object will used this method but the hit method will depend of the object type
        """
        pass

    def is_on_screen(self):
        
        if (self.center.x > self.screen_width):
            self.center.x = 0
        if (self.center.x < 0):
            self.center.x = SCREEN_WIDTH
        
        if (self.center.y > self.screen_heigth):
            self.center.y = 0
        if (self.center.y < 0):
            self.center.y = SCREEN_HEIGHT
            
         

class Ship (Flying_object):
    def __init__(self):
        super().__init__()
        self.sound = arcade.load_sound("sound/explosion.mp3")
        self.live=3
        self.center.x= SCREEN_WIDTH / 2
        self.center.y= SCREEN_HEIGHT / 2
        self.velocity=Velocity()
        self.frame_rotate=0
        self.alive=True
        self.ShipThrust_Amount= SHIP_THRUST_AMOUNT
        
        self.angle=SHIP_TURN_AMOUNT
        self.radius=SHIP_RADIUS
        self.image="images/Ship.png"
    

    def turn_left(self):
        self.angle += SHIP_TURN_AMOUNT
        
    def turn_right(self):
        self.angle -= SHIP_TURN_AMOUNT
        
    def move_forward(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) *self.ShipThrust_Amount
        self.velocity.dy += math.cos(math.radians(self.angle)) *self.ShipThrust_Amount
        
    def move_backward(self):
        self.velocity.dx += math.sin(math.radians(self.angle)) *self.ShipThrust_Amount
        self.velocity.dy -= math.cos(math.radians(self.angle)) *self.ShipThrust_Amount

    def hit(self):
        if self.live <= 0:
            self.alive= False
            self.image= "images/explosion.png"
            self.ShipThrust_Amount=0
            self.velocity.dx=0
            self.velocity.dy=0
            arcade.play_sound(self.sound)
            
        else:
            self.live-= 1
            
class Bullets(Ship):
    def __init__(self, ship):
        super().__init__()
        self.center = Point()
        self.center.x = ship.center.x
        self.center.y = ship.center.y
        self.radius=BULLET_RADIUS
        self.frame_rotate=0
        self.angle=ship.angle
        self.speed=BULLET_SPEED
        self.B_life= BULLET_LIFE 
        self.image="images/Bullet.png"

    
    def fire(self):
        self.velocity.dx-=math.sin(math.radians(self.angle)) * self.speed 
        self.velocity.dy+=math.cos(math.radians(self.angle)) * self.speed
        
    def advance(self):
        
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy 
        
        #The bullets just live per 60 frames
        self.B_life -=1
        if self.B_life <= 0:
            self.alive=False
    
    # I added an updated draw method here. When the bullet is drawn you want to add 90 to the angle so it looks
    # like its coming from the front of the ship.
    def draw(self):
        texture = arcade.load_texture(self.image)
        width = texture.width
        height = texture.height
        alpha = 255 # For transparency, 1 means not transparent


        arcade.draw_texture_rectangle(self.center.x, self.center.y, width, height, texture, self.angle + 90, alpha) # I changed it to self.angle + 90
        


    def hit(self):
        #the bullet die when it hits asteroids
        pass

        
       

class Large_Asteroids(Flying_object):
    def __init__(self):
        super().__init__()
        self.velocity.dx= random.uniform(1,LARGE_ASTEROIDS_SPEED)
        self.velocity.dy= random.uniform(1,LARGE_ASTEROIDS_SPEED)
        self.frame_rotate=LARGE_ASTEROIDS_SPIN
        self.radius=LARGE_ASTEROIDS_RADIUS
        self.image="images/Big_Aster.png"


    def hit(self):
        self.alive = False

        return [Medium_Asteroids(self,0,1.5),Medium_Asteroids(self,0,-1.5) ]

       
        

class Medium_Asteroids(Large_Asteroids):
    def __init__(self,Large_Asteroids, dx, dy):
        super().__init__()
        self.center= Point()
        self.center.x=Large_Asteroids.center.x
        self.center.y=Large_Asteroids.center.y
        self.velocity.dx= Large_Asteroids.velocity.dx + dx
        self.velocity.dy= Large_Asteroids.velocity.dy + dy
        self.frame_rotate=MEDUM_ASTEROIDS_SPIN
        self.radius=MEDUM_ASTEROIDS_RADIUS
        self.image="images/Med_Aster.png"

        
    def hit(self):
        self.alive=False
        return [Small_Asteroids(self, 1.5, 1.5)]
        


class Small_Asteroids(Flying_object):
    def __init__(self, Medium_Asteroids, dx, dy):
        super().__init__()
        self.center= Point()
        self.center.x=Medium_Asteroids.center.x
        self.center.y=Medium_Asteroids.center.y
        self.velocity.dx= Medium_Asteroids.velocity.dx + dx
        self.velocity.dy= Medium_Asteroids.velocity.dy + dy
        self.frame_rotate=5
        self.radius=2
        self.image="images/Small_Aster.png"
    
        
    def hit(self):
        self.alive=False
        return []
    
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLUEBONNET)
        self.score = 0

        self.held_keys = set()
        self.laser_sound=arcade.load_sound( "sound/laser.mp3")

        # TODO: declare anything here you need the game class to track
        self.ship= Ship()
        self.asteroids=[Large_Asteroids(),Large_Asteroids(),Large_Asteroids(),Large_Asteroids(),Large_Asteroids()]
        self.bullets=[]
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        
        self.ship.draw()
        # draw score
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 710 , 10, arcade.csscolor.ORANGE, 18)
        
        # draw Lives
        lives_text = f"Lives: {self.ship.live}"
        arcade.draw_text(lives_text, 0 , 570, arcade.csscolor.RED, 18)
        
        #draw game_over
        if self.ship.alive==False:
            arcade.draw_text("GAME OVER",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.CANDY_APPLE_RED,
                         60,
                         width=700,
                         align="center",
                         anchor_x="center",
                         anchor_y="center")
            main()
                
        #draw win message
        if len(self.asteroids)<=0:
            if self.ship.alive:
                arcade.draw_text("YOUR ARE THE BOSS!",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.CANDY_APPLE_RED,
                             50,
                             width=800,
                             align="center",
                             anchor_x="center",
                             anchor_y="center")
            
                arcade.draw_text("YOU WON! ",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3,
                             arcade.color.CANDY_APPLE_RED,
                             50,
                             width=800,
                             align="center",
                             anchor_x="center",
                             anchor_y="center")
            
        
        # TODO: draw each object
        for bullet in self.bullets:
            if bullet.alive == True:
                bullet.draw()
                
        for asteroid in self.asteroids:
            asteroid.draw()
            
            

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        self.ship.advance()

        for bullet in self.bullets:
            bullet.advance()

        for asteroid in self.asteroids:
            asteroid.advance()
        
        self.check_collisions()

        # TODO: Check for collisions
    def check_collisions(self):
        """
        Checks for collisons between objects
        """
        # Check if bullets hit rocks
        for asteroid in self.asteroids:

            for bullet in self.bullets:
                
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius
                    if (abs(bullet.center.x - asteroid.center.x) < too_close and abs(bullet.center.y - asteroid.center.y) < too_close):
                        self.score += 1
                        bullet.alive = False
                        self.asteroids += asteroid.hit()

        for asteroid in self.asteroids:
            if asteroid.alive and self.ship.alive:
                too_close = asteroid.radius + self.ship.radius
                if (abs(asteroid.center.x - self.ship.center.x) < too_close and
                    abs(asteroid.center.y - self.ship.center.y) < too_close):
                    self.ship.live -= 1
                    self.ship.hit()
                    # Kill the asteroid
                    asteroid.alive = False

        self.cleanup_asteroids()      

    def cleanup_asteroids(self):
        
        for bullet in self.bullets:
            if bullet.alive==False:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if asteroid.alive==False:
                self.asteroids.remove(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn_left()
            pass

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn_right()
            pass

        if arcade.key.UP in self.held_keys:
            self.ship.move_forward()
            pass

        if arcade.key.DOWN in self.held_keys:
            self.ship.move_backward()
            pass

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        if arcade.key.SPACE in self.held_keys:
            arcade.play_sound(self.laser_sound)
            pass
        

    def on_key_press(self, key: int, modifiers: int):
        """
         firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if arcade.key.SPACE in self.held_keys:
                # TODO: Fire the bullet here!
                
                bullet=Bullets(self.ship)
                bullet.fire()

                self.bullets.append(bullet)
                pass

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

def main():
# Creates the game and starts it going
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
   
            
main()
        

    

