/** @format */
// EIDTADO ABRIL/20

// GERENCIA O MODAL DE CONFIRMAÇÃO PARA AÇÕES DE DELETE E CLONE

import { CurrencyManager, toggleModalManual } from "../../main.js";
import { update_all_professional_selects } from "../../projetos.js";
import { deleteObject } from "../buttons/btn_delete.js";

// CONTEXTO GLOBAL DO MODAL
const data_context = {
	table: null,
	action: null,
	page: null,
};

const btnConfirm = document.querySelector("#btn_confirm_modal");
const btnCancel = document.querySelector("#btn_cancel_modal");

// CANCELAR
if (btnCancel) {
	btnCancel.addEventListener("click", () => {
		fecharModal();

		document.querySelectorAll(".phase_container").forEach((el) => {
			el.classList.remove("temp-delete");
		});
	});
}

// =========================
// ABRIR MODAL
// =========================
export function configurarModal(dados, table = null, page = null) {
	const titulo = document.getElementById("modal_confirmation_title");
	const corpo = document.getElementById("modal_confirmation_body");
	const btnConfirm = document.getElementById("btn_confirm_modal");
	const btnCancel = document.getElementById("btn_cancel_modal");

	titulo.innerText = dados.titulo;
	corpo.innerText = dados.corpo;
	btnConfirm.innerText = dados.botoes?.confirm?.texto;
	btnCancel.innerText = dados.botoes?.cancel?.texto;
	btnCancel.classList.add(dados.botoes?.cancel?.class);

	// salva contexto
	data_context.table = table;
	data_context.page = page;
	data_context.action = dados.botoes?.confirm?.class;

	resetConfirmButton();

	// Configura classe do botão de confirmação com base na ação
	if (data_context.action === "btn_delete_confirmation") {
		btnConfirm.classList.add("btn_delete_confirmation");
	} else if (data_context.action === "btn_copy_confirmation") {
		btnConfirm.classList.add("btn_copy_confirmation");
	}

	toggleModalManual("modal_confirmation_container", true);
	document.body.classList.add("no-scroll");
}

// =========================
// CLICK GLOBAL DO CONFIRM
// =========================
if (btnConfirm) {
	btnConfirm.addEventListener("click", async () => {
		if (data_context.action === "btn_delete_confirmation") {
			if (deleteObject.etapa) {
				await handleDeleteEtapa();
			} else {
				await handleDelete();
			}
		}

		if (data_context.action === "btn_copy_confirmation") {
			await handleClone();
		}
	});
}

// =========================
// RESET BOTÃO
// =========================
function resetConfirmButton() {
	btnConfirm.classList.remove(
		"btn_delete_confirmation",
		"btn_copy_confirmation",
	);
}

// =========================
// FECHAR MODAL
// =========================

function fecharModal() {
	toggleModalManual("modal_confirmation_container", false);
	document.body.classList.remove("no-scroll");
}

// =========================
//     GARANTIR LINHA MÍNIMA
// =========================
function garantirLinhaMinima(table) {
	const tbody = table.querySelector(".table_body");

	if (!tbody) return;

	const rows = tbody.querySelectorAll("tr");
	if (rows.length > 0) return;

	// MELHORIA: Busca o template na tabela ou no documento global caso falhe
	let template = table.querySelector("#row-body-template");
	if (!template) {
		template = document.querySelector("#row-body-template");
	}

	if (!template) {
		console.error("Template de linha não encontrado no DOM.");
		return;
	}

	const clone = template.content.cloneNode(true);
	const newRow = clone.querySelector("tr"); // Busca a TR diretamente no clone

	if (newRow) {
		// Define um ID temporário único
		const phaseContainer = table.closest(".phase_container");
		const phaseIndex =
			phaseContainer ?
				phaseContainer
					.querySelector('input[name="phase_name"]')
					?.id?.replace(/\D/g, "")
			:	Date.now();
		newRow.dataset.id = `temp-${phaseIndex}-min`;

		// Limpa inputs de texto e mantém os valores padrão de moeda
		newRow.querySelectorAll("input").forEach((input) => {
			if (input.name === "total_item") {
				input.value =
					typeof CurrencyManager !== "undefined" ?
						CurrencyManager.format(0)
					:	"R$ 0,00";
			} else if (input.classList.contains("currency-input")) {
				input.value =
					typeof CurrencyManager !== "undefined" ?
						CurrencyManager.format(0)
					:	"R$ 0,00";
			} else {
				input.value = "";
			}
		});

		// Garante que os checkboxes estejam desmarcados
		newRow.querySelectorAll(".row_checkbox").forEach((cb) => {
			cb.checked = false;
		});

		tbody.appendChild(newRow);

		// ESSENCIAL: Atualiza os selects de profissionais para a nova linha
		if (typeof update_all_professional_selects === "function") {
			update_all_professional_selects();
		}

		// Re-vincula eventos de moeda se necessário
		if (typeof CurrencyManager !== "undefined") {
			CurrencyManager.updateUI();
		}
	}
}

// =========================
// 	DELETE ITEm
// =========================
async function handleDelete() {
	const table = data_context?.table;

	const page = data_context?.page;

	if (!table) return;

	const itens_back = [];
	const itens_front = [];

	const checkedCheckboxes = data_context?.table?.querySelectorAll(
		`.row_checkbox:checked`,
	);

	checkedCheckboxes?.forEach((cb) => {
		const row = cb.closest("tr");
		const id = row.dataset.id;

		if (id && id.toString().startsWith("temp-")) {
			row.remove(); // remove direto
		} else {
			itens_back.push(id);
		}
	});
	// REMOVE FRONT
	itens_front.forEach((item) => item.remove());

	// DELETE BACKEND
	if (itens_back.length > 0) {
		await delete_itens_db(itens_back, page);
	}

	// GARANTE LINHA MÍNIMA
	if (table) {
		garantirLinhaMinima(table);
	}

	fecharModal();
}

// =========================
// DELETE ETAPA COMPLETA
// =========================

async function handleDeleteEtapa() {
	const table = data_context?.table;

	const phaseId = table.dataset.id;

	// Se o ID não começar com 'temp-', ele existe no banco de dados
	if (phaseId && !phaseId.toString().startsWith("temp-")) {
		const page = data_context?.page;


		const url = `/${page}/gerenciar_itens/`;

		const payload = {
			item_id: phaseId,
			// Se for uma etapa, passamos 'phase', se for um item de tabela, 'item'
			resource_type: "phase",
		};

		try {
			const response = await fetch(url, {
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"),
				},
				body: JSON.stringify(payload),
			});

			//status 204 é sucesso sem conteúdo, ou seja, foi deletado mas não tem o que retornar
			// Se a resposta for 204, removemos a etapa do DOM
			// Se for outro status, podemos mostrar um erro ou tentar novamente
			if (response.status === 204) {
				table.remove();
			} else {
				console.error("Erro ao deletar etapa no backend. Status:", response.status);
				// Aqui você pode optar por mostrar uma mensagem de erro para o usuário
			}

		} catch (e) {
			console.error(e);
		}
	}

	const checkPhases = document.querySelectorAll(".phase_container");
	// SE EXISTIR APENAS UMA ETAPA, LIMPA OS DADOS AO INVÉS DE EXCLUIR (LÓGICA PARA FRONT)
	if (checkPhases.length <= 1) {
		fecharModal();


		// 1. Reset do Responsável da Etapa (Cabeçalho)
		const phaseResponsibleInput = table.querySelector(
			".phases input[name='professional_phase']",
		);
		const phaseResponsibleSpan = table.querySelector(
			".phases .selected_item_base span",
		);

		if (phaseResponsibleInput) phaseResponsibleInput.value = "";
		if (phaseResponsibleSpan)
			phaseResponsibleSpan.innerText = "Selecione o Profissional"; // Ou o texto padrão que você usa

		// 2. Reset do Nome da Etapa
		const phaseNameInput = table.querySelector("input[name='phase_name']");
		if (phaseNameInput) phaseNameInput.value = "";

		// 3. Gerenciamento das Linhas da Tabela
		const table_body = table.querySelector(".table_body");
		if (table_body) {
			const list_row = table_body.querySelectorAll("tr");

			list_row.forEach((row, index) => {
				if (index === 0) {
					// Reseta a primeira linha
					row.querySelectorAll("input").forEach((input) => {
						if (input.name === "total_item") {
							input.value =
								typeof CurrencyManager !== "undefined" ?
									CurrencyManager.format(0)
								:	"R$ 0,00";
						} else if (input.name === "responsible") {
							// Reseta o select customizado da linha
							const span = input.parentNode.querySelector("span");
							if (span) span.innerText = "Responsável";
							input.value = "";
						} else {
							input.value = "";
						}
					});

					// Reseta checkboxes se houver
					const cb = row.querySelector(".row_checkbox");
					if (cb) cb.checked = false;
				} else {
					// Remove as linhas excedentes
					row.remove();
				}
			});
		}
		return; // Interrompe aqui para não tentar deletar o elemento do DOM
	}

	const validateDeleteInFront = phaseId.toString().startsWith("temp-") ? true : false;

	// SE TIVER MAIS DE UMA ETAPA, REMOVE NORMALMENTE
	if ( validateDeleteInFront) {
		table.remove();
	}

	fecharModal();
	return;
}

// =========================
// CLONE
// =========================
async function handleClone() {
	const table = data_context.table;

	if (!table) return;

	// =========================
	//  CLONA A TABELA
	// =========================
	const tableClone = table.cloneNode(true);

	// =========================
	//  CRIA NOVA ETAPA (IGUAL AO BOTÃO ADD)
	// =========================
	const phases_list = document.querySelector("#phases_list");
	const phases_container = phases_list?.parentNode;
	const template_phase = phases_container?.querySelector("#phase-template");

	if (!template_phase) {
		console.error("Template de etapa não encontrado");
		return;
	}

	const newIndex =
		phases_list.querySelectorAll(".phase_container").length + 1;

	let phaseHtml = template_phase.innerHTML.replace(/__prefix__/g, newIndex);

	const tempDiv = document.createElement("div");
	tempDiv.innerHTML = phaseHtml;

	const newPhase = tempDiv.firstElementChild;

	// =========================
	//  INSERE A TABELA CLONADA NA NOVA ETAPA
	// =========================
	const phaseTableBody = newPhase.querySelector(".table_body");

	if (phaseTableBody) {
		phaseTableBody.innerHTML = "";

		// pega só o tbody da tabela clonada
		const cloneRows = tableClone.querySelectorAll("tbody tr");

		cloneRows.forEach((row, index) => {
			const newRow = row.cloneNode(true);
			newRow.querySelectorAll(".row_checkbox").forEach((cb) => {
				cb.checked = false;
			});

			// atualiza ID temporário (IMPORTANTE)
			newRow.dataset.id = `temp-${newIndex}-${index + 1}`;

			phaseTableBody.appendChild(newRow);
		});
	}

	// =========================
	//  INSERE A NOVA ETAPA NA TELA
	// =========================
	phases_list.appendChild(newPhase);

	// =========================
	//  ATUALIZA UI GLOBAL
	// =========================
	if (typeof update_all_professional_selects === "function") {
		update_all_professional_selects();
	}

	if (typeof CurrencyManager !== "undefined") {
		CurrencyManager.updateUI();
	}

	newPhase.scrollIntoView({ behavior: "smooth" });

	fecharModal();
}

// =========================
// DELETE BACKEND
// =========================
async function delete_itens_db(ids, page) {
	const url = `/${page}/gerenciar_itens/`;
	const payload = {
		item_ids: ids,
		// Se for uma etapa, passamos 'phase', se for um item de tabela, 'item'
		resource_type: "item",
	};

	try {
		await fetch(url, {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			body: JSON.stringify(payload),
		});
	} catch (e) {
		console.error(e);
	}
}

function getCookie(name) {
	let cookieValue = null;

	if (document.cookie) {
		document.cookie.split(";").forEach((cookie) => {
			cookie = cookie.trim();
			if (cookie.startsWith(name + "=")) {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1),
				);
			}
		});
	}
	return cookieValue;
}
