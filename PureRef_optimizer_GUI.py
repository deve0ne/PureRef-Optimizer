import webview
import threading
import json
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

# Create a simple HTML interface
html = """
<!DOCTYPE html>
<html>
<head>
    <title>PureRef Optimizer</title>
    <script>
        function startOptimization() {
            var input_file = document.getElementById('input_file').value;
            var max_dimension = parseInt(document.getElementById('max_dimension').value);
            var colors = parseInt(document.getElementById('colors').value);
            var processes = parseInt(document.getElementById('processes').value);

            var options = {
                input_file: input_file,
                max_dimension: max_dimension,
                colors: colors,
                processes: processes
            };

            pywebview.api.start_optimization(options);
        }

        function optimizationStarted() {
            alert('Optimization has started!');
        }
    </script>
</head>
<body>
    <h1>PureRef Optimizer</h1>
    <input type="file" id="input_file" accept=".pur"><br>
    Max Dimension: <input type="number" id="max_dimension" value="2048"><br>
    Colors: <input type="number" id="colors" value="256"><br>
    Processes: <input type="number" id="processes" value="6"><br>
    <button onclick="startOptimization()">Start Optimization</button>
</body>
</html>
"""

# Set up the JS API
class Api:
    def __init__(self, window):
        self.window = window

    def start_optimization(self, options):
        start_optimization(self.window, options)

# Create the webview window
def create_window():
    window = webview.create_window('PureRef Optimizer', html=html)
    window.api = Api(window)  # Set the API for the window
    webview.start(debug=True)

if __name__ == '__main__':
    create_window()