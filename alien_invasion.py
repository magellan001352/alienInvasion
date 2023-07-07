import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    #Overall Class to manage game assests and behavior
    
    def __init__(self):
    #Initialize the game and create game resources
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
#EXTRA code so screen doesnt take up whole fullscreen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game statistics
        #create a scoreboard 
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
    
        #Set the Background Color
        self.bg_color = (230,230,230)

        #Start Alien Invasion in an inactive state
        self.game_active = False

        #Make the Play Button
        self.play_button = Button(self, "Play")
    
    def _create_fleet(self):
         #create the fleet of aliens
         #make an alien and keep addings aliens until theres no room left
         #space between aliens is one alien width
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size
         
         current_x, current_y = alien_width, alien_height
         while current_y < (self.settings.screen_height - 3 * alien_height):
              while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

              #finished a row: reset x value and increment y value
              current_x = alien_width
              current_y += 2 * alien_height
         

    def _create_alien(self, x_position, y_position):
              #Create an alien and place it in the row
              new_alien = Alien(self)
              new_alien.x = x_position
              new_alien.rect.x = x_position
              new_alien.rect.y = y_position
              self.aliens.add(new_alien)
            #  current_x += 2 * alien_width

    def _check_fleet_edges(self):
         #respond appropriately if any aliens have reached an edge
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
    
    def _change_fleet_direction(self):
         #drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        #Start the main loop for the game
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)
    
    def _update_bullets(self):
         #update position of bullets and get rid of old bullets
         #update bullet positions 
         self.bullets.update()
         
         #get rid of bullets that have dissapeared
         for bullet in self.bullets.copy():
              if bullet.rect.bottom <= 0:
                  self.bullets.remove(bullet)
         
         self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
         #respond to bullet-alien collisions
         #remove any bullets and aliens that have collided
        
         collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

         if collisions:
              for aliens in collisions.values():
                   self.stats.score += self.settings.alien_points * len(aliens)
              self.sb.prep_score()
              self.sb.check_high_score()
         
         if not self.aliens:
              #destroy existing bullets and create new fleets
              self.bullets.empty()
              self._create_fleet()
              self.settings.increase_speed()

              #increase level
              self.stats.level += 1
              self.sb.prep_level()
    
    def _ship_hit(self):
        #respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            #decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _update_aliens(self):
         #update the position of all aliens in the fleet
         #check if the fleet is at an edge then update positions
         self._check_fleet_edges()
         self.aliens.update()

         #look for alien-ship collisions
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._ship_hit()

        #look for aliens hitting the bottom of the screen
         self._check_aliens_bottom()
    
    def _update_screen(self): 
            #update images on the screen, and flip to the new screen
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                 bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)

            #draw the scoreboard information
            self.sb.show_score()

            #Draw the play button if the game is inactive
            if not self.game_active:
                 self.play_button.draw_button()

            #Make the most recently drawn screen visible
            pygame.display.flip()
            
    def _check_aliens_bottom(self):
         #check if any aliens have reached the bottom of the screen
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= self.settings.screen_height:
                   #treat this the same as if the ship got hit
                   self._ship_hit()
                   break
    
    def _check_events(self): 
        #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)
                     
    def _check_play_button(self, mouse_pos):
         #start new game when the player clicks play
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.game_active:
        #if self.play_button.rect.collidepoint(mouse_pos):
             
            #reset game statistics
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True

            #reset game settings
            self.settings.initialize_dynamic_settings()    

            #get rid of remaining bullets
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor 
            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self, event):
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                 sys.exit()
            elif event.key == pygame.K_SPACE:
                 self._fire_bullet()

    def _check_keyup_events(self,event):
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
    

    
    def _fire_bullet(self):
         #create a new bullet and add it to the bullets group
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    

if __name__ == '__main__':
    #make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()