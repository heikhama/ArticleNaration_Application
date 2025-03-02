async function submitText() {
    try {
        const prompt = document.getElementById('prompt').value;
        const voice = document.getElementById('voice').value;
        const language = document.getElementById('language').value;
        const submitButton = document.getElementById('submit');
        submitButton.disabled = true;
        const responseDivmessage = document.getElementById('message');

        responseDivmessage.innerHTML = `<p style="color: red;">TTS is Generating... Kindly wait</p>`;

        const response = await fetch('/generate-speech', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: prompt, voice: voice, language: language })
        });

        const data = await response.json();

        if (!data.audio_path) {
            responseDivmessage.innerHTML = `<p style="color: red;">Error: No audio file generated.</p>`;
            submitButton.disabled = false;
            return;
        }

        responseDivmessage.innerHTML = `<p style="color: green;">${data.message}</p>`;

        let formatheader = data.responseMessage || "Prompt failed to load";

        document.getElementById("playaudio").innerHTML = `
            <audio src="/get-audio/${data.audio_path.split('/').pop()}" id="audioPlayer" controls></audio>
        `;

        // Set up the download link
        const downloadLink = document.getElementById('download_link');
        const savedFilename = data.audio_path.split('/').pop();
        downloadLink.href = `/get-audio/${savedFilename}`;
        downloadLink.style.display = 'inline';
        downloadLink.textContent = 'Download Audio';

        const responseDivresults = document.getElementById('results');
        responseDivresults.innerHTML = `
            <p><strong>Translated Prompt:</strong> ${prompt}</p>  
            <pre id="generatedCode">${formatheader}</pre>
            <button id="copyButton">Copy Content</button>
        `;

        document.getElementById("copyButton").addEventListener("click", function () {
            copyToClipboard(document.getElementById("generatedCode").textContent);
        });

    } catch (error) {
        console.error('Error:', error);
    } finally {
        submitButton.disabled = false; // Ensure button is re-enabled
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => alert("Content copied to clipboard!"))
        .catch(err => {
            console.error("Failed to copy: ", err);
            alert("Failed to copy content to clipboard.");
        });
}
