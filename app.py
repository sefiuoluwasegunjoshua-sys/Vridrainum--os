import os, json, urllib.request
from flask import Flask, request, jsonify
app = Flask(__name__)

PAGE = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:10px}button{padding:14px;background:#0ff;color:#000;border:none;border-radius:20px;margin:5px;font-weight:bold}#log{background:#111;color:#0f0;padding:10px;border-radius:10px;text-align:left}audio{width:95%}</style>
</head><body><h2>VIBRANIUM OS v8 FINAL</h2><h4 id="st">Ready - Brain Online</h4>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button onclick="replay()" style="background:#0f0">REPLAY</button>
<div id="log">v8 Final - Ask me anything boss!</div><audio id="aud" controls></audio>
<script>
var synth=window.speechSynthesis; var voices=[]; var enVoice=null; var lastAns='Boss Sefiu I am Vibranium v8 final with ChatGPT brain online!';
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
    key=os.getenv("OPENAI_API_KEY")
    if not key: return jsonify({"answer":"Boss add OPENAI_API_KEY in Render Environment to unlock my full ChatGPT brain!"})
    try:
        url="https://api.openai.com/v1/chat/completions"
        headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"}
        data=json.dumps({"model":"gpt-4o-mini","messages":[{"role":"system","content":"You are Vibranium OS Jarvis, created by Sefiu from Lagos. Keep answers under 25 words for voice. Be loyal and smart."},{"role":"user","content":q}],"max_tokens":100}).encode()
        req=urllib.request.Request(url,data=data,headers=headers)
        with urllib.request.urlopen(req,timeout=15) as resp:
            result=json.loads(resp.read().decode())
            ans=result['choices'][0]['message']['content']
            return jsonify({"answer":ans})
    except Exception as e:
        return jsonify({"answer":f"Brain error boss: {str(e)[:120]}"})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
