/**
 * EDITADO ABRIL/11
 *
 * @format
 */

import "./components/modals/modal_confirmation.js";
import "./components/buttons/btn_notification.js";
import "./components/buttons/btn_delete.js";
import "./components/buttons/btn_primary.js";
import "./components/buttons/btn_copy.js";
 import "./components/buttons/btn_pdf.js";


import "./components/table.js";

import "./components/form_fields/select_base.js";
import "./components/form_fields/select_checkbox.js";


export function toggleModal(idItem) {
	const modal = document.querySelector(`#${idItem}`);
	modal.classList.toggle("active_modal");
}

export function toggleModalManual(idItem, boolean) {
	const modal = document.querySelector(`#${idItem}`);

	if (boolean === true) {
		{
			modal.classList.add("active");
		}
	} else {
		modal.classList.remove("active");
	}
}

/**
 * Utilitário global para formatação e conversão de moeda.
 * Gerencia a exibição visual e a extração de valores numéricos para cálculos.
 */
export const CurrencyManager = {
	/**
	 * Recupera as configurações de localidade (Brasil, EUA, Europa)
	 * com base na escolha salva pelo usuário no localStorage.
	 */
	getCurrencyConfig() {
		const saved = localStorage.getItem("user_currency") || "BRL";
		const configs = {
			BRL: {
				locale: "pt-BR",
				currency: "BRL",
				symbol: "R$",
				decimal: ",",
				thousands: ".",
			},
			USD: {
				locale: "en-US",
				currency: "USD",
				symbol: "$",
				decimal: ".",
				thousands: ",",
			},
			EUR: {
				locale: "de-DE",
				currency: "EUR",
				symbol: "€",
				decimal: ",",
				thousands: ".",
			},
		};
		return configs[saved] || configs["BRL"];
	},

	/**
	 * TRANSFORMA TEXTO EM NÚMERO (FLOAT)
	 * Essencial para cálculos. Remove símbolos e trata separadores decimais.
	 */
	parseCurrency(value) {
		if (!value) return 0;

		const config = this.getCurrencyConfig();

		// 1. Remove símbolos de moeda, espaços e separadores de milhar
		// Ex: "R$ 1.250,50" -> "1250,50"
		let cleanValue = value
			.toString()
			.replace(config.symbol, "")
			.replace(/\s/g, "")
			.split(config.thousands)
			.join("");

		// 2. Substitui a vírgula decimal por ponto para que o parseFloat entenda
		// Ex: "1250,50" -> "1250.50"
		if (config.decimal === ",") {
			cleanValue = cleanValue.replace(",", ".");
		}

		// 3. Converte para float real. Se falhar, retorna 0.
		return parseFloat(cleanValue) || 0;
	},

	/**
	 * FORMATA NÚMERO PARA MOEDA (STRING)
	 * Transforma 1250.5 em "R$ 1.250,50"
	 */
	format(value) {
		const config = this.getCurrencyConfig();

		// Garante que o valor processado seja um número
		const number =
			typeof value === "string" ? this.parseCurrency(value) : value;

		return (number || 0).toLocaleString(config.locale, {
			style: "currency",
			currency: config.currency,
		});
	},

	/**
	 * MÁSCARA DE INPUT EM TEMPO REAL
	 * Formata o valor enquanto o usuário digita (ex: 100 vira R$ 1,00)
	 */
	formatInput(input) {
		// Remove tudo que não é dígito
		let value = input.value.replace(/\D/g, "");

		if (value === "") {
			input.value = "";
			return;
		}

		// Converte para decimal (centavos)
		const numberValue = parseFloat(value) / 100;

		// Usa a função format que já respeita o local (BRL, USD, etc)
		input.value = this.format(numberValue);
	},
	/**
	 * ATUALIZA TODA A INTERFACE
	 * Varre a página procurando por elementos que precisam de formatação de moeda
	 */
	updateUI() {
		const config = this.getCurrencyConfig();

		// 1. Atualiza símbolos estáticos em labels ou cabeçalhos
		document.querySelectorAll(".currency-symbol").forEach((el) => {
			el.textContent = config.symbol;
		});

		// 2. Formata inputs que possuem a classe '.input-currency'
		document
			.querySelectorAll(".input-currency, .currency-input")
			.forEach((input) => {
				input.placeholder = `${config.symbol} 0,00`;
				if (input.value) {
					this.formatInput(input);
				}
			});

		// 3. Seletores de células de tabela que contêm valores monetários
		const tableSelectors = [
			".currency-format",
		];

		document.querySelectorAll(tableSelectors.join(",")).forEach((cell) => {
			// Ignora se houver um input dentro (o input é tratado separadamente)
			if (cell.querySelector("input")) return;

			// Extrai o valor, trata o formato de entrada e reaplica a formatação da moeda atual
			const rawValue = cell.textContent
				.replace(/[^\d,.-]/g, "")
				.replace(",", ".");

			if (!isNaN(parseFloat(rawValue)) && rawValue.trim() !== "") {
				cell.textContent = this.format(rawValue);
			}
		});

		// 4. Configura placehoders de inputs específicos por nome
		const inputSelectors = [
			'input[name="cost_value"]',
			'input[name="value_hour"]',
			'input[name="total_item"]',
		];

		document.querySelectorAll(inputSelectors.join(",")).forEach((input) => {
			input.placeholder = config.symbol + " 0,00";
		});
	},
};

/**
 * Inicializa o CurrencyManager quando o documento estiver pronto
 */
document.addEventListener("DOMContentLoaded", () => {
	CurrencyManager.updateUI();
});
