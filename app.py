import os
from flask import Flask, request, jsonify
app = Flask(__name__)
PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:10px}button{padding:14px;background:#0ff;color:#000;border:none;border-radius:20px;margin:5px;font-weight:bold}#log{background:#111;color:#0f0;padding:10px;border-radius:10px;text-align:left;min-height:80px}audio{width:90%;margin-top:10px}</style>
</head><body><h2>VIBRANIUM OS v7 FINAL FIX</h2><h4 id="st">Tap TEST to unlock audio</h4>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button onclick="replay()" style="background:#0f0">🔊 REPLAY</button>
<div id="log">v7 has phone + internet voice</div>
<audio id="aud" controls></audio>
<script>
var synth=window.speechSynthesis;
var voices=[]; var enVoice=null; var lastAns='Boss Sefiu I am Vibranium v7 ultra stable and I will always talk!';
function loadV(){voices=synth.getVoices(); enVoice=voices.find(v=>v.name.includes('Google US English'))||voices.find(v=>v.lang=='en-US')||voices[0]; if(enVoice) document.getElementById('st').innerText='Ready - '+enVoice.name; else document.getElementById('st').innerText='Ready - voices:'+voices.length;}
loadV(); synth.onvoiceschanged=loadV;
// unlock audio on first tap
function unlock(){var a=document.getElementById('aud'); a.play().then(()=>{a.pause();}).catch(()=>{}); synth.resume();}
function speakOnline(t){
 var a=document.getElementById('aud');
 var url='https://translate.google.com/translate_tts?ie=UTF-8&q='+encodeURIComponent(t)+'&tl=en&client=tw-ob&ttsspeed=1';
 a.src=url; a.play().then(()=>{document.getElementById('st').innerText='Playing ONLINE voice...';}).catch(e=>{document.getElementById('st').innerText='Audio blocked, tap again';});
 a.onended=()=>{document.getElementById('st').innerText='Ready';};
}
function speak(t){
 lastAns=t; unlock();
 document.getElementById('st').innerText='Speaking...';
 try{
  synth.cancel();
  var u=new SpeechSynthesisUtterance(t);
  if(enVoice) u.voice=enVoice; u.lang='en-US'; u.rate=0.95;
  u.onend=()=>{document.getElementById('st').innerText='Ready';};
  u.onerror=()=>{console.log('phone voice failed, using online'); speakOnline(t);};
  synth.speak(u);
  setTimeout(()=>{if(synth.speaking==false && synth.pending==false){speakOnline(t);}},500);
 }catch(e){speakOnline(t);}
}
function testVoice(){speak(lastAns);}
function replay(){speak(lastAns);}
function startListen(){
 var R=window.SpeechRecognition||window.webkitSpeechRecognition; if(!R){alert('Use Chrome');return;}
 var r=new R(); r.lang='en-US';
 r.onstart=()=>{document.getElementById('st').innerText='LISTENING...';};
 r.onresult=(e)=>{
  var t=e.results[0][0].transcript;
  document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br>Thinking...';
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
@app.route('/ask')
def ask():
    q=request.args.get('q','').lower()
    if 'president' in q: return jsonify({"answer":"Boss Sefiu, President of Nigeria is Bola Ahmed Tinubu."})
    if 'know' in q and 'me' in q: return jsonify({"answer":"You are Sefiu, my creator from Lagos, boss of Vibranium OS!"})
    if 'who are you' in q: return jsonify({"answer":"I am Vibranium OS v7, your loyal Jarvis, built by Sefiu, with double voice engine, I will always talk!"})
    return jsonify({"answer":f"You said {q}. I am v7 ultra stable boss!"})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
