import * as THREE from 'https://esm.sh/three@0.170.0';
import {GLTFLoader} from 'https://esm.sh/three@0.170.0/examples/jsm/loaders/GLTFLoader.js';
const section=document.querySelector('[data-hvac-scroll]'),canvas=document.getElementById('cc-real-hvac');
if(section&&canvas){
 const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,powerPreference:'high-performance'});
 renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.75));renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.3;
 const scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(39,1,.1,100);
 camera.position.set(3.7,-5.4,3.2);camera.lookAt(0,0,.8);
 scene.add(new THREE.HemisphereLight(0xdafaff,0x202a31,2.7));
 const key=new THREE.DirectionalLight(0xffffff,3.4);key.position.set(-3,-4,7);scene.add(key);
 const rim=new THREE.DirectionalLight(0x78fff0,2.0);rim.position.set(3,2,5);scene.add(rim);
 let mixer=null,actions=[],duration=6,root=null,p=0,desired=0;
 const loader=new GLTFLoader();
 loader.load('https://d2ol7oe51mr4n9.cloudfront.net/user_3Hv0eSSe1UKKaX8lO1KL1shZHyq/6dc17d0c-8292-45bb-baab-c05eb4fe1f0e.glb',gltf=>{
  root=gltf.scene;scene.add(root);
  // Blender lights and cameras do not control this website's locked composition.
  root.traverse(o=>{if(o.isLight||o.isCamera)o.visible=false;if(o.isMesh){o.castShadow=false;o.receiveShadow=true;o.frustumCulled=false;}});
  mixer=new THREE.AnimationMixer(root);
  actions=gltf.animations.map(clip=>mixer.clipAction(clip).play());
  duration=Math.max(1,...gltf.animations.map(c=>c.duration));
  const bounds=new THREE.Box3().setFromObject(root);const center=bounds.getCenter(new THREE.Vector3());
  // Animations remain relative to the unchanged world position.
  root.position.sub(new THREE.Vector3(center.x,center.y,0));
  section.dataset.modelReady='true';
 },undefined,e=>{console.error('HVAC 3D asset could not be loaded',e);section.dataset.modelReady='false'});
 const labelNodes=[...section.querySelectorAll('.cc-inspection__tech')],intro=section.querySelector('.cc-inspection__intro'),end=section.querySelector('.cc-inspection__final');
 const meter=section.querySelector('.cc-inspection__meter i'),hint=section.querySelector('.cc-inspection__scroll');
 const clamp=x=>Math.max(0,Math.min(1,x)),range=(a,b,x)=>clamp((x-a)/(b-a));
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 function measure(){let r=canvas.getBoundingClientRect();renderer.setSize(Math.max(1,r.width),Math.max(1,r.height),false);camera.aspect=r.width/Math.max(1,r.height);camera.updateProjectionMatrix();}
 function scroll(){const r=section.getBoundingClientRect();desired=reduced?0:clamp(-r.top/Math.max(1,r.height-innerHeight));}
 let visible=true;
 new IntersectionObserver(e=>visible=e[0].isIntersecting,{rootMargin:'250px'}).observe(section);
 function frame(){requestAnimationFrame(frame);if(!visible)return;p+=(desired-p)*.12;
 if(mixer)for(let i=0;i<actions.length;i++)actions[i].time=p*duration;
 if(mixer)mixer.update(0);
 renderer.render(scene,camera);
 const first=1-range(.10,.34,p),last=range(.70,.93,p);
 intro.style.opacity=first;intro.style.pointerEvents=first>.3?'auto':'none';
 end.style.opacity=last;end.style.transform='translateY('+(20*(1-last))+'px)';end.style.pointerEvents=last>.7?'auto':'none';
 labelNodes.forEach((el,i)=>{const t=range(.32+i*.09,.45+i*.09,p)*(1-range(.8,.94,p));el.style.opacity=t;el.style.transform='translateY('+(16*(1-t))+'px)'});
 meter.style.transform='scaleX('+p+')';hint.style.opacity=1-range(.1,.3,p);
 }
 addEventListener('resize',measure,{passive:true});addEventListener('scroll',scroll,{passive:true});measure();scroll();frame();
}
