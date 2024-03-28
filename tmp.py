# Your existing code up to the game loop remains the same

announcement_time = 0  # Variable to track announcement time
announcement_duration = 3000  # Duration of the announcement in milliseconds (3 seconds)

while running:
    clock.tick(FPS)
    win.fill((50, 133, 168))
        
    m.draw()

    for obs in obstacles:
        obs.draw()
        if seeker.can_pick_obstacle():
            if seeker.obstacle is None:
                seeker.set_obstacle(obs)
                seeker.reset_map_data()
                seeker.remove_obstacle()
            key = pygame.key.get_pressed()
            if key[pygame.K_g]:
                seeker.set_obstacle(obs)
            elif key[pygame.K_h]:
                seeker.remove_obstacle()
        else:
            seeker.remove_obstacle()
        
    if seeker.obstacle is None:
        seeker.move()
        seeker.character_vision(3)
    else:
        seeker.move_obstacle()
        seeker.character_vision(3)

    pygame.draw.rect(win, (255, 0, 0), (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))

    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
    win.blit(SCORE_TEXT, [0,0])   
    
    pygame.draw.rect(win, (0, 0, 255), (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))
 
    # Check if it's time to announce hider's location
    if pygame.time.get_ticks() - announcement_time >= announcement_duration:
        hider_location = []
        for i in range(0, num_hiders):
            tmp = hider.annouce_location(2)
            hider_location.append(tmp)
            ANNOUNCE_LOCATION_TEXT = SCORE_FONT.render(f'Hider {i + 1} is at {tmp}', True, (0, 0, 0))
            ANNOUNCE_LOCATION_REC = ANNOUNCE_LOCATION_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 * i))
            win.blit(ANNOUNCE_LOCATION_TEXT, ANNOUNCE_LOCATION_REC.topleft)
            pygame.display.update()
            pygame.time.wait(1000)
        seeker.move_count = 0
        seeker.get_hider_postion(hider_location)
        announcement_time = pygame.time.get_ticks()  # Update announcement time

    # Update the display
    pygame.display.update()
    
    # Rest of your code remains the same

#len(self.map_data[0])
pygame.quit()
