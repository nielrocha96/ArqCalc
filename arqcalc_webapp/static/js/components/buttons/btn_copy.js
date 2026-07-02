// EDITADO ABRIL-6

import { configurarModal } from "../modals/modal_confirmation.js";

document.addEventListener("DOMContentLoaded", () => {
    async function abrirModalClone(
        urlDestino,
        btnClicked,
        table,
    ) {
        try {
            //BUSCA PELO CONTEÚDO DO MODAL DE CONFIRMAÇÃO
            const response = await fetch(urlDestino, {
                headers: { "x-requested-with": "XMLHttpRequest" },
            });

            if (!response.ok)
                throw new Error("Erro ao buscar dados do servidor");


            const data = await response.json();

            configurarModal(data, table, null);


        
        } catch (error) {
            console.error("Falha na operação:", error);
        }
    }

    // EVENT DELEGATION: Ouve cliques em qualquer lugar do documento
    document.addEventListener("click", function (event) {
        // Verifica se o clique foi no botão ou em algum ícone dentro dele
        const btn = event.target.closest(".btn_copy");

        if (btn) { 
            const url = btn.getAttribute("data-url");
            
            const content = btn.parentNode;
            
            const row = content?.parentNode;
            
            const container_row = row?.parentNode;
            
            const table = container_row?.parentNode;

            if (url && table.closest('.table')) {
                console.log("URL para o modal:", url);
                abrirModalClone(url, btn, table);
            }


        }
    });
});
