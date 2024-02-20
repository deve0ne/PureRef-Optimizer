import webview
import threading
from PureRef_optimizer import process_pureref_file, argparse

# Define a function to handle the optimization process
def optimize_pureref_file(options):
    args = argparse.Namespace(
        input_file=options['input_file'],
        max_dimension=options['max_dimension'],
        colors=options['colors'],
        processes=options['processes']
    )
    process_pureref_file(args)

# Define a function to be called from the JS API
def start_optimization(window, options):
    threading.Thread(target=optimize_pureref_file, args=(options,)).start()
    window.evaluate_js('optimizationStarted()')

# Set up the JS API
class Api:
    def __init__(self, window):
        self.window = window

    def start_optimization(self, options):
        start_optimization(self.window, options)


import watchfiles

def watch_and_reload(window):
    for change in watchfiles.watch('web'):
        window.evaluate_js('window.location.reload()')

def create_window():
    with open('./web/gui.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    window = webview.create_window('PureRef Optimizer', 'web/gui.html', resizable=False, width=360, height=600, background_color="#0E0E11")
    window.api = Api(window)  # Set the API for the window
    webview.start(func=watch_and_reload, args=window, debug=True, http_server=True)


if __name__ == '__main__':
    create_window()