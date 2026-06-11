document.addEventListener("DOMContentLoaded", function () {

    const perfilMenu = document.getElementById("perfilMenu");
    const perfilChevron = document.getElementById("perfilChevron");

    if (perfilMenu && perfilChevron) {

        perfilMenu.addEventListener("shown.bs.collapse", function () {

            perfilChevron.classList.remove("bi-chevron-down");
            perfilChevron.classList.add("bi-chevron-up");

        });

        perfilMenu.addEventListener("hidden.bs.collapse", function () {

            perfilChevron.classList.remove("bi-chevron-up");
            perfilChevron.classList.add("bi-chevron-down");

        });

    }

});