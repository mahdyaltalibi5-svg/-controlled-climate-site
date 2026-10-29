(()=>{'use strict';
const stage=document.querySelector('[data-cc-experience]');if(!stage)return;
const scenes=['hvac','duct-in','furnace','duct-out','warm','editorial'].map(k=>stage.querySelector('[data-cc-layer="'+k+'"]'));
const cold=stage.querySelector('.cc-experience__blend--cold'),hot=stage.querySelector('.cc-experience__blend--warm');
const tunnel=stage.querySelector('.cc-ref__tunnel-img--in'),tunnelOut=stage.querySelector('.cc-ref__tunnel-img--out'),warmImg=stage.querySelector('.cc-ref__warm-img');
const track=stage.querySelector('.cc-experience__track i'),chapter=stage.querySelector('[data-cc-chapter]');
const dial=stage.querySelector('.cc-ref__dial-progress');
const clamp=n=>Math.min(1,Math.max(0,n));
const ease=(a,b,p)=>{const q=clamp((p-a)/(b-a));return q*q*(3-2*q)};
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
let target=0,pos=0,raf=0;
window.__ccSceneProgress={hvac:0,furnace:0,room:0};
function measure(){const r=stage.getBoundingClientRect();target=reduce?0:clamp(-r.top/Math.max(1,r.height-innerHeight));queue();}
const set=(el,key,value)=>{if(el)el.style[key]=value};
function draw(){
 raf=0;
 pos+=(target-pos)*.19;
 if(Math.abs(target-pos)<.00015)pos=target;
 const p=pos;
 // Continuous HVAC -> duct -> flame -> duct -> home sequence. Each duct uses the same image.
 const ductIn=ease(.205,.278,p)*(1-ease(.348,.406,p));
 const flame=ease(.358,.428,p)*(1-ease(.535,.606,p));
 const ductOut=ease(.551,.620,p)*(1-ease(.685,.747,p));
 const room=ease(.704,.770,p)*(1-ease(.845,.904,p));
 const editorial=ease(.86,.928,p);
 const alpha=[1-ease(.218,.29,p),ductIn,flame,ductOut,room,editorial];
 scenes.forEach((el,i)=>{set(el,'opacity',String(alpha[i]));set(el,'pointerEvents',alpha[i]>.7?'auto':'none')});
 // The same center-of-frame duct appears on either side of ignition.
 set(tunnel,'transform','scale('+(1.02+.63*ease(.21,.405,p))+')');
 set(tunnelOut,'transform','scale('+(1.65-.60*ease(.56,.74,p))+')');
 set(scenes[2],'clipPath','circle('+(3+170*ease(.36,.44,p))+'% at 50% 50%)');
 set(scenes[3],'clipPath','circle('+(3+170*ease(.55,.63,p))+'% at 50% 50%)');
 set(scenes[4],'clipPath','circle('+(2+170*ease(.705,.778,p))+'% at 50% 50%)');
 set(warmImg,'transform','scale('+(1.095-.085*ease(.70,.83,p))+')');
 set(cold,'opacity',String(.24*ease(.18,.25,p)*(1-ease(.29,.36,p))));
 set(hot,'opacity',String(.25*ease(.36,.42,p)*(1-ease(.68,.75,p))));
 window.__ccSceneProgress.hvac=ease(0,.27,p);
 window.__ccSceneProgress.furnace=ease(.395,.565,p);
 window.__ccSceneProgress.room=ease(.70,.86,p);
 set(track,'transform','scaleX('+p+')');
 if(chapter)chapter.textContent=p<.24?'01 / EVERY PART':p<.39?'02 / WARM AIR':p<.58?'03 / BLUE FLAME':p<.73?'04 / WARM AIR':p<.88?'05 / WARM. FINALLY.':'06 / TURN UP THE HEAT';
 stage.dataset.activeScene=p<.25?'cooling':p<.39?'duct-entry':p<.58?'ignition':p<.73?'duct-exit':p<.88?'living-room':'thermostat';
 if(Math.abs(target-pos)>.00015)queue();
}
function queue(){if(!raf)raf=requestAnimationFrame(draw)}
stage.querySelectorAll('[data-cc-temp-change]').forEach(btn=>btn.addEventListener('click',()=>{
 const n=stage.querySelector('[data-cc-temp]');if(!n)return;
 const temp=Math.max(60,Math.min(80,Number(n.textContent)+Number(btn.dataset.ccTempChange)));
 n.textContent=String(temp);
 if(dial)dial.style.strokeDasharray=(150+(temp-60)*12)+' 566';
}));
window.addEventListener('scroll',measure,{passive:true});
window.addEventListener('resize',measure,{passive:true});
measure();draw();
})();