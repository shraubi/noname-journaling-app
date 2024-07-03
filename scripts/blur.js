const editor = document.getElementById('editor');
const status = document.getElementById('status');
const editorDiv = document.querySelector('.editor');

editor.addEventListener('input', async (e) => {
    const response = await fetch('/stroke', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({key: e.data, text: editor.value})
    });
    const data = await response.json();
    status.textContent = `Status: Last key pressed: ${data.letter}`;
    document.querySelector('.hardcore').textContent = data.letter;

    editorDiv.classList.remove('blur');
});

setInterval(async () => {
    const response = await fetch('/check-idle');
    const data = await response.json();
    if (data.blur) {
        editorDiv.classList.add('blur');
    } else {
        editorDiv.classList.remove('blur');
    }
    if (data.idle) {
        editor.value = '';
        status.textContent = 'Status: Idle detected, text cleared';
        document.querySelector('.hardcore').textContent = '';
        editorDiv.classList.remove('blur');
    }
}, 1000);

editor.addEventListener('scroll', () => {
    editorDiv.classList.toggle('cut-top', editor.scrollTop > 0);
    editorDiv.classList.toggle('cut-bottom', 
        editor.scrollHeight - editor.clientHeight - editor.scrollTop > 1);
});
