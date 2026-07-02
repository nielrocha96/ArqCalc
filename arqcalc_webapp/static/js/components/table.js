/** @format */
// EDITADO MAR-17
import { initTableCheckbox } from "./buttons/btn_checkbox.js";

document.addEventListener("DOMContentLoaded", () => {
	// Inicialização dos checkboxes na tabela
	initTableCheckbox();

	

	const btnEditElements = document.querySelector("[data-row-id]  ");
	if (btnEditElements) {
		btnEditElements.forEach((btn) => {
			btn.addEventListener("click", (event) => {
				const rowId = btn.getAttribute("data-row-id");
				const selectContainer = document.getElementById(
					`select-${rowId}-container`,
				);
				const inputContainer = document.getElementById(
					`input-${rowId}-container`,
				);

				selectContainer.style.display = "none";
				inputContainer.style.display = "flex";
			});
		});
	}
});
