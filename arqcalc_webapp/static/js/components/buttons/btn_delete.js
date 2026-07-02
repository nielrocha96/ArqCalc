/** @format */
// EDITADO ABRIL/8

import { configurarModal } from "../modals/modal_confirmation.js";

export const deleteObject = {
	"item": true,
	"etapa": true,
}

document.addEventListener("DOMContentLoaded", () => {
	async function carregarDadosEAbrirModal(urlDestino, btnClicked, table, ) {
		try {
			//BUSCA PELO CONTEÚDO DO MODAL DE CONFIRMAÇÃO
			const response = await fetch(urlDestino, {
				headers: { "x-requested-with": "XMLHttpRequest" },
			});

			if (!response.ok)
				throw new Error("Erro ao buscar dados do servidor");

			const data = await response.json();

			const page = btnClicked.getAttribute("data-page"); 

			configurarModal(data, table, page, );;

		} catch (error) {
			console.error("Falha na operação:", error);
		}
	}

	// EVENT DELEGATION: Ouve cliques em qualquer lugar do documento
	document.addEventListener("click", function (event) {
		// Verifica se o clique foi no botão ou em algum ícone dentro dele
		const btn = event.target.closest(".btn_delete");

		if (btn) {
			const url = btn.getAttribute("data-url");

			const content = btn.parentNode;

			const row = content?.parentNode;

			const container_row = row?.parentNode;

			const table = container_row?.parentNode;

			if (url && table.closest(".table")) {
				deleteObject.etapa = false;
				deleteObject.item = true;
				carregarDadosEAbrirModal(url, btn, table);
			}

			const etapa = container_row.classList.contains("phase_container");

			if (etapa && btn.classList.contains("delete_phase")) {
				deleteObject.etapa = true;
				deleteObject.item = false;
				carregarDadosEAbrirModal(url, btn, container_row);
			}
		}
	});
});
