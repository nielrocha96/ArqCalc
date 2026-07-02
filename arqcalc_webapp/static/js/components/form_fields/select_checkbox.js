/** EDITADO - ABRIL/5 
 
 * Inicializa componentes de multiselect com lógica de cálculo e interface.
 
 * @format
 */

export function initMultiSelect(containerId) {
	const container = document.getElementById(containerId);
	if (!container) return;

	const btn = container.querySelector(".btn_select_checkbox");
	const list = container.querySelector(".select_list");
	const hiddenInput = container.querySelector('input[type="hidden"]');
	const textDisplay = container.querySelector(".selected_text");
	const arrow = container.querySelector(".arrow_icon");

	// 1. Toggle de Abertura/Fechamento
	btn.addEventListener("click", (e) => {
		e.stopPropagation();
		const isOpen = container.classList.contains("open");

		document
			.querySelectorAll(".select_checkbox_container.open")
			.forEach((c) => {
				if (c !== container) {
					c.classList.remove("open");
					c.querySelector(".select_list").style.display = "none";
					const otherArrow = c.querySelector(".arrow_icon");
					if (otherArrow) otherArrow.classList.remove("rotate_arrow");
				}
			});

		if (isOpen) {
			container.classList.remove("open");
			list.style.display = "none";
			if (arrow) arrow.classList.remove("rotate_arrow");
		} else {
			container.classList.add("open");
			list.style.display = "block";
			if (arrow) arrow.classList.add("rotate_arrow");
		}
	});

	// Fechar ao clicar fora
	document.addEventListener("click", (e) => {
		if (!container.contains(e.target)) {
			container.classList.remove("open");
			list.style.display = "none";
			if (arrow) arrow.classList.remove("rotate_arrow");
		}
	});

	// 2. Lógica de Seleção e Cálculo
	container.addEventListener("change", (e) => {
		if (e.target.classList.contains("row_checkbox")) {
			const checkedInputs = container.querySelectorAll(
				".row_checkbox:checked",
			);

			// Atualiza o input hidden com os IDs (Ex: Custo-1, Custo-2)
			const values = Array.from(checkedInputs).map((cb) => cb.value);
			hiddenInput.value = values.join(",");

			// Atualiza o texto do botão com as descrições
			const labels = Array.from(checkedInputs).map((cb) =>
				cb.getAttribute("data-label"),
			);
			textDisplay.innerText =
				labels.length > 0 ? labels.join(", ") : "Selecionar itens";

			// Realiza a Soma Total
			let somaTotal = 0;
			checkedInputs.forEach((cb) => {
				const precoStr = cb
					.getAttribute("data-price")
					.replace(",", ".");
				const preco = parseFloat(precoStr);
				if (!isNaN(preco)) somaTotal += preco;
			});

			// Dispara evento para outros componentes (como o dashboard de custos)
			container.dispatchEvent(
				new CustomEvent("totalUpdated", {
					detail: { total: somaTotal, count: checkedInputs.length },
				}),
			);
		}
	});
}
