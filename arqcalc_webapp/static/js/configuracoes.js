/** @format */
// # EDITADO - ABRIL/10

import { CurrencyManager } from "./main.js";

document.addEventListener("DOMContentLoaded", function () {
	// --- LÓGICA DAS ABAS ---
	const tabs = document.querySelectorAll(".tab");
	const contents = document.querySelectorAll(".tab-content");

	tabs.forEach((tab) => {
		tab.addEventListener("click", () => {
			const target = tab.getAttribute("data-tab");

			tabs.forEach((t) => t.classList.remove("active"));
			contents.forEach((c) => c.classList.remove("active"));

			tab.classList.add("active");
			const targetElement = document.getElementById(target);
			if (targetElement) {
				targetElement.classList.add("active");
			}
		});
	});

	// --- LÓGICA DO INPUT DE FOTO  ---
	// Usa a delegação de evento no document para garantir que pegue o input
	document.addEventListener("change", function (event) {
		// Verifica se o ID do elemento que mudou é o do seu input
		if (event.target && event.target.id === "input_photo") {
			const fileInput = event.target;
			const fileNameDisplay = document.getElementById("file_name");

			if (fileNameDisplay) {
				if (fileInput.files && fileInput.files.length > 0) {
					// Pega o nome do arquivo selecionado
					const name = fileInput.files[0].name;
					fileNameDisplay.textContent = name;
					fileNameDisplay.style.color = "#6f42c1";
					fileNameDisplay.style.fontWeight = "bold";
				} else {
					// Caso o usuário cancele a seleção
					fileNameDisplay.textContent = "Nenhuma imagem selecionada";
					fileNameDisplay.style.color = "#666";
					fileNameDisplay.style.fontWeight = "normal";
				}
			}
		}
	});

	// --- LÓGICA DO SELECT DE MOEDA (CUSTOMIZADO) ---

	const moedaSelectContainer = document.getElementById("moeda_select");

	if (moedaSelectContainer) {
		const moedaButton = moedaSelectContainer.querySelector("button");
		const moedaInput = moedaSelectContainer.querySelector(
			'input[name="moeda_selecionada"]',
		);
		const moedaOptions = moedaSelectContainer.querySelectorAll("ul li");

		// Restaurar a moeda salva no localStorage
		const savedCurrency = localStorage.getItem("user_currency");
		if (savedCurrency && moedaInput) {
			moedaInput.value = savedCurrency;

			// Atualizar o texto do botão
			const selectedOption = moedaSelectContainer.querySelector(
				`li[data-value="${savedCurrency}"]`,
			);
			if (selectedOption) {
				moedaButton.querySelector("span").textContent =
					selectedOption.textContent;
				// Atualizar classes
				moedaOptions.forEach((opt) =>
					opt.classList.remove("active", "selected"),
				);
				selectedOption.classList.add("active", "selected");
			}
		}

		// Adicionar listener para cada opção
		moedaOptions.forEach((option) => {
			option.addEventListener("click", (e) => {
				e.preventDefault();
				const selectedValue = option.getAttribute("data-value");

				// Atualizar o input hidden
				if (moedaInput) {
					moedaInput.value = selectedValue;
				}

				// Atualizar o texto do botão
				moedaButton.querySelector("span").textContent =
					option.textContent;

				// Remover classe 'active' de todas as opções e adicionar à selecionada
				moedaOptions.forEach((opt) =>
					opt.classList.remove("active", "selected"),
				);
				option.classList.add("active", "selected");

				// Salvar no localStorage
				localStorage.setItem("user_currency", selectedValue);

				// Atualizar a UI com a nova moeda
				CurrencyManager.updateUI();
			});
		});
	}
});
