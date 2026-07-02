// EDITADO MAR-13

export function initTableCheckbox() {
	document.addEventListener("change", (event) => {

		const target = event.target;

		// CHECKBOX DO HEAD DAS TABELAS
		const checkbox_head = document.querySelector("#checkbox_head");


		if (target.id === "checkbox_head") {

			const content = target.parentNode;

			const content_collumn_head = content.parentNode;

			const row_head_table = content_collumn_head.parentNode;

			const table_head = row_head_table.parentNode;
			
			const table = table_head.parentNode;

			const list_checkbox = table.querySelectorAll(".row_checkbox"); // CHECKBOX DO BODY DAS TABELAS

			list_checkbox.forEach((cb) => { cb.checked = target.checked; });  // ADICIONA/REMOVE CHECKED DE TODOS CHECKBOXES			
		}

		// ADICIONA/REMOVE CHECKED INDIVIDUAL DE CADA CHECKBOXDO BODY CLICADO E REMOVE CHECKED DO CHECKBOX_HEAD
		if (target.classList.contains("row_checkbox")) {
			// const list_checkbox = document.querySelectorAll(".row_checkbox");
			if (checkbox_head) {
				checkbox_head.checked       = false;
				checkbox_head.indeterminate = true;
			}
		}
	});
}