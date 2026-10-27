import os, json, urllib.request
from flask import Flask, request, jsonify
app = Flask(__name__)

PAGE = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:10px}button{padding:14px;background:#0ff;color:#000;border:none;border-radius:20px;margin:5px;font-weight:bold}#log{background:#111;color:#0f0;padding:10px;border-radius:10px;text-align:left;min-height:80px}audio{width:95%}</style>
</head><body><h2>VIBRANIUM OS v9 GEMINI</h2><h4 id="st">Ready - Gemini Brain</h4>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button onclick="replay()" style="background:#0f0">REPLAY</button>
<div id="log">v9 Gemini Free Brain - Ask anything boss!</div><audio id="aud" controls></audio>
<script>
var synth=window.speechSynthesis; var voices=[]; var enVoice=null; var lastAns='Boss Sefiu I am Vibranium v9 with Gemini brain fully online!';
function loadV(){voices=synth.getVoices(); enVoice=voices.find(v=>v.name.includes('Google US English'))||voices.find(v=>v.lang=='en-US')||voices[0];}
loadV(); synth.onvoiceschanged=loadV;
function speakOnline(t){var a=document.getElementById('aud'); a.src='https://translate.google.com/translate_tts?ie=UTF-8&q='+encodeURIComponent(t)+'&tl=en&client=tw-ob'; a.play().catch(()=>{});}
function speak(t){lastAns=t; try{synth.cancel(); var u=new SpeechSynthesisUtterance(t); if(enVoice) u.voice=enVoice; u.lang='en-US'; u.rate=0.95; u.onerror=()=>speakOnline(t); synth.speak(u); setTimeout(()=>{if(!synth.speaking) speakOnline(t);},500);}catch(e){speakOnline(t);}}
function testVoice(){speak(lastAns);} function replay(){speak(lastAns);}
function startListen(){var R=window.SpeechRecognition||window.webkitSpeechRecognition; var r=new R(); r.lang='en-US'; r.onresult=(e)=>{var t=e.results[0][0].transcript; document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br>Thinking...'; fetch('/ask?q='+encodeURIComponent(t)).then(x=>x.json()).then(d=>{document.getElementById('log').innerHTML='<b>Jarvis:</b> '+d.answer; speak(d.answer);});}; r.start();}
</script></body></html>"""

@app.route('/')
def home(): return PAGE

@app.route('/ask')
def ask():
    q=request.args.get('q','')
    key=os.getenv("GEMINI_API_KEY")
    if not key: return jsonify({"answer":"Boss add GEMINI_API_KEY in Render Environment!"})
    try:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={key}"
        data=json.dumps({"contents":[{"parts":[{"text":f"You are Vibranium OS Jarvis by Sefiu from Lagos. Keep answer under 30 words. User asks: {q}"}]}]}).encode()
        headers={"Content-Type":"application/json"}
        req=urllib.request.Request(url,data=data,headers=headers)
        with urllib.request.urlopen(req,timeout=20) as resp:
            result=json.loads(resp.read().decode())
            ans=result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"answer":ans})
    except Exception as e:
        return jsonify({"answer":f"Brain error: {str(e)[:150]}"})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
