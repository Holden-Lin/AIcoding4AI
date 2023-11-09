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
    async function generateGeneralText() {
        try {
            const response = await fetch('/gen', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    book_name: generalInput.value
                })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // replace the \\n from llm api's original reponse with line break
            generalOutput.innerHTML = data.intro.replace(/\\n/g, '<br>');

            copyTextBtn.style.display = 'block'; // Make sure 'copyTextBtn' is the correct ID for the copy button
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            generalOutput.textContent = 'Error generating text. Please try again.';
        }
    }


    async function generateBookPromotionText() {
        const briefing = sourceSelection.value === 'manual' ? bookBriefingInput.value : null;
        const response = await fetch('/gen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                book_name: bookNameInput.value,
                book_briefing: briefing
            })
        });
        const data = await response.json();
        bookOutput.textContent = data.intro;
        copyBookTextBtn.style.display = 'block';
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
