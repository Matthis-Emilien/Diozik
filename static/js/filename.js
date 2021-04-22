const fileInput = document.querySelector('#file-js-example input[type=file]');
fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
        const fileName = document.querySelector('#file-js-example .name');
        fileName.textContent = fileInput.files[0].name;
        console.log('True')
    }
}

