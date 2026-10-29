(()=>{'use strict';
const stage=document.querySelector('[data-cc-experience]');if(!stage)return;
const scenes=['hvac','furnace','tunnel','warm','editorial'].map(k=>stage.querySelector('[data-cc-layer="'+k+'"]'));
const cold=stage.querySelector('.cc-experience__blend--cold'),hot=stage.querySelector('.cc-experience__blend--warm');
const tunnel=stage.querySelector('.cc-ref__tunnel-img'),warmImg=stage.querySelector('.cc-ref__warm-img');
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
 // Five measured beats matching the reference's progression, with purposeful overlaps.
 const hvacExit=ease(.215,.305,p);
 const furnaceIn=ease(.225,.305,p),furnaceOut=ease(.45,.525,p);
 const tunnelIn=ease(.452,.514,p),tunnelOut=ease(.545,.612,p);
 const warmIn=ease(.555,.625,p),warmOut=ease(.735,.82,p);
 const editorialIn=ease(.755,.845,p);
 const alphas=[1-hvacExit,furnaceIn*(1-furnaceOut),tunnelIn*(1-tunnelOut),warmIn*(1-warmOut),editorialIn];
 scenes.forEach((s,i)=>{if(!s)return;set(s,'opacity',String(alphas[i]));set(s,'pointerEvents',alphas[i]>.7?'auto':'none')});
 // Reveal glowing tunnel through an expanding circular aperture, not a blanket dissolve.
 const size=4+180*ease(.465,.545,p);
 set(scenes[2],'clipPath','circle('+size+'% at 50% 50%)');
 // Warm living room emerges through the bright vanishing point of the tunnel.
 const roomRadius=2+175*ease(.565,.645,p);
 set(scenes[3],'clipPath','circle('+roomRadius+'% at 50% 50%)');
 set(tunnel,'transform','scale('+(1.18+.5*ease(.46,.60,p))+')');
 set(warmImg,'transform','scale('+(1.095-.085*ease(.575,.73,p))+')');
 set(cold,'opacity',String(.35*ease(.18,.24,p)*(1-ease(.29,.35,p))));
 set(hot,'opacity',String(.38*ease(.46,.51,p)*(1-ease(.58,.65,p))));
 // 0..1 play each clip during its visual ownership, not during a second independent scroll timeline.
 window.__ccSceneProgress.hvac=ease(0,.265,p);
 window.__ccSceneProgress.furnace=ease(.255,.49,p);
 window.__ccSceneProgress.room=ease(.59,.75,p);
 set(track,'transform','scaleX('+p+')');
 if(chapter)chapter.textContent=p<.25?'01 / EVERY PART':p<.51?'02 / BLUE FLAME':p<.61?'03 / WARM AIR':p<.79?'04 / WARM. FINALLY.':'05 / TURN UP THE HEAT';
 stage.dataset.activeScene=['cooling','ignition','duct','living-room','thermostat'][p<.27?0:p<.5?1:p<.6?2:p<.8?3:4];
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