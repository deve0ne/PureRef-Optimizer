document.getElementById('max_dimension').oninput = function() {
    document.getElementById('max_dimension_value').innerText = this.value;
}

document.getElementById('colors').oninput = function() {
    document.getElementById('colors_value').innerText = this.value;
}

document.getElementById('drop_zone').ondrop = function(e) {
    e.preventDefault();
    if (e.dataTransfer.items) {
        let file = e.dataTransfer.items[0].getAsFile();
        eel.set_input_file(file.path);
    }
}

document.getElementById('drop_zone').ondragover = function(e) {
    e.preventDefault();
}

function startOptimization() {
    let max_dimension = document.getElementById('max_dimension').value;
    let colors = document.getElementById('colors').value;
    eel.start_optimization(max_dimension, colors)(updateProgress);
}

function updateProgress(progress) {
    document.getElementById('progress_bar').style.width = `${progress * 100}%`;
}