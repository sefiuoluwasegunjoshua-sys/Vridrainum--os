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
