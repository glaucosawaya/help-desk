document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById('anexoModal');
    const modalImg = document.getElementById('imagem-modal');

    modal.addEventListener('show.bs.modal', function (event) {

        const trigger = event.relatedTarget;
        const src = trigger.getAttribute('data-imagem');

        modalImg.src = src;

    });

});
document.addEventListener("DOMContentLoaded", function () {

    const chatBox = document.getElementById("chat-box");

    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

});