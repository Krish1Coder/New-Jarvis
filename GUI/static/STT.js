window.onload = function() {
    let inputbox = document.querySelector("#text");
    let send = document.querySelector(".send");
    let container = document.querySelector('.container');
    let user = document.querySelector(".user");
    let jarvis = document.querySelector(".center");
    let jarvis_hood = document.querySelector(".bar-3");
    let mic = document.querySelector(".mic");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = SpeechRecognition ? new SpeechRecognition() : null;

    if (recognition) {
        recognition.continuous = true;
        recognition.interimResults = false;

        recognition.onresult = (event) => {
            const speechToText = event.results[0][0].transcript;
            handleUserInput(speechToText);
        };

        recognition.onerror = (event) => {
            setTimeout(() => {
                recognition.start();  // Restart recognition on error
            }, 1000);  // Short delay before restarting
        };

        recognition.onend = () => {
            console.log("Speech recognition service disconnected");
        };
    } else {
        console.warn("Speech Recognition is not supported in this browser.");
    }

    function typingAnimation(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';

    function typeWriter() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            i++;
            setTimeout(typeWriter, speed);
        }
    }
    typeWriter();
    }


    function formatText(response) {
    if (response.includes("```")) {
        const parts = response.split(/```/);

        for (let i = 0; i < parts.length; i++) {
            if (i % 2 === 1) { 
                const codeBlock = `
                    <pre>
                        <code>${parts[i].trim()}</code>
                        <button class="copy-btn" onclick="copyCode(this)">Copy Code</button>
                    </pre>`;
                console.log("Code block with button:", codeBlock); // Debug log
                parts[i] = codeBlock;
            } else {
                parts[i] = parts[i]
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/_(.*?)_/g, '<em>$1</em>')
                    .replace(/~~(.*?)~~/g, '<del>$1</del>')
                    .replace(/`([^`]+)`/g, '<code>$1</code>')
                    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
            }
        }

        return parts.join('');
    } else {
        return response
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/_(.*?)_/g, '<em>$1</em>')
            .replace(/~~(.*?)~~/g, '<del>$1</del>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
    }
    }
    

    function handleUserInput(input) {
    jarvis.style.display = "none";
    if (!user) {
        user = document.createElement("div");
        user.classList.add("user");
        container.appendChild(user);
    }

    user.innerHTML = "You: " + input;
    anime({
        targets: user,
        opacity: [0, 1],
        translateY: [-10, 0],
        easing: 'easeOutQuad',
        duration: 500,
        complete: function() {
            user.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });

    fetch('/process_speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: input })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response === "Analysing Sir...") {
            captureImage(input);
        } else {
            user.innerHTML = "Jarvis: " + data.response;
            anime({
                targets: user,
                opacity: [0, 1],
                translateY: [-10, 0],
                easing: 'easeOutQuad',
                duration: 500,
                complete: function() {
                    user.scrollIntoView({ behavior: 'smooth', block: 'center' });

                    const audio = new Audio(data.audio_file);
                    audio.addEventListener('ended', () => {
                        recognition.start();
                    });
                    audio.addEventListener('pause', () => {
                        audio.src = ""; // Remove the source
                        audio.load();
                        recognition.start();
                    });
                    audio.play();
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
    }
    

    send.addEventListener("click", () => {
        let inputboxval = inputbox.value;
        if (inputboxval) {
            handleUserInput(inputboxval);
            inputbox.value = "";
        }
    });

    if (recognition) {
        jarvis_hood.addEventListener("click", () => {
            startSpeechRecognition();
        });

        mic.addEventListener("click", () => {
            recognition.start();
        });

        function startSpeechRecognition() {
            jarvis.style.display = "none";
            if (!user) {
                user = document.createElement("div");
                user.classList.add("user");
                container.appendChild(user);
            }
            typingAnimation(user, "Listening...");

            recognition.start();
            let siriWave = new SiriWave({
                container: document.querySelector(".siri-wave"),
                width: 350,
                height: 150,
                autostart: true,
                style: "ios9"
            });
            document.querySelector(".siri-wave").style.display = "block";

            document.body.addEventListener("click", (event) => {
                if (event.target !== inputbox && event.target !== send && !send.contains(event.target)) {
                    recognition.start();
                }
            });
        }

        function captureImage(user_input) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function (stream) {
                        let video = document.createElement('video');
                        video.autoplay = true;
                        video.srcObject = stream;

                        let canvas = document.createElement('canvas');
                        let context = canvas.getContext('2d');

                        video.onloadedmetadata = function () {
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;
                            context.drawImage(video, 0, 0, canvas.width, canvas.height);

                            let imageDataURL = canvas.toDataURL('image/png');
                            stream.getTracks().forEach(track => track.stop());

                            fetch('/capture_image', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ image: imageDataURL })
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log('Image saved successfully:', data);

                                // Trigger the delayed vision response
                                setTimeout(() => {
                                    fetch('/process_vision', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({ text: user_input })
                                    })
                                    .then(response => response.json())
                                    .then(data => {
                                        typingAnimation(user, "Jarvis: " + data.response);
                                        user.scrollIntoView({ behavior: 'smooth', block: 'center' });

                                        const audio = new Audio(data.audio_file);
                                        audio.addEventListener('ended', () => {
                                            recognition.start();
                                        });
                                        audio.addEventListener('pause', () => {
                                            audio.src = ""; // Remove the source
                                            audio.load();
                                            recognition.start();
                                        });
                                        audio.play();
                                    })
                                    .catch(error => {
                                        console.error('Error:', error);
                                    });
                                }, 10000); // Delay for the vision processing
                            })
                            .catch(error => {
                                console.error('Error saving image:', error);
                            });
                        };
                    })
                    .catch(function (error) {
                        console.error('Error accessing camera:', error);
                    });
            } else {
                console.warn('Camera not supported');
            }
        }
    }
}
