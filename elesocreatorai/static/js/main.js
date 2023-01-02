
const menuIcon = document.querySelector('.header-nav-ul-li__menuicon');
const aside = document.querySelector('aside');

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