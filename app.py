import os
from flask import Flask, request, jsonify
app = Flask(__name__)

PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:12px}button{padding:18px;background:#0ff;color:#000;border:none;border-radius:25px;margin:6px;font-weight:bold}#log{background:#111;color:#0f0;padding:12px;border-radius:10px;text-align:left;min-height:80px}select{padding:10px;width:90%}</style>
</head><body><h2>VIBRANIUM OS v3</h2><h3 id="st">Loading voices...</h3>
<select id="voiceSel"></select><br>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button onclick="replay()" style="background:#0f0">🔊 PLAY ANSWER</button>
<div id="log">Wait for voices to load, then select voice, then TEST</div>
<script>
var synth=window.speechSynthesis;
var lastAnswer='';
var voices=[];
function loadVoices(){
 voices=synth.getVoices();
 var sel=document.getElementById('voiceSel');
 sel.innerHTML='';
 voices.forEach((v,i)=>{
  var o=document.createElement('option');
  o.textContent=v.name+' ('+v.lang+')';
  o.value=i;
  sel.appendChild(o);
 });
 if(voices.length>0){
  document.getElementById('st').innerText='Ready - '+voices.length+' voices';
  document.getElementById('log').innerText='Select a voice then TEST VOICE. Recommended: Google US English';
 } else {
  document.getElementById('st').innerText='No voices - waiting...';
 }
}
synth.onvoiceschanged=loadVoices;
setTimeout(loadVoices,1000);

function speak(t){
 lastAnswer=t;
 synth.cancel();
 setTimeout(()=>{
  var u=new SpeechSynthesisUtterance(t);
  var sel=document.getElementById('voiceSel');
  if(voices[sel.value]) u.voice=voices[sel.value];
  else if(voices[0]) u.voice=voices[0];
  u.rate=0.9; u.volume=1; u.pitch=1;
  u.onstart=function(){document.getElementById('st').innerText='Speaking...';};
  u.onend=function(){document.getElementById('st').innerText='Ready';};
  u.onerror=function(e){document.getElementById('log').innerText='Speech Error: '+e.error+' - Try another voice';};
  synth.speak(u);
 },100);
}
function testVoice(){speak('Hello boss Sefiu! I am Vibranium OS! Can you hear me now?');}
function replay(){if(lastAnswer) speak(lastAnswer); else speak('No answer yet boss');}
function startListen(){
 var R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Use Chrome browser boss');return;}
 var r=new R(); r.lang='en-US';
 r.onstart=function(){document.getElementById('st').innerText='LISTENING...';};
 r.onresult=function(e){
  var t=e.results[0][0].transcript;
  document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br>Thinking...';
  fetch('/ask?q='+encodeURIComponent(t)).then(r=>r.json()).then(d=>{
   document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br><b>Jarvis:</b> '+d.answer+'<br><i>Click PLAY to hear</i>';
   speak(d.answer);
  });
 };
 r.start();
}
</script></body></html>
'''

@app.route('/')
def home():
    return PAGE

@app.route('/ask')
def ask():
    q = request.args.get('q','').lower()
    if 'president' in q and 'nigeria' in q:
        return jsonify({"answer": "Boss, President of Nigeria is Bola Ahmed Tinubu. He became president on May 29 2023."})
    if 'know' in q and 'me' in q:
        return jsonify({"answer": "Boss you are Sefiu, my creator in Lagos Nigeria. You are building Vibranium OS, the most advanced Jarvis. You are my boss and I am loyal to you!"})
    if 'who are you' in q:
        return jsonify({"answer": "I am Vibranium OS, your personal Jarvis created by Sefiu in Lagos!"})
    return jsonify({"answer": "You said "+q+". I am Vibranium OS boss, ready for your command!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
