/** @format */
// EDITADO - ABRIL / 5 
 
document.addEventListener("click", (e) => {
	const target = e.target;

	// --- 1. IDENTIFICAÇÃO DO CONTAINER ---
	const selectContainer = target.closest(".form-group div[id]");
	

	// Fechar ao clicar fora
	if (!selectContainer) {
		document.querySelectorAll(".form-group div[id].open").forEach((s) => {
			s.classList.remove("open");
			// Se houver seta, reseta a rotação
			const arrow = s.querySelector(".arrow_icon");
			if (arrow) arrow.classList.remove("rotate_arrow");
		});
		return;
	}

	const arrow = selectContainer.querySelector(".arrow_icon");

	// --- 2. LÓGICA DE ABRIR/FECHAR ---
	const selectButton = target.closest("button[type='button']");
	if (selectButton) {
		e.stopPropagation();

		// Fecha outros abertos
		document
			.querySelectorAll(".form-group div[id].open")
			.forEach((open) => {
				if (open !== selectContainer) open.classList.remove("open");
			});

		selectContainer.classList.toggle("open");
		if (arrow) arrow.classList.toggle("rotate_arrow");
		return;
	}

	// --- 3. LÓGICA DE SELEÇÃO DE ITEM (LI) ---
	const optionItem = target.closest("li[data-value]");
	
	if (optionItem) {
		const btn = selectContainer.querySelector("button");
		const span = btn.querySelector("span");

		const hiddenInput = selectContainer.querySelector(
			"input[type='hidden']",
		);


		const newValue = optionItem.getAttribute("data-value");
		const newId = optionItem.getAttribute("data-id")
		const newText = optionItem.textContent.trim();

		hiddenInput.value = newValue;
		hiddenInput.id = newId;
		span.textContent = newText;

		// --- SEPARAÇÃO DE LÓGICAS DE ESTILO ---

		if (btn.classList.contains("selected_item_status")) {
			// --- LÓGICA ESPECÍFICA: STATUS ---

			// Limpa classes de status anteriores
			const classesLimpas = Array.from(btn.classList).filter(
				(c) => !c.startsWith("status-"),
			);
			btn.className = classesLimpas.join(" ");

			// Adiciona a nova cor baseada no valor (ex: status-aprovado)
			btn.classList.add(`status-${newValue}`);
		} else if (btn.classList.contains("selected_item_base")) {
			// --- LÓGICA ESPECÍFICA: PADRÃO (BASE) ---

			const classesLimpas = Array.from(btn.classList).filter(
				(c) => !c.startsWith("status-"),
			);
			btn.className = classesLimpas.join(" ");
		}

		// --- FINALIZAÇÃO COMUM ---

		selectContainer.querySelectorAll("li").forEach((li) => {
			li.classList.remove("active", "selected");
		});
		optionItem.classList.add("active", "selected");

		// Fecha o menu
		selectContainer.classList.remove("open");
		if (arrow) arrow.classList.remove("rotate_arrow");


		// Notifica o HTMX/DOM
		hiddenInput.dispatchEvent(new Event("input", { bubbles: true }));
		hiddenInput.dispatchEvent(new Event("change", { bubbles: true }));
	}
});
