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

    const chatModal = document.getElementById("chatModal");

    if (chatModal) {

        chatModal.addEventListener("shown.bs.modal", function () {

            const chatBox = document.getElementById("chat-box");

            if (chatBox) {
                chatBox.scrollTop = chatBox.scrollHeight;
            }

        });

    }

});

const chatForm = document.getElementById("chat-form");

if (chatForm) {

    chatForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const formData = new FormData(chatForm);

        fetch(chatForm.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {

            if (data.success) {

                const chatBox = document.getElementById("chat-box");

                chatBox.insertAdjacentHTML("beforeend", `
                    <div class="d-flex justify-content-end mb-3">
                        <div class="bg-primary text-white p-2 rounded"
                             style="max-width:70%;">

                            <small class="d-block fw-bold">
                                Você
                            </small>

                            ${data.comment}

                            <div class="small text-white-50 text-end">
                                ${data.created_at}
                            </div>

                        </div>
                    </div>
                `);

                chatForm.reset();

                chatBox.scrollTop = chatBox.scrollHeight;
            }

        });

    });

}
document.addEventListener("DOMContentLoaded", function () {

    const statusSelect = document.getElementById("status-select");
    const waitingContainer = document.getElementById("waiting-message-container");

    if (statusSelect && waitingContainer) {

        function toggleWaitingMessage() {

            if (statusSelect.value === "WAITING_USER") {

                waitingContainer.style.display = "block";

            } else {

                waitingContainer.style.display = "none";

            }
        }

        toggleWaitingMessage();

        statusSelect.addEventListener("change", toggleWaitingMessage);
    }

});