(()=>{
'use strict';
const section=document.querySelector('[data-cc-experience]');if(!section)return;
const canvas=section.querySelector('.cc-inspection__frames');if(!canvas)return;
const ctx=canvas.getContext('2d',{alpha:false,desynchronized:true});
const intro=section.querySelector('.cc-inspection__intro');
const conclusion=section.querySelector('.cc-inspection__final');
const labels=Array.from(section.querySelectorAll('.cc-inspection__tech'));
const meter=section.querySelector('.cc-inspection__meter i');
const hint=section.querySelector('.cc-inspection__scroll');
const SOURCES=["https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/1fb62658-a822-4408-878c-d1c23c4577b7.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/e7635dff-5fce-42a3-a01d-08dee10eddaf.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6d05fb3e-b6b6-429e-93b9-f9a78b03ba46.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/d097f296-0f35-4275-95f3-b20943d7e7d4.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/c793909b-adfc-4a92-8c3a-4217c721c31a.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/7e50b11b-c53e-40f2-9713-c6c1597c2f2a.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/0d904c33-fed8-4692-a0d6-e9d225563095.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/62a73393-9ed1-47ff-bca0-adc75cdbf984.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/c11d448a-9b64-4f87-b274-745e53025bae.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/011ece6f-ea2c-467a-9614-99789732365e.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/d39e3b5f-c281-4672-a799-ccfe34361fbe.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/3849aac2-d0f3-4d04-89b5-caa62dea5350.webp"];
const FRAME_COUNT=120,FRAMES_PER_SHEET=10,FRAME_W=1920,FRAME_H=1080;
const low=new Image();
let lowLoaded=false,displayed=-1,raf=0,lastRequested=-1,position=0,target=0,lastDrawnSheet=-1,visible=true;
const sheets=new Map();const activeLoads=new Map();const failures=new Set();
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const fade=(a,b,v)=>clamp((v-a)/(b-a));
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const progress=()=>reduced?0:(window.__ccSceneProgress?.hvac ?? 0);
function demand(index){
 if(index<0||index>=SOURCES.length||sheets.has(index)||activeLoads.has(index)||failures.has(index))return;
 const img=new Image();img.crossOrigin='anonymous';img.decoding='async';
 activeLoads.set(index,img);
 img.onload=()=>{activeLoads.delete(index);sheets.set(index,img);purge(Math.floor(position*119/10));displayed=-1;request()};
 img.onerror=()=>{activeLoads.delete(index);failures.add(index);request()};
 img.src=SOURCES[index];
}
function purge(current){
 for(const i of sheets.keys())if(Math.abs(i-current)>4 && i!==lastDrawnSheet){sheets.delete(i)}
}
function resize(){
 const box=canvas.getBoundingClientRect();
 const scale=Math.min(devicePixelRatio||1,2,FRAME_W/Math.max(1,box.width));
 const w=Math.max(1,Math.round(box.width*scale)),h=Math.max(1,Math.round(box.height*scale));
 if(w!==canvas.width||h!==canvas.height){canvas.width=w;canvas.height=h;displayed=-1}
}
function crop(img,sourceX,sourceY,sourceW,sourceH){
 const w=canvas.width,h=canvas.height,s=Math.max(w/sourceW,h/sourceH);
 const width=sourceW*s,height=sourceH*s;
 ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
 ctx.drawImage(img,sourceX,sourceY,sourceW,sourceH,(w-width)*.5,(h-height)*.5,width,height);
}
function textState(p){
 const first=1-fade(.07,.28,p),last=fade(.70,.9,p);
 intro.style.opacity=String(first);
 intro.style.transform='translate3d(0,'+(-18*(1-first))+'px,0)';
 intro.style.pointerEvents=first>.25?'auto':'none';
 conclusion.style.opacity=String(last);
 conclusion.style.transform='translate3d(0,'+(18*(1-last))+'px,0)';
 conclusion.style.pointerEvents=last>.5?'auto':'none';
 labels.forEach((el,i)=>{
   const t=fade(.24+i*.095,.36+i*.095,p)*(1-fade(.83,.96,p));
   el.style.opacity=String(t);el.style.transform='translate3d(0,'+(12*(1-t))+'px,0)';
 });
 meter.style.transform='scaleX('+p+')';
 hint.style.opacity=String(1-fade(.03,.2,p));
}
function render(){
 raf=0;
 target=progress();
 const delta=target-position;
 position+=Math.abs(delta)<.0002?delta:delta*.24;
 const p=position,frame=Math.round(119*p),sheet=Math.floor(frame/10);
 if(lastRequested!==sheet){lastRequested=sheet;for(let k=-2;k<=2;k++)demand(sheet+k)}
 textState(p);
 const aura=section.querySelector('.cc-inspection__aura');if(aura)aura.style.opacity=String(fade(.36,.67,p)*.3);
 if(frame!==displayed){
   const hi=sheets.get(sheet);
   if(hi){resize();const i=frame%10;crop(hi,(i%2)*FRAME_W,Math.floor(i/2)*FRAME_H,FRAME_W,FRAME_H);displayed=frame;lastDrawnSheet=sheet;section.dataset.framesReady='true';section.dataset.frameIndex=String(frame);section.dataset.frameQuality='high';}
   
 }
 if(Math.abs(target-position)>.0002)request();
}
function request(){if(!raf)raf=requestAnimationFrame(render)}


window.addEventListener('scroll',request,{passive:true});
window.addEventListener('resize',()=>{displayed=-1;resize();request()},{passive:true});
for(let i=0;i<3;i++)demand(i);resize();request();
})();