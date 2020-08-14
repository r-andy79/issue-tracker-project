document.addEventListener('DOMContentLoaded', function() {
    const msgContainer = document.querySelector('.message-container')
    if(msgContainer) {
        setTimeout(() => {
            msgContainer.style.display = "none"
        }, 3000);
    }
})