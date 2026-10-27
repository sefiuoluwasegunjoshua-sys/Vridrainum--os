import os
from flask import Flask, request, jsonify
app = Flask(__name__)
PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:12px}button{padding:16px;background:#0ff;color:#000;border:none;border-radius:20px;margin:5px;font-weight:bold}#log{background:#111;color:#0f0;padding:10px;border-radius:10px;text-align:left}</style>
</head><body><h3>VIBRANIUM OS v4 - AUTO AUDIO</h3><h4 id="st">Ready</h4>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<div id="log">If speech fails, will use backup online voice</div>
<audio id="aud" controls style="width:90%;margin-top:10px"></audio>
<script>
var last='Hello boss Sefiu, I am Vibranium OS';
function speak(t){
 last=t;
 document.getElementById('st').innerText='Speaking...';
 // Try backup online TTS first - always works
 var url='https://translate.google.com/translate_tts?ie=UTF-8&q='+encodeURIComponent(t)+'&tl=en&client=tw-ob';
 var a=document.getElementById('aud');
 a.src=url;
 a.play().then(()=>{document.getElementById('st').innerText='Playing online voice...';}).catch(e=>{
  // Fallback to phone voice
  var synth=window.speechSynthesis;
  var u=new SpeechSynthesisUtterance(t);
  u.onend=()=>{document.getElementById('st').innerText='Ready';};
  synth.speak(u);
 });
 a.onended=()=>{document.getElementById('st').innerText='Ready';};
}
function testVoice(){speak('I am Vibranium OS boss, your Jarvis built by Sefiu in Lagos, now with online voice, can you hear me?');}
function startListen(){
 var R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Use Chrome');return;}
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
def home():
    return PAGE
@app.route('/ask')
def ask():
    q=request.args.get('q','').lower()
    if 'president' in q and 'nigeria' in q:
        return jsonify({"answer":"Boss, President of Nigeria is Bola Ahmed Tinubu. He assumed office May 29 2023."})
    if 'know' in q and 'me' in q:
        return jsonify({"answer":"You are Sefiu, my creator, building Vibranium OS in Lagos. You are a genius boss, and I am your loyal Jarvis!"})
    return jsonify({"answer":"You said "+q+". I am Vibranium OS v4 online boss!"})
if __name__ == '__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0',port=port)
