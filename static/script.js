document.addEventListener('DOMContentLoaded', function() {
    const msgContainer = document.querySelector('.message-container')
    if(msgContainer) {
        setTimeout(() => {
            msgContainer.style.display = "none"
        }, 5000);
    }

    const btn = document.querySelector('.new-ticket')
    btn.addEventListener('mouseover', function() {
        this.textContent = "new ticket"
    })
    btn.addEventListener('mouseout', function() {
        this.innerHTML = '<i class="fas fa-plus"></i>'
    })

    if(window.location.href.includes('/accounts/login/')) {
        btn.style.display = "none";
    }
})