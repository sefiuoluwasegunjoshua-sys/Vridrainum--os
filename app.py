import os
from flask import Flask, request, jsonify
app = Flask(__name__)

KNOWLEDGE = {
 "president of nigeria": "The President of Nigeria is Bola Ahmed Tinubu, boss. He assumed office May 29 2023.",
 "governor of lagos": "Governor of Lagos is Babajide Sanwo-Olu, boss.",
 "who are you": "I am Vibranium OS, your personal Jarvis, built by you Sefiu in Lagos Nigeria. I am loyal, powerful, and fully online!",
 "what is vibranium": "Vibranium is your personal OS boss, the most advanced Jarvis in Lagos, built by Sefiu!",
}

PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:10px}button{padding:16px 24px;background:#0ff;color:#000;border:none;border-radius:25px;margin:6px;font-weight:bold}#log{background:#111;color:#0f0;padding:12px;border-radius:10px;margin-top:12px;text-align:left;min-height:90px}#play{background:#0f0}</style>
</head><body><h2>VIBRANIUM OS v2</h2><h3 id="st">Ready</h3>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button id="play" onclick="replay()">🔊 PLAY ANSWER</button>
<div id="log">Click HEY JARVIS and ask anything</div>
<script>
var synth=window.speechSynthesis;
var lastAnswer='';
function speak(t){
 lastAnswer=t;
 synth.cancel(); synth.resume();
 var u=new SpeechSynthesisUtterance(t);
 u.rate=0.9; u.volume=1; u.lang='en-US';
 document.getElementById('st').innerText='Speaking...';
 u.onend=function(){document.getElementById('st').innerText='Ready';};
 synth.speak(u);
}
function testVoice(){speak('I am Vibranium OS boss Sefiu, all systems online!');}
function replay(){if(lastAnswer) speak(lastAnswer);}
function startListen(){
 synth.cancel(); synth.resume();
 var R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Use Chrome');return;}
 var r=new R(); r.lang='en-US';
 r.onstart=function(){document.getElementById('st').innerText='LISTENING...'; document.getElementById('log').innerText='Listening boss...';};
 r.onresult=function(e){
  var t=e.results[0][0].transcript;
  document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br>Thinking...';
  fetch('/ask?q='+encodeURIComponent(t))
   .then(res=>res.json())
   .then(data=>{
     var a=data.answer;
     document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br><b>Jarvis:</b> '+a+'<br><small>Click 🔊 PLAY ANSWER to hear</small>';
     speak(a);
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
    for k,v in KNOWLEDGE.items():
        if k in q:
            return jsonify({"answer": v})
    if "president" in q and "nigeria" in q:
        return jsonify({"answer": KNOWLEDGE["president of nigeria"]})
    if "time" in q:
        from datetime import datetime
        return jsonify({"answer": f"Boss, time is {datetime.now().strftime('%I:%M %p')} in Lagos"})
    return jsonify({"answer": f"You asked: {q}. I am Vibranium OS boss, I heard you. As your Jarvis, I am still learning. President of Nigeria is Bola Ahmed Tinubu. How can I help further boss?"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
