/** @format */
// # EDITADO - ABRIL/2

import "./components/modals/modal_new_costs.js";

document.addEventListener("click", async (e) => {
	const target = e.target;
	const modal = document.querySelector(".modal_new_costs");
    const form = document.getElementById("form_costs");
    const titleElement = modal.querySelector("h2");

	// 1. ABRIR MODAL PARA NOVO ITEM
	if (target.closest(".btn_add_custo_fixo")) {
		form.reset();
		document.getElementById("modal_item_id").value = "";
		titleElement.innerText = "Adicionar Custo Fixo";
		modal.classList.add("active");
	}

	// 2. ABRIR MODAL PARA EDIÇÃO
    if (target.closest(".btn_edit")) {
        const th = target.parentNode;
		const tr = th.parentNode;

		titleElement.innerText = "Adicionar Custo Fixo";
		const elDescription = tr.querySelector("input[name='description']");
		const elValue = tr.querySelector("input[name='value']");
		const itemIdInput = document.getElementById("modal_item_id");

		// Verifica se os elementos existem antes de acessar o innerText
		if (elDescription && elValue) {
			itemIdInput.value = tr.dataset.id || "";
			document.getElementById("modal_description").value =
				elDescription.value.trim();
			document.getElementById("modal_value").value = elValue.value
				.replace("R$", "")
				.replace(",", ".") 
				.trim();

			modal.classList.add("active");
		} else {
			console.error(
				"Erro: Classes .cell_description ou .cell_value não encontradas na linha.",
			);
		}
	}
});

// 3. ENVIO VIA AJAX (FETCH)
document.getElementById("form_costs").addEventListener("submit", function (e) {
	e.preventDefault();

	const itemId = document.getElementById("modal_item_id").value;
	const formData = new FormData(this);

	// CORREÇÃO: Adicionada a barra "/" no início para ser um caminho absoluto
	// E usamos a estrutura que você definiu no urls.py: /resource/gerenciar_itens/
	let url = "/custos_fixos/gerenciar_itens/";

	if (itemId) {
		url += `${itemId}/`; // Resulta em /custos_fixos/gerenciar_itens/2/
	}

	fetch(url, {
		method: "POST",
		body: formData,
		headers: {
			// O Django precisa do CSRF para validar o POST
			"X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
				.value,
		},
	})
		.then((response) => {
			if (!response.ok) throw new Error("Erro na rede ou 404");
			return response.json();
		})
		.then((data) => {
			// Ajustado para ler 'status' conforme sua GerenciarItensView sugerida
			if (data.status === "sucesso" || data.success) {
				alert("Operação realizada com sucesso!");
				location.reload();
			} else {
				alert("Erro: " + (data.message || "Falha ao salvar"));
			}
		})
		.catch((error) => {
			console.error("Erro na requisição:", error);
		});
});