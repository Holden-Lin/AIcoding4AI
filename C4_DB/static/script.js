console.log("Script loaded")

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const generalInput = document.getElementById('general-input');
    const generalOutput = document.getElementById('general-output');
    const generateTextBtn = document.getElementById('generate-text');
    const copyTextBtn = document.getElementById('copy-text');

    const bookNameInput = document.getElementById('book-name-input');
    const sourceSelection = document.getElementById('source-selection');
    const generateBookTextBtn = document.getElementById('generate-book-text');
    const copyBookTextBtn = document.getElementById('copy-book-text');
    const bookOutput = document.getElementById('book-output');

    // Event listeners
    generateTextBtn.addEventListener('click', () => generateGeneralText());
    copyTextBtn.addEventListener('click', () => copyText(generalOutput));

    generateBookTextBtn.addEventListener('click', () => generateBookPromotionText());
    copyBookTextBtn.addEventListener('click', () => copyText(bookOutput));

    // get user ip as the user's identifier
    async function getUserIP() {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    }

    // after stream data is collcted, use this function to save data to db
    async function saveDataToServer(writingId, answerData) {
        const updateData = {
            answer: answerData,
        };

        try {
            const response = await fetch(`/update/${writingId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });

            const responseData = await response.json();
            console.log('Update success:', responseData);
        } catch (error) {
            console.error('Error updating writing:', error);
        }
    }


    async function generateGeneralText() {
        // Elements and loading indication
        const loadingDiv = document.getElementById('general-loading');
        loadingDiv.style.display = 'block';
        console.log("Loading display set to block");

        const userIP = await getUserIP();
        console.log("current user ip is:", userIP);

        // Clear previous output
        generalOutput.innerHTML = '';
        let writingId;
        // save stream data and write to db later
        let accumulatedData = "";


        // Encode the book name for use in a query string
        const user_input = encodeURIComponent(generalInput.value);
        const url = `/gen?user_input=${user_input}&user_ip=${userIP}`;

        const eventSource = new EventSource(url);

        // get Id(db index) to update db later
        eventSource.addEventListener("init-id", function (event) {
            writingId = event.data;
        });

        // Handle a message event
        eventSource.onmessage = function (event) {
            //console.log(event.data);
            generalOutput.innerHTML += event.data.replace(/\n/g, '<br>');
            accumulatedData += event.data;
        };

        // Handle stream completion
        eventSource.addEventListener('stream-end', () => {
            console.log("Stream closed by the server");
            eventSource.close(); // Close the connection
            copyTextBtn.style.display = 'block'; // Show the copy text button
            loadingDiv.style.display = 'none'; // Hide the loading indicator
            console.log("updating generation to server");
            saveDataToServer(writingId, accumulatedData);
        });

        eventSource.onerror = function (error) {
            if (eventSource.readyState === EventSource.CLOSED) {
                console.log('EventSource connection was closed.');
            } else {
                console.error('There was a problem with the event stream:', error);
                generalOutput.textContent = 'Error generating text. Please try again.';
                loadingDiv.style.display = 'none'; // Hide the loading indicator
            }
            eventSource.close(); // Close the connection
        };

    }

    async function generateBookPromotionText() {
        const loadingDiv = document.getElementById('book-loading');
        loadingDiv.style.display = 'block';
        copyBookTextBtn.style.display = 'None';
        bookOutput.innerHTML = '';

        const bookName = encodeURIComponent(bookNameInput.value);
        const url = `/genbook?book_name=${bookName}`;

        try {
            const response = await fetch(url);
            const reader = response.body.getReader();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = new TextDecoder("utf-8").decode(value);

                try {
                    const data = JSON.parse(chunk);
                    if (data.message === "Stream closed") {
                        copyBookTextBtn.style.display = 'block';
                        loadingDiv.style.display = 'none';
                    } else if (data.error) {
                        console.error('Error:', data.error);
                        bookOutput.textContent = 'Error generating text. Please try again.';
                        loadingDiv.style.display = 'none';
                    } else {
                        bookOutput.innerHTML += `${data.replace(/\n/g, '<br>')}`;
                    }
                } catch (e) {
                    console.error('Error parsing JSON:', e);
                }
            }
        } catch (error) {
            console.error('Fetch error:', error);
            bookOutput.textContent = 'Error generating text. Please try again.';
            loadingDiv.style.display = 'none';
        }
    }

    async function loadHistory() {
        const userIP = await getUserIP();
        const response = await fetch(`/get_history?user_ip=${userIP}`);
        const historyData = await response.json();

        // Sort historyData by creat_time in descending order
        historyData.sort((a, b) => new Date(b.creat_time) - new Date(a.creat_time));

        const tbody = document.getElementById('history-table').querySelector('tbody');
        tbody.innerHTML = '';  // Clear existing content

        historyData.forEach(item => {
            const row = `<tr>
                <td>${item.user_ip}</td>
                <td>${item.prompt}</td>
                <td>${item.answer}</td>
                <td>${item.creat_time}</td>
            </tr>`;
            tbody.innerHTML += row;
        });
    }

    // Call loadHistory on page load or on a specific user action
    loadHistory();


    function copyText(outputElem) {
        if (!outputElem.textContent) return;

        navigator.clipboard.writeText(outputElem.textContent).then(() => {
            alert('Text copied to clipboard!');
        }).catch(err => {
            alert('Failed to copy text: ', err);
        });
    }

    // Tab switching logic
    function showSection(section) {
        const generalSection = document.getElementById('general-text-generation');
        const bookSection = document.getElementById('book-promotion-generation');
        if (section === 'general') {
            generalSection.style.display = 'block';
            bookSection.style.display = 'none';
        } else if (section === 'promotion') {
            generalSection.style.display = 'none';
            bookSection.style.display = 'block';
        }
    }

    // Set up initial tab state
    showSection('general');

    // Attach showSection to window for tab buttons
    window.showSection = showSection;
});
