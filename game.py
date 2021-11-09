class Game:
    """
    Class wich create and manage the game
    """

    def __init__(self, id):
        # Player 1 has played
        self.player1Went = False
        # Player 2 has played
        self.player2Went = False
        # Game is ready to be played
        self.ready = False
        # ID of the game
        self.id = id
        # Moves of each player (player 0 and 1)
        self.moves = [None, None]
        # Win of each player (player 0 and 1)
        self.wins = [0, 0]
        # Ties
        self.ties = 0

    def getPlayerMove(self, player: int):
        """
        Get player moves. player is either 0 or 1
        """
        return self.moves[player]

    def play(self, player: int, move: str):
        """
        Make the player play
        """
        self.moves[player] = move
        if player == 0:
            self.player1Went = True
        else:
            self.player2Went = True

    def connected(self) -> bool:
        """
        If the game is connected
        """
        return self.ready

    def bothWent(self) -> bool:
        """
        If both player has played
        """
        return self.player1Went and self.player2Went

    def winner(self) -> int:
        """
        Get the winner of the game
        """
        player1 = self.moves[0].upper()[0]
        player2 = self.moves[1].upper()[0]
        winner = -1

        if player1 == "R" and player2 == "S":
            winner = 0
        elif player1 == "S" and player2 == "R":
            winner = 1
        elif player1 == "P" and player2 == "R":
            winner = 0
        elif player1 == "R" and player2 == "P":
            winner = 1
        elif player1 == "S" and player2 == "P":
            winner = 0
        elif player1 == "P" and player2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        """
        Reset the players turns
        """
        self.player1Went = False
        self.player2Went = False
