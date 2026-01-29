from globals import *
from classes.stations import StationManager

# Станции
station_manager = StationManager()

def game(events):
    """ Основной игрой цикл """
    py.display.set_caption('Paws & Beans')
    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
    station_manager.handle_events(events)

    station_manager.draw(screen)