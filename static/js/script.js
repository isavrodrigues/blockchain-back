const btn = document.getElementById('mobileBtn');
const panel = document.getElementById('mobilePanel');
if(btn && panel){
  btn.addEventListener('click', ()=>{
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
  });
}