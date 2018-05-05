import logging

SIM = 90
GAME = 80
ROUND = 70
TURN = 60

logging.addLevelName(GAME, "GAME")
logging.addLevelName(SIM, "SIM")
logging.addLevelName(ROUND, "ROUND")
logging.addLevelName(TURN, "TURN")


logger = logging.getLogger(__name__)
logger.setLevel(SIM)
