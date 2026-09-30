"""
Renderer: draws the game scene, UI, and game-over screen.
"""

import pygame


WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)


def draw_scene(
    surface,
    player,
    coins,
    obstacles=None,
    player_visible=True
):
    """
    Draw the complete game scene.

    player_visible is used to make the player blink
    during the invulnerability period.
    """

    surface.fill(COLOR_BG)

    # -------------------------
    # Draw coins
    # -------------------------

    for coin in coins:
        pygame.draw.circle(
            surface,
            coin.color,
            (int(coin.x), int(coin.y)),
            coin.radius
        )

    # -------------------------
    # Draw obstacles
    # -------------------------

    if obstacles is not None:
        for obstacle in obstacles:
            pygame.draw.circle(
                surface,
                obstacle.color,
                (
                    int(obstacle.x),
                    int(obstacle.y)
                ),
                obstacle.radius
            )

    # -------------------------
    # Draw player
    # -------------------------

    # During invulnerability, the GameEngine
    # alternates this between True and False.
    if player_visible:
        pygame.draw.rect(
            surface,
            COLOR_PLAYER,
            player.get_rect(),
            border_radius=4
        )


def draw_text(
    surface,
    font,
    text,
    pos,
    color=COLOR_TEXT
):
    """Draw text on the screen."""

    surface.blit(
        font.render(
            text,
            True,
            color
        ),
        pos
    )


def draw_game_over(
    surface,
    font,
    score,
    reason
):
    """
    Draw the game-over screen with the final score
    and the reason the round ended.
    """

    # -------------------------
    # Dark transparent overlay
    # -------------------------

    overlay = pygame.Surface(
        surface.get_size(),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 170)
    )

    surface.blit(
        overlay,
        (0, 0)
    )

    # -------------------------
    # Fonts
    # -------------------------

    game_over_font = pygame.font.SysFont(
        "consolas",
        42,
        bold=True
    )

    reason_font = pygame.font.SysFont(
        "consolas",
        26,
        bold=True
    )

    score_font = pygame.font.SysFont(
        "consolas",
        28
    )

    restart_font = pygame.font.SysFont(
        "consolas",
        22
    )

    # -------------------------
    # Text
    # -------------------------

    game_over_surface = game_over_font.render(
        "GAME OVER",
        True,
        (255, 220, 80)
    )

    reason_surface = reason_font.render(
        reason,
        True,
        (255, 100, 100)
    )

    score_surface = score_font.render(
        f"Final Score: {score}",
        True,
        (255, 255, 255)
    )

    restart_surface = restart_font.render(
        "Press R to restart",
        True,
        (200, 200, 200)
    )

    # -------------------------
    # Center everything
    # -------------------------

    center_x = surface.get_width() // 2

    surface.blit(
        game_over_surface,
        game_over_surface.get_rect(
            center=(center_x, 165)
        )
    )

    surface.blit(
        reason_surface,
        reason_surface.get_rect(
            center=(center_x, 215)
        )
    )

    surface.blit(
        score_surface,
        score_surface.get_rect(
            center=(center_x, 265)
        )
    )

    surface.blit(
        restart_surface,
        restart_surface.get_rect(
            center=(center_x, 320)
        )
    )