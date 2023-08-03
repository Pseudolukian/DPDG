function handleGeneratedUrl(data) {
    const outputDiv = document.getElementById('output');
    const previewButton = document.getElementById('previw_data'); 

    
    outputDiv.innerHTML = '';

    
    const iconPaths = {
        "CSV": "/static/csv.png",
        "JSON": "/static/json.png",
        "XLS": "/static/xls.png",
        "LiteSQL": "/static/sql.png",
        
    };

    for (let fileType in data) {
        
        const anchor = document.createElement('a');
        anchor.href = data[fileType];
        anchor.style.marginRight = '10px'; 

        
        if (iconPaths[fileType]) {
            const img = document.createElement('img');
            img.src = iconPaths[fileType];
            img.alt = fileType;
            img.style.marginRight = '5px';  
            anchor.appendChild(img);
        }

        
        const textNode = document.createTextNode(`Download ${fileType}`);
        anchor.appendChild(textNode);

        anchor.download = `generated_data.${fileType.toLowerCase()}`;

        
        outputDiv.appendChild(anchor);
    }

    
    if (data["CSV"]) {
        previewButton.removeAttribute('disabled');
    } else {
        previewButton.setAttribute('disabled', 'disabled');
    }
}
