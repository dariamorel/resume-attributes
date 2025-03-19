const fileInput = document.getElementById('fileInput');
const fileNameDiv = document.getElementById('fileName');

fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
        // Если файл выбран, отображаем его имя
        fileNameDiv.textContent = fileInput.files[0].name;
    } else {
        // Если файл не выбран, показываем исходный текст
        fileNameDiv.textContent = 'Файл не загружен';
    }
});
