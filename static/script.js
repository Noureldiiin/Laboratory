document.addEventListener('DOMContentLoaded', function() {
    animateWelcomeMessage();
    animateButtonHoverEffect('.patient-list-btn');
    animateButtonHoverEffect('.add-patient-btn');
});

function animateButtonHoverEffect(buttonSelector) {
    let button = document.querySelector(buttonSelector);

    button.addEventListener('mouseenter', function() {
        anime({
            targets: button,
            scale: 1.1,
            duration: 300,
            easing: 'easeInOutQuad'
        });
    });

    button.addEventListener('mouseleave', function() {
        anime({
            targets: button,
            scale: 1,
            duration: 300,
            easing: 'easeInOutQuad'
        });
    });
}

function redirectToPatientList() {
    window.location.href = '/patient_list';
}

function redirectToAddPatient() {
    window.location.href = '/add_patient';
}

function animateWelcomeMessage() {
    let welcomeMessage = document.querySelector('h1');
    let chars = welcomeMessage.innerText.split('');
    welcomeMessage.innerHTML = '';
    
    chars.forEach(char => {
        let charSpan = document.createElement('span');
        charSpan.innerText = char;
        charSpan.style.opacity = Math.random();
        welcomeMessage.appendChild(charSpan);
    });

    anime.timeline({loop: false})
        .add({
            targets: 'h1 span',
            translateY: [-20, 0],
            opacity: [0, 1],
            easing: 'easeOutExpo',
            duration: 1500,
            delay: (el, i) => 50 * i
        });
}
