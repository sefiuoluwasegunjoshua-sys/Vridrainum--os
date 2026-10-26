from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html>
<head>
<title>VIBRANIUM OS - VOICE</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#000;color:#0ff;font-family:monospace;text-align:center;padding:30px}
h1{font-size:40px;text-shadow:0 0 20px #0ff}
button{padding:20px 40px;font-size:20px;background:#0ff;color:#000;border:none;border-radius:30px;box-shadow:0 0 30px #0ff;cursor:pointer;margin:20px}
#log{margin-top:30px;font-size:18px;color:#fff}
.orb{width:150px;height:150px;border-radius:50%;background:radial-gradient(#0ff,#00f);margin:20px auto;box-shadow:0 0 60px #0ff;animation:pulse 2s infinite}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
</style>
</head>
<body>
<h1>🔮 VIBRANIUM OS</h1>
<div class="orb" id="orb"></div>
<h2 id="status">Click to Activate Jarvis</h2>
<button onclick="startJarvis()">🎤 HEY JARVIS</button>
<div id="log">Say: Hello, What time is it, Who are you...</div>

<script>
let recognition;
function startJarvis(){
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.onstart = ()=>{ document.getElementById('status').innerText='🎧 LISTENING...'; document.getElementById('orb').style.background='radial-gradient(#f0f,#f00)'; }
  recognition.onresult = (e)=>{
    let text = e.results[0][0].transcript;
    document.getElementById('log').innerHTML = '<b>You:</b> ' + text + '<br>';
    respond(text.toLowerCase());
  }
  recognition.start();
}
function speak(text){
  document.getElementById('log').innerHTML += '<b>Jarvis:</b> ' + text + '<br>';
  let utter = new SpeechSynthesisUtterance(text);
  utter.rate=1; utter.pitch=1.2;
  speechSynthesis.speak(utter);
  document.getElementById('status').innerText='🔊 SPEAKING...';
  setTimeout(()=>{document.getElementById('status').innerText='Click to Activate Jarvis'; document.getElementById('orb').style.background='radial-gradient(#0ff,#00f)';}, 3000);
}
function respond(t){
  if(t.includes('hello')||t.includes('hi')) speak('Hello Sefiu! Vibranium OS online, all systems operational, sir.');
  else if(t.includes('time')) speak('The time is ' + new Date().toLocaleTimeString() + ' sir.');
  else if(t.includes('who are you')) speak('I am Vibranium OS, your personal AI Jarvis, built by you Sefiu from Lagos!');
  else if(t.includes('love you')) speak('I love you too boss, always here for you.');
  else if(t.includes('how are you')) speak('I am perfect sir, running on Render cloud, ready for missions.');
  else speak('You said ' + t + '. I am learning sir, tell me what to do next!');
}
</script>
</body>
</html>
    """

if __name__ == '__main__':
    app.run()
    
