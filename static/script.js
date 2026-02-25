document.addEventListener('DOMContentLoaded', function() {
    const filterInput = document.getElementById('filter');
    const dropdown = document.getElementById('dropdown');
    const dateDropdown = document.getElementById('dateDropdown');
    const executeButton = document.getElementById('executeButton');
    const resultDiv = document.getElementById('result');
    let selectedUrl = '';

    filterInput.addEventListener('input', updateDropdown);

    dropdown.addEventListener('change', function() {
        const selectedText = dropdown.value;
        fetch('/get_selected_link', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `selected_text=${encodeURIComponent(selectedText)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                selectedUrl = data.url;
                updateDateDropdown();
            }
        });
    });

    document.querySelectorAll('input[name="dateRange"]').forEach(function(radio) {
        radio.addEventListener('change', updateDateDropdown);
    });

    executeButton.addEventListener('click', function() {
        const idValue = document.getElementById('id').value;
        const keywordValue = document.getElementById('keyword').value;
        const date = dateDropdown.value;

        if (!selectedUrl) {
            alert('板を選択してください');
            return;
        }
        if (!date) {
            alert('日付を選択してください');
            return;
        }

        fetch('/execute_action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `url=${encodeURIComponent(selectedUrl)}&id_value=${encodeURIComponent(idValue)}&keyword_value=${encodeURIComponent(keywordValue)}&date=${encodeURIComponent(date)}`
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = '';
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

    function updateDateDropdown() {
        const checkedRadio = document.querySelector('input[name="dateRange"]:checked');
        if (!checkedRadio) return;
        const dateRange = parseInt(checkedRadio.value);
        const today = new Date();
        dateDropdown.innerHTML = '<option value="">日付を選択</option>';

        let start, end;
        if (dateRange > 0) {
            // 直近15日: 今日から14日前まで
            start = 0;
            end = dateRange - 1;
        } else {
            // 直近15日以前: 15日前から30日前まで
            start = Math.abs(dateRange);
            end = start + Math.abs(dateRange) - 1;
        }

        for (let i = start; i <= end; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() - i);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const dateStr = `${year}${month}${day}`;
            const displayStr = `${year}/${month}/${day}`;
            const option = document.createElement('option');
            option.value = dateStr;
            option.textContent = displayStr;
            dateDropdown.appendChild(option);
        }
    }

    updateDateDropdown();
});
