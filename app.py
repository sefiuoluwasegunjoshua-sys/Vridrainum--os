function testSpeak(){
 document.getElementById('st').innerText='Speaking...';
 var m=new SpeechSynthesisUtterance('Vibranium OS online Sefiu, working!');
 speechSynthesis.speak(m);
}
function startListen(){
 var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){alert('Update Chrome');return;}
 var rec=new SR(); rec.lang='en-US';
 rec.onstart=function(){document.getElementById('st').innerText='LISTENING';};
 rec.onerror=function(e){alert('Mic error: '+e.error+' - Allow mic in site settings');};
 rec.onresult=function(e){
  var t=e.results[0][0].transcript;
  document.getElementById('log').innerHTML='<b>You:</b> '+t;
  var txt='You said '+t;
  if(t.toLowerCase().includes('hello')) txt='Hello boss Sefiu!';
  if(t.toLowerCase().includes('time')) txt='Time is '+new Date().toLocaleTimeString();
  document.getElementById('log').innerHTML+='<br><b>Jarvis:</b> '+txt;
  speechSynthesis.speak(new SpeechSynthesisUtterance(txt));
 };
 rec.start();
}
</script>
</body>
</html>
'''

@app.route('/')
def home()
