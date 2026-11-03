if(!matchMedia('(prefers-reduced-motion: reduce)').matches){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:.12});document.querySelectorAll('.reveal').forEach(el=>io.observe(el));}else document.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'));
const nav=document.querySelector('.nav'),home=document.body.classList.contains('home');
const tint=()=>nav.classList.toggle('solid',!home||scrollY>innerHeight*.7);tint();addEventListener('scroll',tint,{passive:true});

// intro once per session; afterwards the logo curtain is skipped
if(home){const seen=sessionStorage.getItem('intro');if(seen)document.body.classList.add('seen');else{sessionStorage.setItem('intro','1');const i=document.getElementById('intro');if(i)setTimeout(()=>i.remove(),2000);}}
