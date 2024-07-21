window.onload = function() {
  const audio = new Audio('../../GARBAGE/output_audio.mp3');

  audio.addEventListener('canplaythrough', () => {
    console.log('Audio can play through.');
    audio.play().catch((error) => {
      console.error('Playback error:', error);
    });
  });

  audio.addEventListener('error', (e) => {
    console.error('Audio error:', e);
  });

  audio.addEventListener('loadstart', () => {
    console.log('Audio load started.');
  });

  audio.addEventListener('loadeddata', () => {
    console.log('Audio data loaded.');
  });

  audio.addEventListener('loadedmetadata', () => {
    console.log('Audio metadata loaded.');
  });
}


const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
  const recognition = new SpeechRecognition();

  let container = document.querySelector('.container');
  let jarvis = document.querySelector(".center");
  let jarvis_hood = document.querySelector(".bar-3");

  jarvis_hood.addEventListener("click", () => {
    jarvis.style.display = "none";
    let user = document.createElement("div");
    user.classList.add("user");
    container.appendChild(user);

    user.innerHTML = "Listning..."

    recognition.start();
    let siriWave = new SiriWave({
      container: document.querySelector(".siri-wave"),
      width: 350,
      height: 150,
      autostart: true,
      style: "ios9"
    });
    document.querySelector(".siri-wave").style.display = "block";

    recognition.onresult = (event) => {
      const speechToText = event.results[0][0].transcript;
      console.log(speechToText);
      user.innerHTML = "You: " + speechToText;

      let formatStt = speechToText.toLowerCase();

      if(formatStt.includes("hello")){
        setTimeout(()=>{
          user.innerHTML = "Hello, sir how can I help you?"
          
        }, 1000)
        setTimeout(()=>{
          recognition.start()
        }, 1000)
        
      }
      
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
    };

    recognition.onend = () => {
      console.log("Speech recognition service disconnected");
      
      /*jarvis.style.display = "flex";*/
      /*document.querySelector(".siri-wave").style.display = "none";*/
    };
  });
} else {
  console.warn("Speech Recognition is not supported in this browser.");
}
