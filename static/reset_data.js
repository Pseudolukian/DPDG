function resetData() {
    fetch('/reset/', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data) {
            window.location.reload();  // Перезагрузка страницы
        } else {
            console.error('Ошибка при сбросе данных.');
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
    });
}
