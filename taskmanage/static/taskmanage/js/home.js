function checkpersent(task_id) {
    fetch('api/' + 16 + '/check')
    .then(response => response.json())
    .then(display)
    .catch(function(error) {
        console.log('ERROR:' + error);
    });
}

function display(result) {
    let per = document.getElementById('persent');
    per.textContent = result.persent;
}