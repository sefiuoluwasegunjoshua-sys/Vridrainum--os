import os
from flask import Flask, request, jsonify
app = Flask(__name__)

PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:10px}button{padding:14px 20px;background:#0ff;color:#000;border:none;border-radius:20px;margin:5px;font-weight:bold}#log{background:#111;color:#0f0;padding:10px;border-radius:10px;text-align:left;min-height:80px}</style>
</head><body><h2>VIBRANIUM OS v6 FAST</h2><h4 id="st">Loading voices...</h4>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button onclick="replay()" style="background:#0f0">🔊 REPLAY</button>
<div id="log">v6 Optimized - Fast + Stable</div>
<script>
var synth=window.speechSynthesis;
var voices=[];
var englishVoice=null;
var lastAns='I am Vibranium OS v6 fast and stable boss!';
function initVoices(){
 voices=synth.getVoices();
 englishVoice=voices.find(v=>v.name.includes('Google US English')) || voices.find(v=>v.lang==='en-US') || voices.find(v=>v.lang.startsWith('en')) || voices[0];
 if(englishVoice){document.getElementById('st').innerText='Ready - '+englishVoice.name; console.log('LOCKED:',englishVoice.name);}
 else {document.getElementById('st').innerText='Ready';}
}
initVoices();
if(speechSynthesis.onvoiceschanged!==undefined) speechSynthesis.onvoiceschanged=initVoices;
// WARM UP RENDER EVERY 5 MIN TO KEEP FAST
setInterval(()=>{fetch('/ping').then(()=>console.log('keep warm'));}, 5*60*1000);
function speak(t){
 lastAns=t;
 document.getElementById('st').innerText='Speaking...';
 synth.cancel();
 var u=new SpeechSynthesisUtterance(t);
 if(englishVoice) u.voice=englishVoice;
 u.lang='en-US'; u.rate=0.95; u.volume=1; u.pitch=1;
 u.onend=()=>{document.getElementById('st').innerText='Ready';};
 u.onerror=(e)=>{console.log('speech err',e); document.getElementById('st').innerText='Ready - retry'; setTimeout(()=>{synth.cancel(); synth.speak(u);},200);};
 // force queue
 setTimeout(()=>synth.speak(u),50);
}
function testVoice(){speak(lastAns);}
function replay(){speak(lastAns);}
function startListen(){
 var R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Use Chrome');return;}
 var r=new R(); r.lang='en-US'; r.interimResults=false;
 r.onstart=()=>{document.getElementById('st').innerText='LISTENING...';};
 r.onend=()=>{document.getElementById('st').innerText='Ready';};
 r.onresult=(e)=>{
  var t=e.results[0][0].transcript;
  document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br>...';
  fetch('/ask?q='+encodeURIComponent(t)).then(x=>x.json()).then(d=>{
   document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br><b>Jarvis:</b> '+d.answer;
   speak(d.answer);
  });
 };
 r.start();
}
</script></body></html>
'''
@app.route('/')
def home(): return PAGE
@app.route('/ping')
def ping(): return "warm"
@app.route('/ask')
def ask():
    q=request.args.get('q','').lower()
    if 'president' in q: return jsonify({"answer":"Boss, President is Bola Tinubu, since May 29 2023."})
    if 'know' in q and 'me' in q: return jsonify({"answer":"You are Sefiu boss, creator of Vibranium OS in Lagos, my only boss!"})
    return jsonify({"answer":f"You said {q}. I am v6 fast and stable, boss!"})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
