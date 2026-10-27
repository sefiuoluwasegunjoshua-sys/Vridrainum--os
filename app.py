import os
from flask import Flask
app = Flask(__name__)

PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:15px}button{padding:18px 28px;background:#0ff;color:#000;border:none;border-radius:30px;margin:8px;font-weight:bold;font-size:16px}#log{background:#111;color:#0f0;padding:12px;border-radius:12px;margin-top:15px;text-align:left;min-height:80px}</style>
</head><body><h1>VIBRANIUM OS</h1><h3 id="st">Ready</h3>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<div id="log">1. Click TEST VOICE first<br>2. Then HEY JARVIS and say who are you</div>
<script>
var synth=window.speechSynthesis;
function speak(t){
 synth.cancel(); synth.resume();
 var u=new SpeechSynthesisUtterance(t);
 u.rate=0.9; u.volume=1; u.lang='en-US';
 var x=setInterval(function(){if(synth.speaking){synth.pause();synth.resume();}},2500);
 u.onend=function(){clearInterval(x); document.getElementById('st').innerText='Ready';};
 document.getElementById('st').innerText='Speaking...';
 synth.speak(u);
}
function testVoice(){
 synth.resume();
 speak('I am Vibranium OS, your Jarvis built by Sefiu in Lagos. All systems online boss!');
}
function startListen(){
 synth.cancel(); synth.resume();
 var R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Use Chrome');return;}
 var r=new R(); r.lang='en-US';
 r.onstart=function(){synth.resume(); document.getElementById('st').innerText='LISTENING...'; document.getElementById('log').innerText='Listening...';};
 r.onresult=function(e){
  var t=e.results[0][0].transcript;
  var l=t.toLowerCase(); var a='';
  if(l.includes('who')) a='I am Vibranium OS, your personal Jarvis, created by you Sefiu in Lagos Nigeria. I am your loyal assistant boss!';
  else if(l.includes('time')) a='Boss time is '+new Date().toLocaleTimeString();
  else if(l.includes('hello')||l.includes('hi')) a='Hello boss Sefiu! Vibranium online sir!';
  else a='You said '+t+'. I am Vibranium OS boss, ready!';
  document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br><b>Jarvis:</b> '+a;
  speak(a);
 };
 r.start();
}
</script></body></html>
'''

@app.route('/')
def home():
    return PAGE

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
