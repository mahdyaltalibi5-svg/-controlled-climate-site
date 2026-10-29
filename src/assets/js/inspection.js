/* Controlled Climate interactive scroll study. No third-party requests. */
(() => {
const section=document.querySelector('[data-hvac-scroll]');if(!section)return;
const canvas=section.querySelector('canvas'),ctx=canvas.getContext('2d');
const intro=section.querySelector('.cc-inspection__intro'),final=section.querySelector('.cc-inspection__final');
const labels=[...section.querySelectorAll('.cc-inspection__tech')],glow=section.querySelector('.cc-inspection__halo');
const meter=section.querySelector('.cc-inspection__meter i'),scroll=section.querySelector('.cc-inspection__scroll');
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let progress=0,target=0,w=0,h=0,dpr=1,raf=0,visible=true;
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v)),smooth=(a,b,v)=>{v=clamp((v-a)/(b-a));return v*v*(3-2*v)};
function resize(){const r=canvas.getBoundingClientRect();w=Math.max(1,r.width);h=Math.max(1,r.height);dpr=Math.min(2,window.devicePixelRatio||1);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0)}
function line(points,color,width=1,blur=0){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineJoin='round';ctx.lineCap='round';ctx.shadowColor=color;ctx.shadowBlur=blur;ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke();ctx.restore()}
function poly(points,fill,stroke,width=1){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke()}}
function round(x,y,width,height,r,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,width,height,r);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke()}}
function render(){
ctx.clearRect(0,0,w,h);
const u=Math.min(w/500,h/560)*.88,cy=h*.49,cx=w*.51;
ctx.save();ctx.translate(cx,cy);ctx.scale(u,u);
const lift=smooth(.17,.76,progress),opened=smooth(.24,.66,progress),show=smooth(.35,.72,progress),g=smooth(.35,.6,progress);
const mint='rgba(100,255,220,'+(.12+.73*g)+')';
// shadow and bottom pad
ctx.save();ctx.filter='blur(20px)';round(-153,167,306,25,16,'rgba(0,0,0,.67)');ctx.restore();
poly([[-146,146],[83,146],[151,98],[-79,98]],'#505b5e','#809092',2);
poly([[-146,146],[-146,164],[83,164],[83,146]],'#303e41');
poly([[83,146],[151,98],[151,117],[83,164]],'#263338');
function compressor(){ctx.save();ctx.translate(-13,20);round(-52,2,104,126,20,'#1a2427','#374145');ctx.fillStyle='#273236';ctx.beginPath();ctx.ellipse(0,5,52,19,0,0,Math.PI*2);ctx.fill();line([[-30,17],[-30,113]],'#4f5d61',3);line([[35,14],[35,110]],'#090f12',3);round(-57,115,114,15,5,'#263238');ctx.restore()}
compressor();
// right electrical assembly
ctx.save();ctx.translate(80+show*25,21-show*13);round(-14,-4,69,115,4,'#717f80','#d7dad1');round(-7,3,55,103,3,'#263436','#3e5653');for(let i=0;i<8;i++){round(0+i%3*16,10+Math.floor(i/3)*25,11,18,2,i%2?'#b79b64':'#161e23');}ctx.restore();
// copper tubing rising into coil
for(let i=0;i<4;i++){const x=-22+i*19;line([[x,31],[x,4],[x+13,-11],[x+43,-11]],'#be7844',5);line([[x,30],[x,4],[x+13,-11],[x+43,-11]],'#efb77c',1)}
// black radiator block at midheight, lifts as a single assembly
ctx.save();ctx.translate(0,-lift*101);
poly([[-151,-125],[88,-125],[149,-156],[-91,-156]],'#4b5458','#8f9997',2);
poly([[88,-125],[149,-156],[149,0],[88,30]],'#101b20','#667779',2);
round(-151,-125,239,155,3,'#131c20','#627276');
// dense heat-exchanger fins
for(let i=0;i<35;i++){const x=-146+i*6.8;line([[x,-120],[x,25]],i%2?'#303f40':'#536264',1)}
for(let i=0;i<15;i++){const y=-111+i*9.5;line([[-146,y],[84,y]],'#ba7a4c',4);line([[-146,y-1],[84,y-1]],'#f3b982',1)}
for(let i=0;i<14;i++){const y=-111+i*9.5;ctx.beginPath();ctx.arc(84,y+4.5,4.5,-Math.PI/2,Math.PI/2);ctx.strokeStyle='#d58e54';ctx.lineWidth=3;ctx.stroke()}
if(g){line([[-151,-125],[88,-125],[88,30],[-151,30],[-151,-125]],mint,2,14);line([[88,-125],[149,-156],[149,0],[88,30]],mint,2,12)}
ctx.restore();
// gray cabinet grille - retract sideways, keep rounded frame
function front(offset){ctx.save();ctx.translate(offset,0);round(-160,-167,255,315,13,'#495256','#909e9d');round(-151,-158,237,292,5,'#10191d');for(let i=0;i<34;i++){let x=-145+i*6.9;line([[x,-153],[x,130]],i%3?'#6d7878':'#4c585b',2)}round(-160,-167,12,315,5,'#7d8989');round(80,-167,15,315,5,'#788485');ctx.restore()}
function right(offset){ctx.save();ctx.translate(offset,0);poly([[95,-167],[157,-209],[157,96],[95,148]],'#465256','#a3afac',2);for(let i=0;i<28;i++){let x=100+i*2.0;line([[x,-160-(x-95)*.64],[x,140-(x-95)*.65]],'#7a898a',1.6)}ctx.restore()}
front(-opened*320);right(opened*320);
// top shroud and fan, rises above and exits frame
ctx.save();ctx.translate(0,-lift*360);
poly([[-160,-168],[95,-168],[160,-210],[-95,-210]],'#7e898a','#d8dddd',3);
poly([[-160,-168],[-160,-186],[-95,-228],[-95,-210]],'#556366');
poly([[95,-168],[160,-210],[160,-225],[95,-182]],'#4a595b');
ctx.save();ctx.transform(1,-.13,0,.48,0,-199);
ctx.beginPath();ctx.ellipse(0,0,116,90,0,0,Math.PI*2);ctx.fillStyle='#111a1e';ctx.fill();ctx.strokeStyle='#9ba6a4';ctx.lineWidth=9;ctx.stroke();
for(let i=0;i<5;i++){ctx.save();ctx.rotate(i*2*Math.PI/5+.15);poly([[0,-7],[30,-14],[85,-22],[76,6],[27,16]],'#657476','#a6b6b4',2);ctx.restore()}
for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(0,0,18+i*20,13+i*15,0,0,Math.PI*2);ctx.strokeStyle='#a4b2b0';ctx.lineWidth=1.5;ctx.stroke()}
ctx.beginPath();ctx.arc(0,0,16,0,Math.PI*2);ctx.fillStyle='#788787';ctx.fill();
ctx.restore();
if(g)line([[-160,-168],[-95,-210],[160,-210],[95,-168],[-160,-168]],mint,3,18);
ctx.restore();
if(g)line([[-150,147],[83,147],[151,98]],mint,2,15);
ctx.restore();
glow.style.opacity=String(g*.95);
intro.style.opacity=String(1-smooth(.08,.30,progress));intro.style.transform='translateY('+(-35*smooth(.08,.30,progress))+'px)';
intro.style.pointerEvents=progress>.3?'none':'auto';
labels.forEach((el,i)=>{let a=smooth(.28+i*.09,.43+i*.1,progress)*(1-smooth(.82,.95,progress));el.style.opacity=String(a);el.style.transform='translateY('+(15*(1-a))+'px)'});
let fin=smooth(.76,.94,progress);final.style.opacity=String(fin);final.style.transform='translateY('+(26*(1-fin))+'px)';final.style.pointerEvents=fin>.8?'auto':'none';
scroll.style.opacity=String(1-smooth(.09,.3,progress));meter.style.transform='scaleX('+progress+')';
}
function update(){if(reduced){progress=0;render();return}let rect=section.getBoundingClientRect();target=clamp(-rect.top/Math.max(1,rect.height-innerHeight));}
function tick(){if(!visible){raf=0;return}progress+=(target-progress)*.17;if(Math.abs(target-progress)<.0004)progress=target;render();if(progress!==target)raf=requestAnimationFrame(tick);else raf=0}
function request(){update();if(!raf)raf=requestAnimationFrame(tick)}
resize();request();window.addEventListener('resize',()=>{resize();request()},{passive:true});window.addEventListener('scroll',request,{passive:true});
if('IntersectionObserver'in window){const io=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)request()},{rootMargin:'150px'});io.observe(section)}
})();