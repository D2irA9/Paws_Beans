from globals import *
from classes.stations import StationManager

# Станции
station_manager = StationManager()

def game(events):
    """ Основной игрой цикл """
    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            station_manager.handle_events(events)

    station_manager.draw(screen)