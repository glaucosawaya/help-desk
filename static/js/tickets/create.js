    const inputArquivos = document.getElementById("anexos-input");
    const listaArquivos = document.getElementById("lista-anexos");

    let arquivosSelecionados = [];

    inputArquivos.addEventListener("change", function () {

        for (const arquivo of this.files) {

            const existe = arquivosSelecionados.some(file =>
                file.name === arquivo.name &&
                file.size === arquivo.size &&
                file.lastModified === arquivo.lastModified
            );

            if (existe) {

                alert(`O arquivo "${arquivo.name}" já foi adicionado.`);

                continue;
            }

            arquivosSelecionados.push(arquivo);

            const item = document.createElement("li");

            item.className =
                "list-group-item d-flex justify-content-between align-items-center";

            item.innerHTML = `
                <span>${arquivo.name}</span>

                <button
                    type="button"
                    class="btn btn-sm btn-outline-danger">

                    ✕

                </button>
            `;

            const botaoRemover = item.querySelector("button");

            botaoRemover.addEventListener("click", function () {

                arquivosSelecionados = arquivosSelecionados.filter(file =>
                    !(
                        file.name === arquivo.name &&
                        file.size === arquivo.size &&
                        file.lastModified === arquivo.lastModified
                    )
                );

                atualizarInput();

                item.remove();

            });

            listaArquivos.appendChild(item);
        }

        atualizarInput();

        this.value = "";

    });

    function atualizarInput() {

        const dataTransfer = new DataTransfer();

        arquivosSelecionados.forEach(file => {
            dataTransfer.items.add(file);
        });

        inputArquivos.files = dataTransfer.files;
    }

