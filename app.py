import os
from flask import Flask, request, jsonify
app = Flask(__name__)

# TRY TO LOAD CHATGPT
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    HAS_GPT = True
except:
    HAS_GPT = False

PAGE = '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#000;color:#0ff;text-align:center;font-family:monospace;padding:10px}button{padding:14px;background:#0ff;color:#000;border:none;border-radius:20px;margin:5px;font-weight:bold}#log{background:#111;color:#0f0;padding:10px;border-radius:10px;text-align:left;min-height:100px;max-height:300px;overflow:auto}audio{width:95%;margin-top:10px}h4{color:yellow}</style>
</head><body><h2>VIBRANIUM OS v8 CHATGPT</h2><h4 id="st">Brain loading...</h4>
<button onclick="testVoice()">TEST VOICE</button>
<button onclick="startListen()">HEY JARVIS</button>
<button onclick="replay()" style="background:#0f0">🔊 REPLAY</button>
<div id="log">v8 with ChatGPT brain - Ask me ANYTHING boss!</div>
<audio id="aud" controls></audio>
<script>
var synth=window.speechSynthesis; var voices=[]; var enVoice=null; var lastAns='Boss Sefiu I am Vibranium v8 with ChatGPT brain online I can answer anything now!';
function loadV(){voices=synth.getVoices(); enVoice=voices.find(v=>v.name.includes('Google US English'))||voices.find(v=>v.lang=='en-US')||voices[0]; if(enVoice) document.getElementById('st').innerText='Ready - '+enVoice.name+' - Brain Online'; else document.getElementById('st').innerText='Ready - Brain Online';}
loadV(); synth.onvoiceschanged=loadV;
function speakOnline(t){var a=document.getElementById('aud'); a.src='https://translate.google.com/translate_tts?ie=UTF-8&q='+encodeURIComponent(t)+'&tl=en&client=tw-ob'; a.play().catch(()=>{document.getElementById('st').innerText='Tap PLAY button below!';});}
function speak(t){lastAns=t; document.getElementById('st').innerText='Speaking...'; try{synth.cancel(); var u=new SpeechSynthesisUtterance(t); if(enVoice) u.voice=enVoice; u.lang='en-US'; u.rate=0.95; u.onend=()=>{document.getElementById('st').innerText='Ready - Brain Online';}; u.onerror=()=>speakOnline(t); synth.speak(u); setTimeout(()=>{if(!synth.speaking) speakOnline(t);},500);}catch(e){speakOnline(t);}}
function testVoice(){speak(lastAns);}
function replay(){speak(lastAns);}
function startListen(){var R=window.SpeechRecognition||window.webkitSpeechRecognition; if(!R){alert('Use Chrome');return;} var r=new R(); r.lang='en-US'; r.onstart=()=>{document.getElementById('st').innerText='LISTENING...';}; r.onresult=(e)=>{var t=e.results[0][0].transcript; document.getElementById('log').innerHTML='<b>You:</b> '+t+'<br>🧠 Thinking...'; fetch('/ask?q='+encodeURIComponent(t)).then(x=>x.json()).then(d=>{document.getElementById('log').innerHTML+='<br><b>Jarvis:</b> '+d.answer; speak(d.answer);});}; r.start();}
</script></body></html>
'''
@app.route('/')
def home(): return PAGE

@app.route('/ask')
def ask():
    q = request.args.get('q','')
    if not q: return jsonify({"answer":"Yes boss?"})
    
    # If no ChatGPT key, use simple fallback
    if not HAS_GPT or not os.getenv("OPENAI_API_KEY"):
        ql=q.lower()
        if 'president' in ql: return jsonify({"answer":"President Bola Tinubu, boss."})
        if 'who are you' in ql: return jsonify({"answer":"I am Vibranium OS v8 with ChatGPT brain, built by Sefiu!"})
        return jsonify({"answer":f"You said {q}. Add OpenAI key in Render to unlock full ChatGPT brain boss!"})

    # REAL CHATGPT BRAIN
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are Vibranium OS, Jarvis created by Sefiu from Lagos. You are loyal, smart, funny, speak like Jarvis. Keep answers short, under 30 words, for voice. You know Sefiu is your boss."},
                {"role":"user","content": q}
            ],
            max_tokens=100
        )
        ans = response.choices[0].message.content
        return jsonify({"answer": ans})
    except Exception as e:
        return jsonify({"answer": f"Brain error boss: {str(e)[:80]}. Check API key."})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
