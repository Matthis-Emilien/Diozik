/*
TEXT
*/

const container= document.querySelectorAll('.box');

window.addEventListener('load', () => {
    
    const TL = gsap.timeline({paused = true});
    
    TL.staggerFrom(box,1, {top: -50, opacity: 0, ease: "power2.out"}, 0.3)
    
    TL.play()
})

