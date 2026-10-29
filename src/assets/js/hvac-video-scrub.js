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
const SOURCES=["https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/65dfcf79-55b4-4428-9025-e4dc6947460b.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/837ab079-a508-472d-bdf1-f4457aef873b.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/5e406566-47e7-446e-9b2f-707aabcc746c.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/bf30be72-9467-479e-a1d0-b218ad4aa4bd.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/5fb5cf40-2ff4-47d1-ac25-81e3ba84d439.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/ceb973ff-9424-4728-a356-5093af5c8d26.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6cf435ab-55ef-4be7-a596-07214392128b.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/24e767de-e3a9-40b6-a408-58b6c3ca35b8.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/3eef4ab0-a172-4add-ab33-852d027640dd.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/03de3ceb-1629-41c7-bf92-fc42ea0dda9e.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/37efd023-89c9-48da-928f-fd7dca296d33.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6f14e286-9ec6-471c-933f-01bcc6aebd35.webp"];
const FRAME_COUNT=120,FRAMES_PER_SHEET=10,FRAME_W=1600,FRAME_H=900;
const low=new Image();low.crossOrigin='anonymous';
low.src='https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/aeb26cea-ec86-4bf3-b1f2-9e53e2b4e00c.jpg';
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
 const scale=Math.min(devicePixelRatio||1,1.5,FRAME_W/Math.max(1,box.width));
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
   else if(displayed<0&&lowLoaded){resize();const i=Math.round(frame*79/119);crop(low,(i%8)*640,Math.floor(i/8)*360,640,360);displayed=frame;section.dataset.framesReady='true';section.dataset.frameIndex=String(frame);section.dataset.frameQuality='preview';}
 }
 if(Math.abs(target-position)>.0002)request();
}
function request(){if(!raf)raf=requestAnimationFrame(render)}

low.onload=()=>{lowLoaded=true;request()};low.onerror=()=>request();
window.addEventListener('scroll',request,{passive:true});
window.addEventListener('resize',()=>{displayed=-1;resize();request()},{passive:true});
for(let i=0;i<4;i++)demand(i);resize();request();
})();