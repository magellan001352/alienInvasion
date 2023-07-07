class Settings:
    #Class to store all settings for Alien Invasion
    
    def __init__(self):
        #initialize the game's static settings
        
        #SCREEN Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #SHIP Settings
        self.ship_speed = 3
        self.ship_limit = 1

        #BULLET Settings
        self.bullet_speed = 4
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 6

        #ALIEN Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #fleet direction of 1 represents right and -1 represents left
        self.fleet_direction = 1

        #How quickly the game speeds up
        self.speedup_scale = 1.2
        #how quick the alien point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 2.5
        self.bullet_speed = 3.5
        self.alien_speed = 1.0

        #fleet direction of 1 represents right and -1 represents left
        self.fleet_direction = 1

        #score settings
        self.alien_points = 50
    
    def increase_speed(self):
        #Increase speed settings and alien point value settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        #print(self.alien_points)
