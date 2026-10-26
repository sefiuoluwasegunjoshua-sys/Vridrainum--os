from flask import Flask
app = Flask(__name__)

HTML = '''
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#000;color:#0ff;font-family:monospace;text-align:center;padding:20px}
button{padding:18px 35px;font-size:18px;background:#0ff;color:#000;border:none;border-radius:30px;margin:10px}
#log{background:#111;padding:15px;border-radius:10px;margin-top:20px;color:#fff;text-align:left}</style>
</head>
<body>
<h1>VIBRANIUM OS</h1>
<div style="width:120px;height:120px;border-radius:50%;background:cyan;margin:20px auto;box-shadow:0 0 50px cyan"></div>
<h3 id="st">Ready</h3>
<button onclick="testSpeak()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<div id="log">1. Click TEST VOICE<br>2. Then HEY JARVIS</div>
<script>
function testSpeak(){
 document.getElementById('st').innerText='Speaking...';
 var m=new SpeechSynthesisUtterance('Vibranium OS online Sefiu, working!');
 speechSynthesis.speak(m);
}
function startListen(){
 var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){alert('Update Chrome');return;}
 var rec=new SR(); rec.lang='en-US';
 rec.onstart=function(){document.getElementById('st').innerText='LISTENING';};
 rec.onerror=function(e){alert('Mic error: '+e.error+' - Allow mic in site settings');};
 rec.onresult=function(e){
  var t=e.results[0][0].transcript;
  document.getElementById('log').innerHTML='<b>You:</b> '+t;
  var txt='You said '+t;
  if(t.toLowerCase().includes('hello')) txt='Hello boss Sefiu!';
  if(t.toLowerCase().includes('time')) txt='Time is '+new Date().toLocaleTimeString();
  document.getElementById('log').innerHTML+='<br><b>Jarvis:</b> '+txt;
  speechSynthesis.speak(new SpeechSynthesisUtterance(txt));
 };
 rec.start();
}
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

if __name__ == '__main__':
    app.run()
