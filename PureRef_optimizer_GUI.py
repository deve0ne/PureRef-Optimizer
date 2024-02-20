import eel
import sys
from PureRef_optimizer import process_pureref_file, argparse

eel.init("web")


@eel.expose
def set_input_file(input_file):
    global args
    args.input_file = input_file


@eel.expose
def start_optimization(max_dimension, colors):
    args.max_dimension = int(max_dimension)
    args.colors = int(colors)
    process_pureref_file(args, progress_callback=update_progress)


def update_progress(progress):
    eel.updateProgress(progress)


def main():
    global args
    parser = argparse.ArgumentParser(description="Optimize PureRef files.")
    parser.add_argument("--input_file", type=str, help="The input PureRef file path.")
    parser.add_argument(
        "--max_dimension",
        type=int,
        default=2048,
        help="Maximum dimension for the longest side of the image.",
    )
    parser.add_argument(
        "--colors",
        type=int,
        default=256,
        help="Number of colors for the image palette.",
    )
    parser.add_argument(
        "--processes", type=int, default=6, help="Number of processes to use."
    )
    args = parser.parse_args()

    eel.start("gui.html", mode="electron", size=(360, 600))
    observer.join()

import eel
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Путь к папке с исходниками, которые нужно отслеживать
watched_dir = "web"

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        eel.reload_page()  # Функция для перезагрузки страницы

@eel.expose
def reload_page():
    eel.browsers[0].reload()

# Настройка Watchdog
event_handler = ReloadHandler()
observer = Observer()
observer.schedule(event_handler, path=watched_dir, recursive=True)
observer.start()




if __name__ == "__main__":
    main()
