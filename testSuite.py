#Here's a general test suite for the project. 
#It's not complete, because there are a lot of things to test for our project for writing tests methods for.
#We decided to run tests manually instead of writing a test suite code for the project.

# tests/test_player.py
def test_player_initial_position():
    # Test that the player starts at the correct position
    pass

def test_player_jump():
    # Test that the player can jump properly
    pass

def test_player_collision():
    # Test that player collisions with other objects are handled correctly
    pass

# tests/test_level.py
def test_level_loading():
    # Test that levels are loaded correctly from files
    pass

def test_level_enemies():
    # Test that enemies are placed and behave correctly in a level
    pass

# tests/test_enemies.py
def test_enemy_movement():
    # Test the movement of an enemy
    pass

def test_enemy_collision():
    # Test enemy collision with the player and other objects
    pass


# tests/test_player.py

def test_player_initial_position():
    player = Player()
    assert player.position == (0, 0), "Player should start at (0, 0)"

def test_player_jump():
    player = Player()
    initial_y = player.position[1]
    player.jump()
    assert player.position[1] > initial_y, "Player should jump upward"
