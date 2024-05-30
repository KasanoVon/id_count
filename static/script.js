document.addEventListener('DOMContentLoaded', function() {
    const filterInput = document.getElementById('filter');
    const dropdown = document.getElementById('dropdown');
    const dateDropdown = document.getElementById('dateDropdown');
    const executeButton = document.getElementById('executeButton');
    const resultDiv = document.getElementById('result');

    filterInput.addEventListener('input', updateDropdown);

    dropdown.addEventListener('change', function() {
        const selectedText = dropdown.value;
        fetch('/get_selected_link', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `selected_text=${selectedText}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                console.log(data.url);
            }
        });
    });

    executeButton.addEventListener('click', function() {
        const url = ''; // Get the selected URL
        const idValue = document.getElementById('id').value;
        const keywordValue = document.getElementById('keyword').value;
        const date = dateDropdown.value;

        fetch('/execute_action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `url=${url}&id_value=${idValue}&keyword_value=${keywordValue}&date=${date}`
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = ''; // Clear previous results
            data.data.forEach(item => {
                const div = document.createElement('div');
                div.textContent = `URL: ${item[0]}, スレタイ: ${item[1]}, ID数: ${item[2]}, レス数: ${item[3]}`;
                resultDiv.appendChild(div);
            });
        });
    });

    function updateDropdown() {
        const filterText = filterInput.value.toLowerCase();
        for (let option of dropdown.options) {
            const text = option.textContent.toLowerCase();
            option.style.display = text.includes(filterText) ? '' : 'none';
        }
    }
});
