import pygame
import game_objects

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Shmup Game")

game_objects.init()

background_image = game_objects.all_images["background"]
meteor_explotion = game_objects.all_sounds["meteor_explosion"]

# Sprite Groups
all_sprites = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteors_group = pygame.sprite.Group()

spaceship = game_objects.SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT)
player_life_num = game_objects.Player_Life_Num(spaceship)
player_life_img = game_objects.Player_Life_Img()

all_sprites.add(player_life_img)
all_sprites.add(player_life_num)
all_sprites.add(spaceship)


# Number of meteors that will be drawn
for i in range(10):
    meteor = game_objects.Meteor(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(meteor)
    meteors_group.add(meteor)


def new_meteor():
    meteor = game_objects.Meteor(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(meteor)
    meteors_group.add(meteor)

music_game = game_objects.all_sounds["music_game"]
music_game.play(-1)

def main() :

    # Main loop
    running = True
    while running:
        # Keep loop running at the right speed
        clock.tick(FPS)

        # Setting timer
        pygame.time.set_timer(1, 15000)


        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spaceship.shoot(all_sprites, laser_group)


        # update
        all_sprites.update()

        # Check if a laser hit a meteor
        for hit in pygame.sprite.groupcollide(laser_group, meteors_group, True, True):
            # For each meteor that is destroyed, a new one is created and a sound is played
            meteor_explotion.play()
            new_meteor()

        # Check if a meteor hit the spaceship
        for hit in pygame.sprite.spritecollide(spaceship, meteors_group, True):
            spaceship.lives -= 1
            player_life_num.image = game_objects.all_images["player_life_num"][spaceship.lives]

            if spaceship.lives == 0:
                running = False

        # draw / render
        screen.blit(background_image, (0,0))
        all_sprites.draw(screen)

        # flip the display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()




