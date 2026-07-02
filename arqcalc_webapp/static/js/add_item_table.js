/** @format */
/**
 * EDITADO - ABRIL/5
 */

import { update_all_professional_selects } from "./projetos.js";

import { CurrencyManager } from "./main.js";



export function add_item_table(container) {
	const tableBody = container.querySelector(".table_body");
	const table = tableBody.parentNode;

	let rowTemplate = table.querySelector("#row-body-template");

	function templateHasInputs(template) {
		if (!template?.content) return false;
		const tr = template.content.querySelector("tr");
		if (!tr) return false;
		
		const cells = tr.querySelectorAll("th, td");
		return cells.length > 2;
	}

	if (!tableBody || !templateHasInputs(rowTemplate)) {
		// Tenta fallback para um template completo existente em .table_phases
		rowTemplate = document.querySelector(
			".table_phases #row-body-template",
		);
	}

	const newRowContent = rowTemplate.content.cloneNode(true);
	const row = newRowContent.querySelector("tr");
	const totalRows = tableBody.querySelectorAll("tr").length;

	//  Reseta os valores dos inputs (o que o usuário digita)
	row.querySelectorAll("input").forEach((input) => {
		input.value = "";
		input.defaultValue = "";
	});

	const inputTotalItem = row.querySelector('input[name="total_item"]');
	if (inputTotalItem) {
		inputTotalItem.value = `${CurrencyManager.format(0)}`;
		inputTotalItem.defaultValue = `${CurrencyManager.format(0)}`;
	}

	//  Reseta o texto visual dos botões/spans (o que o usuário vê)
	row.querySelectorAll(
		".professional_select_container, .select_item_status",
	).forEach((container) => {
		const span = container.querySelector("button span");
		const hiddenInput = container.querySelector("input[type='hidden']");

		if (container.classList.contains("select_item_status")) {
			span.textContent = "Em andamento";
		} else if (hiddenInput && hiddenInput.name === "responsible") {
			// Define o texto padrão que aparece no botão do select de responsável
			span.textContent = "Responsável";
		}
	});

	// --- CONFIGURAÇÃO DA NOVA LINHA ---
	row.dataset.id = `temp-${totalRows + 1}`;

	// Habilitar elementos e remover classes de "vazio"
	row.querySelectorAll("input, button, .selected_item_base").forEach((el) => {
		el.disabled = false;
		el.removeAttribute("disabled");
		el.classList.remove("cell_none");
	});

	// Tratar selects de profissional se existirem
	const hasProfessionalSelect = row.querySelector(".custom_options_base");
	if (hasProfessionalSelect) {
		setTimeout(() => update_all_professional_selects(), 10);
	}

	tableBody.appendChild(row);
	CurrencyManager.updateUI();
}
