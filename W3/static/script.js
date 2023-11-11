console.log("Script loaded")

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const generalInput = document.getElementById('general-input');
    const generalOutput = document.getElementById('general-output');
    const generateTextBtn = document.getElementById('generate-text');
    const copyTextBtn = document.getElementById('copy-text');

    const bookNameInput = document.getElementById('book-name-input');
    const sourceSelection = document.getElementById('source-selection');
    const bookBriefingInput = document.getElementById('book-briefing-input');
    const generateBookTextBtn = document.getElementById('generate-book-text');
    const copyBookTextBtn = document.getElementById('copy-book-text');
    const bookOutput = document.getElementById('book-output');

    // Event listeners
    generateTextBtn.addEventListener('click', () => generateGeneralText());
    copyTextBtn.addEventListener('click', () => copyText(generalOutput));

    generateBookTextBtn.addEventListener('click', () => generateBookPromotionText());
    copyBookTextBtn.addEventListener('click', () => copyText(bookOutput));

    sourceSelection.addEventListener('change', (e) => {
        bookBriefingInput.style.display = e.target.value === 'manual' ? 'block' : 'none';
    });

    // Functions
    // async function generateGeneralText() {
    //     // 获取灵感生成中的元素
    //     const loadingDiv = document.getElementById('general-loading');
    //     // 展示灵感生成中 为block
    //     loadingDiv.style.display = 'block';
    //     console.log("Loading display set to block");


    //     try {

    //         const response = await fetch('/gen', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify({
    //                 book_name: generalInput.value
    //             })
    //         });
    //         if (!response.ok) {
    //             throw new Error(`HTTP error! status: ${response.status}`);
    //         }
    //         const data = await response.json();

    //         // replace the \\n from llm api's original reponse with line break
    //         generalOutput.innerHTML = data.intro.replace(/\\n/g, '<br>');

    //         copyTextBtn.style.display = 'block';
    //         // 灵感生成中消失
    //         loadingDiv.style.display = 'None';
    //     } catch (error) {
    //         console.error('There was a problem with the fetch operation:', error);
    //         generalOutput.textContent = 'Error generating text. Please try again.';
    //     }
    // }


    async function generateGeneralText() {
        // Elements and loading indication
        const loadingDiv = document.getElementById('general-loading');
        loadingDiv.style.display = 'block';
        console.log("Loading display set to block");

        // Clear previous output
        generalOutput.innerHTML = '';

        // Encode the book name for use in a query string
        const bookName = encodeURIComponent(generalInput.value);
        const url = `/gen?book_name=${bookName}`;

        const eventSource = new EventSource(url);

        // Handle a message event
        eventSource.onmessage = function (event) {
            console.log(event.data);
            generalOutput.innerHTML += event.data.replace(/\n/g, '<br>');
        };

        // Handle stream completion
        eventSource.addEventListener('stream-end', () => {
            console.log("Stream closed by the server");
            eventSource.close(); // Close the connection
            copyTextBtn.style.display = 'block'; // Show the copy text button
            loadingDiv.style.display = 'none'; // Hide the loading indicator
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
        // Elements and loading indication
        const loadingDiv = document.getElementById('general-loading');
        loadingDiv.style.display = 'block';
        console.log("Loading display set to block");

        // Clear previous output
        generalOutput.innerHTML = '';

        // Encode the book name for use in a query string
        const bookName = encodeURIComponent(generalInput.value);
        const url = `/genbook?book_name=${bookName}`;

        const eventSource = new EventSource(url);

        // Handle a message event
        eventSource.onmessage = function (event) {
            if (event.data === "Stream closed") {
                console.log("Stream closed by the server");
                eventSource.close();
                copyTextBtn.style.display = 'block';
                loadingDiv.style.display = 'none';
                // Any additional cleanup here
            } else {
                // Normal handling of messages
                console.log(event.data);
                generalOutput.innerHTML += event.data.replace(/\n/g, '<br>');
            }
        };

        // eventSource.addEventListener('add', event => {
        //     console.log(event.data);
        //     generalOutput.innerHTML += event.data.replace(/\\n/g, '<br>');
        // });

        // Handle an error event
        eventSource.onerror = function (error) {
            console.error('There was a problem with the event stream:', error);
            console.log('EventSource readyState:', eventSource.readyState);

            if (eventSource.readyState === EventSource.CLOSED) {
                console.log('EventSource connection was closed.');
            } else if (eventSource.readyState === EventSource.CONNECTING) {
                console.log('EventSource is trying to connect.');
            } else {
                console.log('EventSource is open.');
            }

            // Add a conditional check here to handle different states
            if (eventSource.readyState !== EventSource.OPEN) {
                generalOutput.textContent = 'Error generating text. Please try again.';
                eventSource.close(); // Close the connection
                loadingDiv.style.display = 'none'; // Hide the loading indicator
            }
        };


        // Optional: Handle stream completion (if the server sends a specific event to indicate this)
        // Adjust this part according to your server-side implementation
        eventSource.addEventListener('finish', () => {
            eventSource.close(); // Close the connection
            copyTextBtn.style.display = 'block'; // Show the copy text button
            loadingDiv.style.display = 'none'; // Hide the loading indicator
        });
    }

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
