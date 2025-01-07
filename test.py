import pygame
from auxil import WHITE, BLUE, get_sysfont, RED, GREEN

def draw_score_display(screen, score, combo, max_combo=5, last_hit_type=None):
    """
    Draw a styled score display including score, current combo, and max combo.
    
    Args:
        screen: Pygame screen surface
        score: Current score
        combo: Current combo counter
        max_combo: Maximum combo achieved (optional)
        last_hit_type: String indicating last hit quality ('PERFECT', 'GOOD', etc.) (optional)
    """
    # Main score display
    score_font = get_sysfont('Arial', 48)
    score_text = f"{score:,}"  # Add commas for thousand separators
    score_surface = score_font.render(score_text, True, WHITE)
    
    # Add score label
    label_font = get_sysfont('Arial', 24)
    score_label = label_font.render("SCORE", True, BLUE)
    
    # Position score and label
    score_x = 1100  # Right side of screen
    score_y = 50
    screen.blit(score_label, (score_x + (score_surface.get_width() - score_label.get_width()) // 2, score_y))
    screen.blit(score_surface, (score_x, score_y + 30))
    
    # Combo display
    if combo > 0:
        combo_font = get_sysfont('Arial', 36)
        combo_text = f"{combo}x COMBO"
        
        # Choose combo color based on size
        if combo >= 10:
            combo_color = RED
        elif combo >= 5:
            combo_color = GREEN
        else:
            combo_color = WHITE
            
        combo_surface = combo_font.render(combo_text, True, combo_color)
        combo_x = (screen.get_width() - combo_surface.get_width()) // 2  # Center horizontally
        screen.blit(combo_surface, (combo_x, 150))
    
    # Max combo (small display in corner)
    if max_combo > 0:
        max_combo_font = get_sysfont('Arial', 20)
        max_combo_text = f"Max Combo: {max_combo}"
        max_combo_surface = max_combo_font.render(max_combo_text, True, WHITE)
        screen.blit(max_combo_surface, (1100, 120))
    
    # Hit type indicator (e.g., PERFECT, GOOD)
    if last_hit_type:
        hit_font = get_sysfont('Arial', 32)
        hit_colors = {
            'PERFECT': (255, 215, 0),  # Gold
            'GOOD': (0, 255, 0),      # Green
            'OK': (0, 191, 255),      # Deep sky blue
            'MISS': (255, 0, 0)       # Red
        }
        hit_color = hit_colors.get(last_hit_type, WHITE)
        hit_surface = hit_font.render(last_hit_type, True, hit_color)
        hit_x = (screen.get_width() - hit_surface.get_width()) // 2
        screen.blit(hit_surface, (hit_x, 200))

def cut_sprite_sheet(sheet_path, sprite_width, sprite_height):
    """
    Cut a sprite sheet into individual frames.
    
    Args:
        sheet_path (str): Path to the sprite sheet image
        sprite_width (int): Width of each individual sprite
        sprite_height (int): Height of each individual sprite
    
    Returns:
        list: List of pygame Surface objects, each containing one frame
    """
    # Load the sprite sheet
    sheet = pygame.image.load(sheet_path).convert_alpha()
    
    # Get the dimensions of the sheet
    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()
    
    # Calculate number of sprites in the sheet
    num_sprites_x = sheet_width // sprite_width
    
    # List to store all frames
    frames = []
    
    # Cut up the sheet
    for i in range(num_sprites_x):
        # Define the rectangle for the sprite
        rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
        # Create a new surface for the sprite
        frame = sheet.subsurface(rect)
        frames.append(frame)
    
    return frames