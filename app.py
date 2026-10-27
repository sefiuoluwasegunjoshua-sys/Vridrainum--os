browser boss');return;}
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
