let mediaRecorder;
let audioChunks = [];
let recordingStartTime;
let timerInterval;

function startRecording() {
    audioChunks = [];

    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
            clearInterval(timerInterval);
            document.getElementById("status").innerText = "Recording stopped. Processing...";

            const blob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioURL = URL.createObjectURL(blob);

            const recordedAudio = document.getElementById('recordedAudio');
            recordedAudio.src = audioURL;
            recordedAudio.style.display = "block";

            // Send to Flask server
            const formData = new FormData();
            formData.append('audio', blob, 'recorded.wav');
            const imageInput = document.querySelector('input[name="image"]');
            if (imageInput.files.length > 0) {
                formData.append('image', imageInput.files[0]);
            }

            fetch("/", {
                method: "POST",
                body: formData
            }).then(response => response.text())
              .then(html => {
                  document.open();
                  document.write(html);
                  document.close();
              });
        };

        mediaRecorder.start();
        recordingStartTime = Date.now();
        updateTimer();
        timerInterval = setInterval(updateTimer, 1000);

        document.getElementById("status").innerText = "Recording... 00:00";
    });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
    }
}

function updateTimer() {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const seconds = String(elapsed % 60).padStart(2, '0');
    document.getElementById("status").innerText = `Recording... ${minutes}:${seconds}`;
}
