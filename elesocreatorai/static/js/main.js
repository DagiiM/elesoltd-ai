const root = document.documentElement;
const body = document.querySelector("body");
const menuIcon = document.querySelector('.header-nav-ul-li__menuicon');
const aside = document.querySelector('aside');
const toggle = document.querySelector('aside .toggle');
const searchBox = document.querySelector('aside .search-box');
const modeSwitch = document.querySelector('aside .mode');
const modeText = document.querySelector('aside .mode .mode-text');

modeSwitch.addEventListener('click', () => {
  body.classList.toggle('dark');
  
  if(body.classList.contains('dark')) {
  modeText.innerText="Light Mode"
  }
  else{
    modeText.innerHTML="Dark Mode"
  }
});

toggle.addEventListener('click', () => {
  aside.classList.toggle('close');
 /*
  const currentWidth = getComputedStyle(root).getPropertyValue('--sidebar-width');
  const newWidth = currentWidth === '250px' ? '88px' : '250px';
  root.style.setProperty('--sidebar-width', newWidth);
  console.log(currentWidth)
  */
});

menuIcon.addEventListener('click', () => {
    aside.classList.toggle('aside-flex');
  });
  
  document.addEventListener('click', (event) => {
    if (aside.classList.contains('aside-flex') && (!aside.contains(event.target) && !menuIcon.contains(event.target))) {
      aside.classList.remove('aside-flex');
    }
    
  });
  


  function showAlert(title, message) {
    let alert = document.querySelector('.alert-text');
    alert.innerText = message;
    const modal = document.querySelector('.modal');
          modal.style.display = 'block';
          setTimeout(() => {
            modal.style.display = 'none';
          }, 1000);
  }