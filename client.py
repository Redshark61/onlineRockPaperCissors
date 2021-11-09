import pygame
from game import Game
from network import Network
from button import Buttons
import variables as var


def redrawWindow(win: pygame.Surface, game: Game, p: int):
    """
    Draw the main window, and display the game
    """
    win.fill((128, 128, 128))

    # If the game is not created, we show the waiting screen
    if not game.connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player", 1, (255, 0, 0), True)
        win.blit(text, (var.width/2-text.get_width()/2, var.height/2-text.get_height()/2))
    # Else, it means that the game can start
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your move", 1, (0, 255, 255))
        win.blit(text, (80, 200))
        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)
        # If both of the player played, we show the moves
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        # Else, we display the moves according to wich player you are
        else:
            if game.player1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.player1Went:
                text1 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting", 1, (0, 0, 0))

            if game.player2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.player2Went:
                text2 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting", 1, (0, 0, 0))

        # Display the moves on the left or the right depending if you are player 1 or 2
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Buttons("Rock", 50, 500, (0, 0, 0)), Buttons("Paper", 250, 500, (255, 0, 0)), Buttons("Scissors", 450, 500, (0, 255, 0))]


def gameLoop(win: pygame.Surface):
    """
    Loop wich runs the game
    """
    run = True
    clock = pygame.time.Clock()
    # Connect to the server
    n = Network()
    # Get the payer number
    player = int(n.getPlayer())
    print(f"You are player {player}")

    while run:
        clock.tick(60)
        try:
            # We send 'get', and get back the instance of the game
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game, error ")
            break

        # If both of the players played, we can show the screen
        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game error ")
                break

            font = pygame.font.SysFont("comicsans", 90)
            # We check who won
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", 1, (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You lost!", 1, (255, 0, 0))

            win.blit(text, (var.width/2 - text.get_width()/2, var.height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        # Else, if one the players hasn't played, we wait for the other player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get on wich button the player clicked
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        # Send wich button you clicked on
                        if player == 0:
                            if not game.player1Went:
                                n.send(btn.text)
                        else:
                            if not game.player2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menuScreeen(win: pygame.Surface):
    """
    Draw the menu screen
    """
    run = True
    clock = pygame.time.Clock()

    # Run the menu screen
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    gameLoop(win)
