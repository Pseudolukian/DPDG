function handleGeneratedUrl(data) {
    const outputDiv = document.getElementById('output');
    
    // Очищаем предыдущие ссылки, если они есть
    outputDiv.innerHTML = '';

    // Словарь с путями к изображениям для разных типов файлов
    const iconPaths = {
        "CSV": "/static/csv.png",
        "JSON": "/static/json.png",
        "XLS": "/static/xls.png",
        "LiteSQL": "/static/sql.png",
        // ... добавьте другие пути при необходимости
    };

    for (let fileType in data) {
        // Создаем новую ссылку для каждого файла
        const anchor = document.createElement('a');
        anchor.href = data[fileType];
        anchor.style.marginRight = '10px'; // небольшой отступ справа для удобства

        // Добавляем изображение, если оно есть в словаре
        if (iconPaths[fileType]) {
            const img = document.createElement('img');
            img.src = iconPaths[fileType];
            img.alt = fileType;
            img.style.marginRight = '5px';  // небольшой отступ справа от иконки к тексту
            anchor.appendChild(img);
        }

        // Добавляем текст к ссылке
        const textNode = document.createTextNode(`Download ${fileType}`);
        anchor.appendChild(textNode);

        anchor.download = `generated_data.${fileType.toLowerCase()}`;

        // Добавляем ссылку в outputDiv
        outputDiv.appendChild(anchor);
    }
}
