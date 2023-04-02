function getRandomPosition() {
    const min = 25;
    const max = 60;
    return {
      x: Math.floor(Math.random() * (max - min) + min) + '%',
      y: Math.floor(Math.random() * (max - min) + min) + '%',
    };
  }
  
  function animateEye() {
    const pupil = document.querySelector('.pupil');
    if (pupil) {
      const newPosition = getRandomPosition();
      pupil.style.top = newPosition.y;
      pupil.style.left = newPosition.x;
    }
  }
  
  // If the user is not logged in, start the eye animation
  if (!document.querySelector('body').classList.contains('logged-in')) {
    setInterval(animateEye, 2000);
  }
  