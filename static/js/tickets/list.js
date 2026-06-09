$(document).ready(function () {

    const table = $('#tickets-table').DataTable({

        responsive: false,

        scrollX: true,

        pageLength: 25,

        order: [[7, 'desc']],

        language: {

            lengthMenu: "Mostrar _MENU_ registros",

            search: "Pesquisar:",

            info: "Mostrando de _START_ até _END_ de _TOTAL_ registros",

            infoEmpty: "Mostrando 0 até 0 de 0 registros",

            infoFiltered: "(filtrado de _MAX_ registros)",

            zeroRecords: "Nenhum registro encontrado",

            emptyTable: "Nenhum registro disponível",

            paginate: {
                first: "Primeira",
                last: "Última",
                next: "Próxima",
                previous: "Anterior"
            }

        }

    });

    $('.filter-btn').on('click', function () {

    $('.filter-btn').removeClass(
        'active'
    );

    $(this).addClass(
        'active'
    );

    const status = $(this).data(
        'status'
    );

    table
        .column(5)
        .search(status)
        .draw();

});

});