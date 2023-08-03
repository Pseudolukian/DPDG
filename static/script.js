function generateData() {
    let paramsForm = document.getElementById("Models_include");
    let modelForm = document.getElementById("set_up_generator");
    let type_files_Form = document.getElementById("type_of_files");

    document.getElementById('res_data').removeAttribute('disabled');
    
    
    let formData = new FormData();

    // Добавляем данные из первой формы
    for (let [key, value] of new FormData(paramsForm)) {
        formData.append(key, value);
    }

    // Добавляем данные из второй формы
    for (let [key, value] of new FormData(modelForm)) {
        formData.append(key, value);
    }

    // Добавляем данные из третьей формы
    for (let [key, value] of new FormData(type_files_Form)) {
        formData.append(key, value);
    }

    fetch("/generate/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        handleGeneratedUrl(data);
    })
    .catch(error => console.error("Error:", error));

    
}
