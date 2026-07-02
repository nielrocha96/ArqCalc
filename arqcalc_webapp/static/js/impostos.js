/** @format */
// # EDITADO - ABRIL/2

import "./components/modals/modal_new_costs.js";

document.addEventListener("click", async (e) => {
	const target = e.target;
	const modal = document.querySelector(".modal_new_costs");

	// Se o modal não existir na página atual, interrompe para não dar erro
	if (!modal) return;

	const form = document.getElementById("form_costs");
	// Buscamos o h2 de forma mais direta ou garantimos que ele existe
	const titleElement = modal.querySelector("h2");

	// 1. ABRIR MODAL PARA NOVO ITEM
	if (target.closest(".btn_add_imposto")) {
		form.reset();
		document.getElementById("modal_item_id").value = "";
		if (titleElement) titleElement.innerText = "Adicionar Impostos";
		modal.classList.add("active");
	}

	// 2. ABRIR MODAL PARA EDIÇÃO (Usando ParentNode como solicitado)
	if (target.closest(".btn_edit")) {
		const th = target.parentNode;
		const tr = th.parentNode;

		if (titleElement) titleElement.innerText = "Editar Impostos";

		const elDescription = tr.querySelector("input[name='description']");
		const elValue = tr.querySelector("input[name='value']");
		const itemIdInput = document.getElementById("modal_item_id");

		if (elDescription && elValue) {
			itemIdInput.value = tr.dataset.id || "";
			document.getElementById("modal_description").value =
				elDescription.value.trim();
			document.getElementById("modal_value").value = elValue.value
				.replace("R$", "")
				.replace(",", ".")
				.trim();

			modal.classList.add("active");
		}
	}
});

// 3. ENVIO VIA AJAX (FETCH) - Mantendo a URL correta para impostos
document.getElementById("form_costs").addEventListener("submit", function (e) {
	e.preventDefault();

	const itemId = document.getElementById("modal_item_id").value;
	const formData = new FormData(this);

	// Rota absoluta para evitar o erro de duplicação que você teve antes
	let url = "/impostos/gerenciar_itens/";

	if (itemId) {
		url += `${itemId}/`;
	}

	fetch(url, {
		method: "POST",
		body: formData,
		headers: {
			"X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
				.value,
		},
	})
		.then((response) => {
			if (!response.ok) throw new Error("Erro 500 ou 404 no servidor");
			return response.json();
		})
		.then((data) => {
			if (data.success || data.status === "sucesso") {
				location.reload();
			} else {
				alert("Erro: " + data.message);
			}
		})
		.catch((error) => console.error("Erro na requisição:", error));
});
