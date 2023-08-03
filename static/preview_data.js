function previewData() {
    const csvUrl = document.querySelector('a[href$=".csv"]').href;

    Papa.parse(csvUrl, {
        download: true,
        complete: function(results) {
            const table = document.getElementById('csvTable');
            table.innerHTML = ''; 

            
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            results.data[0].forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            
            const tbody = document.createElement('tbody');
            for (let i = 1; i < results.data.length; i++) {
                const row = document.createElement('tr');
                results.data[i].forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            }
            table.appendChild(tbody);

            
            const modal = document.getElementById('previewModal');
            modal.style.display = "block";
            const closeButton = document.querySelector('.close-button');
            closeButton.onclick = () => modal.style.display = "none";
        }
    });
}
