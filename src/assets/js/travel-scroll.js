(()=>{'use strict';
const root=document.querySelector('[data-cc-experience]');
const canvas=root?.querySelector('[data-travel-canvas]');
if(!canvas)return;
const ctx=canvas.getContext('2d',{alpha:false,desynchronized:true});
if(!ctx)return;
const urls=["https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/8b65d3e4-b557-44cb-8f74-ea8242c7e6e4.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/0b41d5c9-6059-4fe2-bf50-0d019dda07ed.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/edc8cf3a-c258-4d51-8d6e-0c3ceccfe18d.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/7c31a5e8-5a11-4fca-8a02-41a1b21e79fb.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/a90e1844-da9a-434b-9d5c-695a5db1c457.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/a08b0217-28c6-4a20-87d4-fd50b8ca924e.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/d15cbc2f-e32a-450e-9357-b0fab108ff96.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/b1b4dd28-7cf9-4664-a6bc-92a956bae071.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/54b4c43e-6b14-4002-8b7c-61f643f03021.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/88568629-3f1e-4765-a7a3-609b6942e949.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/14266651-732b-4b3b-a1b1-ca72c3103b68.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/3f7e4699-813c-40d6-99fa-fed694841bf3.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/20fdbae7-c91b-42a5-abad-6149a9dd364e.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/4d444fad-b37a-4993-87ec-215fd2a6a1ec.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6d37c7ae-5dff-495e-b452-d5667fd6dcc3.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/e8aa7d56-5ea6-45fd-820b-c05a3584347e.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/854f1dc0-4e0c-4e57-973d-ca29aa5a494c.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/a03cb78a-45f3-4d70-b9ca-6f4cae5db8f6.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/fe2932ab-5090-42b7-a450-33ac380176fa.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/949f1f2a-6cee-48e6-9b8a-7c2914f5845c.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/7a394fae-af84-4bd2-a1aa-116b330721dc.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/872786da-470e-48e8-bcf3-394a4671f52c.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/29ca0b73-3690-4315-8406-4e6a77c1c6f2.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/85932aba-239c-4dc7-824c-95a9f0479ca1.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6b113ea8-3208-4925-9957-785f58c5dd21.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/aa879722-93d0-4298-aaf0-89c7bc2f5307.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/55a7abd7-6fe5-4dc6-8f00-b5df119a470b.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/107c63db-02e2-4a83-8bb4-84e7329638a8.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/51a26c5a-b1ba-4bbd-984a-0a405c55b5f4.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/f480a9e9-afb5-4e39-81d1-5fe0b36b5cc1.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/81c81c82-7a75-492d-b884-e836fd9cc78b.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/a99be890-71cd-4cc1-a21a-3df123282ddc.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/30f60793-e5b8-4390-acea-582d29b0f623.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/68e1dbfc-1bd1-4847-b0d5-4ee910756e52.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/012e2d90-12fb-4d11-a48f-d612dbb2663d.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/2f46fc48-e2d1-477f-95d1-552935d010b1.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/e7ffff77-61f4-4231-9846-15e9b11178b9.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/ceacac09-90e3-4e2b-8e44-6c0f97122fb0.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/eddcecda-71fb-4cba-8ff7-c0bbbb43db92.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6901815f-c228-4551-a9f0-79cb0c40b9c9.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/f0f8bbd5-ba66-41c1-938c-e7e90aafa8a5.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/ff94a84d-837f-4ab8-9194-56a09dc6e81f.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/50de4c91-3774-4fd7-8079-d998c9c0842c.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/f1eb1faf-40e1-4866-9c4f-16f50645b67c.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/683864b8-0767-423e-b625-2a3dd4225038.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/f8e337c6-8712-4a40-985a-9e6df24326a0.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/56bd5252-830c-4741-8ace-80d51ddf5dac.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/10212696-f27a-4227-a48f-be9d2419bc65.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/0cb47039-4f48-4274-845a-798a1ffd86ff.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/9cfd4cd1-f749-44f2-b7a6-7642ed3e621f.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/a29cd118-1bb4-4a4c-ab4e-5321cf396dc6.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/676f24c6-2b72-4a7d-9f34-0e4165308216.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/552d4839-d5ad-4b29-a95d-0394a6e6f8c3.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/c0f68129-efda-42dd-9897-77c8b3848463.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/d79e920e-f8d2-4451-9084-57beb39bee27.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/d2ba4038-1c11-428b-99ad-cbd4b0a53c41.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/20b888d8-489f-4565-be9a-8db96a8b0cc6.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/1a289f61-6e9b-4761-a3b3-b9a05486797f.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/79df6b20-b251-44f8-adcb-a116257556e7.webp","https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/ff2ce61d-cfb7-4cb3-b026-feb1e3fc1f6c.webp"];
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const compact=matchMedia('(max-width: 700px), (pointer: coarse)').matches;
const cacheLimit=compact?6:10;
const loadLimit=compact?2:3;
const ready=new Map(),pending=new Map();
let frameShown=-1,drawWidth=0,drawHeight=0,raf=0,seen=0,desired=0,failures=0;
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
function dimensions(){
 const rect=canvas.getBoundingClientRect();
 const scale=Math.min(devicePixelRatio||1,compact?1.2:1.5,1600/Math.max(1,rect.width));
 const w=Math.max(1,Math.round(rect.width*scale)),h=Math.max(1,Math.round(rect.height*scale));
 if(w!==drawWidth||h!==drawHeight){drawWidth=w;drawHeight=h;canvas.width=w;canvas.height=h;frameShown=-1}
}
function currentSheet(){return Math.floor(desired/4)}
function touch(i){const image=ready.get(i);if(image){ready.delete(i);ready.set(i,image)}return image}
function trim(center){
 while(ready.size>cacheLimit){
  let victim=null,best=-1;
  for(const i of ready.keys()){
   if(i===center||i===Math.floor(frameShown/4))continue;
   const distance=Math.abs(i-center);
   if(distance>best){best=distance;victim=i}
  }
  if(victim===null)break;
  ready.delete(victim);
 }
}
function nextPriority(center){
 const direction=Math.sign(desired-frameShown)||1;
 const offsets=direction>=0?[0,1,2,3,-1,4,-2]:[0,-1,-2,-3,1,-4,2];
 for(const off of offsets){const i=center+off;if(i>=0&&i<urls.length&&!ready.has(i)&&!pending.has(i))return i}
 return -1;
}
function pump(){
 const center=currentSheet();
 while(pending.size<loadLimit){
  const i=nextPriority(center);
  if(i<0)break;
  // Restrict preloading to nearby frames, instead of decoding the entire 20 MB sequence.
  const image=new Image();
  image.crossOrigin='anonymous';
  image.decoding='async';
  pending.set(i,image);
  image.onload=()=>{
   const decode=image.decode?image.decode().catch(()=>{}):Promise.resolve();
   decode.then(()=>{
    if(pending.get(i)!==image)return;
    pending.delete(i);ready.set(i,image);trim(currentSheet());
    queue();pump();
   });
  };
  image.onerror=()=>{if(pending.get(i)===image){pending.delete(i);failures++;queue()}};
  image.src=urls[i];
 }
 canvas.dataset.loadedSheets=String(ready.size);
 canvas.dataset.pendingSheets=String(pending.size);
}
function paint(frame){
 const sheet=Math.floor(frame/4);
 const image=touch(sheet);
 if(!image)return false;
 dimensions();
 const tile=frame%4,scale=Math.max(drawWidth/1600,drawHeight/900);
 ctx.imageSmoothingEnabled=true;
 ctx.imageSmoothingQuality='high';
 ctx.drawImage(image,(tile%2)*1600,Math.floor(tile/2)*900,1600,900,
  (drawWidth-1600*scale)/2,(drawHeight-900*scale)/2,1600*scale,900*scale);
 frameShown=frame;
 canvas.dataset.frame=String(frame);
 canvas.dataset.ready='true';
 canvas.dataset.loadedSheets=String(ready.size);
 return true;
}
function run(){
 raf=0;
 const step=root.dataset.targetStep;
 if(step!=='2'){
  // The first frames can be decoded during the exploded HVAC hold.
  if(step==='1')pump();
  return;
 }
 desired=clamp(Math.round((window.__ccJourneyProgress||0)*239),0,239);
 const sheet=currentSheet();
 if(desired!==frameShown&&!paint(desired)){
  // A rapid swipe can outrun the next image download. Show the nearest
  // already-decoded sheet instead of freezing on a distant previous frame.
  let nearest=-1,distance=Infinity;
  for(const i of ready.keys()){const d=Math.abs(i-sheet);if(d<distance){distance=d;nearest=i}}
  if(nearest>=0&&distance<=8){const substitute=clamp(desired,(nearest*4),nearest*4+3);if(substitute!==frameShown)paint(substitute)}
 }
 pump();trim(sheet);
}
function queue(){if(!raf)raf=requestAnimationFrame(run)}
function resize(){frameShown=-1;dimensions();queue()}
window.__ccTravelUpdate=queue;
window.__ccTravelStats=()=>({frame:frameShown,target:desired,loaded:ready.size,pending:pending.size,limit:cacheLimit,errors:failures});
window.addEventListener('resize',resize,{passive:true});
document.addEventListener('visibilitychange',()=>{if(!document.hidden)queue()});
dimensions();
desired=0;pump();
queue();
})();