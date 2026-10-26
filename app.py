function testSpeak(){
 document.getElementById('st').innerText='Speaking...';
 var m=new SpeechSynthesisUtterance('Vibranium OS online Sefiu, working!');
 speechSynthesis.speak(m);
}
function listen(){
 speechSynthesis.cancel();
 speechSynthesis.resume();
 // Unlock trick for Chrome
 var unlock=new SpeechSynthesisUtterance('');
 speechSynthesis.speak(unlock);
 
 var R=window.SpeechRecognition||window.webkitSpeechRecognition;
 var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){alert('Update Chrome');return;}
 var rec=new SR(); rec.lang='en-US';
 rec.onstart=function(){document.getElementById('st').innerText='LISTENING';};r.onstart=function(){ 
  speechSynthesis.resume();
  document.getElementById('st').innerText='LISTENING...';
  document.getElementById('log').innerHTML='Listening... speak now';
};
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
