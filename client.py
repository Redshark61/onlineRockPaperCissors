import pygame
from network import Network
from button import Buttons

pygame.font.init()
width = 700
heigth = 700

win = pygame.display.set_mode((width, heigth))
pygame.display.set_caption("Client")


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player", 1, (255, 0, 0), True)
        win.blit(text, (width/2-text.get_width()/2, heigth/2-text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your move", 1, (0, 255, 255))
        win.blit(text, (80, 200))
        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
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


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getPlayer())
    print(f"You are player {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except Exception as e:
            run = False
            print("Couldn't get game error ", e)
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except Exception as e:
                run = False
                print("Couldn't get game error ", e)
                break

            font = pygame.font.SysFont("comicsans", 90)

            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", 1, (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You lost!", 1, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, heigth / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.player1Went:
                                n.send(btn.text)
                        else:
                            if not game.player2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


main()