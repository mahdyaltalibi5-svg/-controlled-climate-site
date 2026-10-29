(()=>{'use strict';
const stage=document.querySelector('[data-cc-experience]');if(!stage)return;
const names=['hvac','duct-in','furnace','duct-out','warm','editorial'];
const scenes=names.map(k=>stage.querySelector('[data-cc-layer="'+k+'"]'));
const tunnel=stage.querySelector('.cc-ref__tunnel-img--in'),tunnelOut=stage.querySelector('.cc-ref__tunnel-img--out');
const warmImg=stage.querySelector('.cc-ref__warm-img');
const hvacMedia=stage.querySelector('.cc-inspection__backdrop');
const cold=stage.querySelector('.cc-experience__blend--cold'),hot=stage.querySelector('.cc-experience__blend--warm');
const track=stage.querySelector('.cc-experience__track i'),chapter=stage.querySelector('[data-cc-chapter]');
const dial=stage.querySelector('.cc-ref__dial-progress');
const clamp=x=>Math.min(1,Math.max(0,x));
const ease=(a,b,p)=>{const x=clamp((p-a)/(b-a));return x*x*(3-2*x)};
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
// Each wheel/trackpad gesture advances one deliberately composed scene.
const stops=[0,.262,.393,.515,.641,.793,.942];
const labels=['01 / UNIT ASSEMBLED','02 / EVERY PART, CHECKED','03 / WARM AIR','04 / BLUE FLAME','05 / WARM AIR','06 / WARM. FINALLY.','07 / TURN UP THE HEAT'];
let target=0,pos=0,raf=0,activeStop=0,gestureDelta=0,lastWheel=0,lockedUntil=0;
let settling=false;
window.__ccSceneProgress={hvac:0,furnace:0,room:0};
function range(){return Math.max(1,stage.getBoundingClientRect().height-innerHeight)}
function sectionTop(){return window.scrollY+stage.getBoundingClientRect().top}
function measure(){const r=stage.getBoundingClientRect();target=reduced?0:clamp(-r.top/Math.max(1,r.height-innerHeight));queue()}
function queue(){if(!raf)raf=requestAnimationFrame(draw)}
function set(el,k,v){if(el)el.style[k]=v}
function iris(layer,from,to,p,cx='51%',cy='52%'){
 const r=2+145*ease(from,to,p);if(!layer)return;
 // Soft-edge reveal tied to the machinery's center, not a full-screen crossfade.
 layer.style.setProperty('--cc-iris',r+'vmax');
 layer.style.setProperty('--cc-iris-x',cx);layer.style.setProperty('--cc-iris-y',cy);
}
function draw(){
 raf=0;
 pos+=(target-pos)*.42;
 if(Math.abs(target-pos)<.0002)pos=target;
 const p=pos;
 // Strong full-frame holds at each landing. The first stop NEVER exits the condenser.
 const hvac=1-ease(.288,.378,p);
 const ductIn=ease(.285,.37,p)*(1-ease(.430,.493,p));
 const flame=ease(.427,.492,p)*(1-ease(.560,.625,p));
 const ductOut=ease(.561,.625,p)*(1-ease(.693,.763,p));
 const warm=ease(.695,.758,p)*(1-ease(.831,.905,p));
 const editorial=ease(.839,.92,p);
 const alpha=[hvac,ductIn,flame,ductOut,warm,editorial];
 scenes.forEach((s,i)=>{set(s,'opacity',String(alpha[i]));set(s,'pointerEvents',alpha[i]>.75?'auto':'none')});
 iris(scenes[1],.284,.375,p);
 iris(scenes[2],.428,.493,p);
 iris(scenes[3],.557,.623,p);
 iris(scenes[4],.693,.77,p);
 set(hvacMedia,'transform','scale('+(1+.2*ease(.285,.377,p))+')');
 set(tunnel,'transform','scale('+(1.05+.38*ease(.286,.486,p))+')');
 set(tunnelOut,'transform','scale('+(1.44-.39*ease(.561,.759,p))+')');
 set(warmImg,'transform','scale('+(1.09-.07*ease(.695,.83,p))+')');
 set(cold,'opacity',String(.23*ease(.280,.323,p)*(1-ease(.37,.414,p))));
 set(hot,'opacity',String(.17*ease(.432,.48,p)*(1-ease(.70,.76,p))));
 window.__ccSceneProgress.hvac=ease(0,.253,p);
 window.__ccSceneProgress.furnace=ease(.43,.567,p);
 window.__ccSceneProgress.room=ease(.70,.83,p);
 set(track,'transform','scaleX('+p+')');
 const index=stops.reduce((best,s,i)=>Math.abs(s-p)<Math.abs(stops[best]-p)?i:best,0);
 if(chapter)chapter.textContent=labels[index];
 stage.dataset.activeScene=names[[0,0,1,2,3,4,5][index]];
 stage.dataset.scrollStep=String(index);
 if(Math.abs(target-pos)>.0002)queue();
}
function snap(index){
 activeStop=Math.max(0,Math.min(stops.length-1,index));
 stage.dataset.targetStep=String(activeStop);
 const y=sectionTop()+stops[activeStop]*range();
 window.scrollTo({top:Math.round(y),behavior:'smooth'});
 lockedUntil=performance.now()+850;gestureDelta=0;
}
function inside(){
 const r=stage.getBoundingClientRect();
 return r.top<=18&&r.bottom>=innerHeight-18;
}
function isInput(el){return el&&el.closest&&el.closest('input,textarea,select,[contenteditable="true"],.cc-ref__editorial-page')}
function onWheel(e){
 if(reduced||e.ctrlKey||e.metaKey||!inside()||isInput(e.target))return;
 const direction=Math.sign(e.deltaY);
 if(!direction)return;
 const canStep=direction>0?activeStop<stops.length-1:activeStop>0;
 if(!canStep)return; // allow ordinary page scrolling before/after cinematic story
 e.preventDefault();
 const now=performance.now();
 if(now<lockedUntil)return;
 if(now-lastWheel>220)gestureDelta=0;
 lastWheel=now;
 gestureDelta+=Math.abs(e.deltaY)*(e.deltaMode===1?16:e.deltaMode===2?innerHeight:1);
 if(gestureDelta>=18)snap(activeStop+direction);
}
function onKeys(e){
 if(reduced||!inside()||isInput(e.target)||e.altKey||e.ctrlKey||e.metaKey)return;
 const dir=['ArrowDown','PageDown'].includes(e.key)?1:['ArrowUp','PageUp'].includes(e.key)?-1:0;
 if(!dir)return;
 const n=activeStop+dir;if(n<0||n>=stops.length)return;
 e.preventDefault();snap(n);
}
let touchY=null,touchX=null;
function touchStart(e){if(e.touches.length===1){touchY=e.touches[0].clientY;touchX=e.touches[0].clientX}}
function touchEnd(e){
 if(reduced||touchY===null||!inside()||e.changedTouches.length!==1)return;
 const dy=touchY-e.changedTouches[0].clientY,dx=touchX-e.changedTouches[0].clientX;touchY=null;
 if(Math.abs(dy)<55||Math.abs(dy)<Math.abs(dx)*1.3)return;
 const d=Math.sign(dy),n=activeStop+d;
 if(n>=0&&n<stops.length)snap(n);
}
stage.querySelectorAll('[data-cc-temp-change]').forEach(btn=>btn.addEventListener('click',()=>{
 const n=stage.querySelector('[data-cc-temp]');if(!n)return;
 const temp=Math.max(60,Math.min(80,Number(n.textContent)+Number(btn.dataset.ccTempChange)));
 n.textContent=String(temp);if(dial)dial.style.strokeDasharray=(150+(temp-60)*12)+' 566';
}));
window.addEventListener('wheel',onWheel,{passive:false});
window.addEventListener('keydown',onKeys);
window.addEventListener('touchstart',touchStart,{passive:true});
window.addEventListener('touchend',touchEnd,{passive:true});
window.addEventListener('scroll',measure,{passive:true});
window.addEventListener('resize',measure,{passive:true});
measure();draw();
})();