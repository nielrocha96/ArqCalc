/** @format */

import { CurrencyManager } from "../../main.js";

//  EDITADO - ABRIL/6
//  Centraliza os cálculos de precificação e aplica formatação de moeda dinâmica.

const pricing = {

	// Busca dados brutos da interface
	getRawData() {
		let totalCustosFixos = 0;
		document
			.querySelectorAll("#container-custos-fixos .row_checkbox:checked")
			.forEach((cb) => {
				totalCustosFixos +=
					CurrencyManager.parseCurrency(cb.getAttribute("data-price")) || 0;
			});

		let totalImpostoPerc = 0;
		document
			.querySelectorAll("#container-impostos .row_checkbox:checked")
			.forEach((cb) => {
				totalImpostoPerc +=
					CurrencyManager.parseCurrency(cb.getAttribute("data-price")) || 0;
			});

		return {
			venda:
				CurrencyManager.parseCurrency(
					document.getElementById("preco_venda")?.value,
				) || 0,
			impostoPerc: totalImpostoPerc,
			comissaoPerc:
				CurrencyManager.parseCurrency(
					document.getElementById("comissoes_percent")?.value,
				) || 0,
			custoFixo: totalCustosFixos,
		};
	},

	calculateCosts() {
		const custoVariavel = this.getSumFromEtapas();
		const custoEspecifico = this.getSumFromCustosEspecificos();
		const data = this.getRawData();
		const custoOperacional =
			custoVariavel + custoEspecifico + data.custoFixo;

		return {
			custoVariavel,
			custoEspecifico,
			custoFixo: data.custoFixo,
			custoOperacional,
		};
	},

	calculatePricing() {
		const costs = this.calculateCosts();
		const data = this.getRawData();

		const valorImposto = (data.venda * data.impostoPerc) / 100;
		const valorComissao = (data.venda * data.comissaoPerc) / 100;
		
		const lucroAbsoluto =
			data.venda -
			(valorImposto + valorComissao + costs.custoOperacional);
		
		const lucroPercentual =
			data.venda > 0 ? (lucroAbsoluto / data.venda) * 100 : 0;

		const divisor = 1 - (data.impostoPerc + data.comissaoPerc) / 100;
		const pontoEquilibrio =
			divisor > 0 ? costs.custoOperacional / divisor : 0;

		return {
			venda: data.venda,
			imposto: valorImposto,
			comissao: valorComissao,
			custoOperacional: costs.custoOperacional,
			pontoEquilibrio,
			lucroAbsoluto,
			lucroPercentual,
		};
	},

	getSumFromEtapas() {
		let total = 0;
		document
			.querySelectorAll(".table_phases input[name='total_item']")
			.forEach((el) => {
				total += CurrencyManager.parseCurrency(el.value);
			});
		return total;
	},

	getSumFromCustosEspecificos() {
		let total = 0;
		document
			.querySelectorAll(".table_cost input[name='cost_value']")
			.forEach((el) => {
				total += CurrencyManager.parseCurrency(el.value);
			});
		return total;
	},

	render() {
		const c = this.calculateCosts();
		const p = this.calculatePricing();

		const table_body_costs = document.querySelector(
			".table_costs .table_body",
		);
		const table_body_pricing = document.querySelector(
			".table_pricing .table_body",
		);

		if (!table_body_costs || !table_body_pricing) return;

		table_body_costs.innerHTML = "";
		table_body_pricing.innerHTML = "";

		const addPricingRow = (table_body, label, value, isPercent = false) => {
			const template = document.getElementById("row-pricing-template");
			const clone = template.content.cloneNode(true);
			const row = clone.querySelector("tr");

			if (table_body.closest(".table_pricing")) {
				row.classList.add("row_body_pricing");
			}

			const columns = row.querySelectorAll("th");
			columns[0].innerText = label;

			// APLICAÇÃO DA FORMATAÇÃO GLOBAL
			columns[1].innerText =
				isPercent ? value.toFixed(2) + "%" : CurrencyManager.format(value);

			table_body.appendChild(row);
		};

		addPricingRow(table_body_costs, "Custo Variável", c.custoVariavel);
		addPricingRow(table_body_costs, "Custo Específico", c.custoEspecifico);
		addPricingRow(table_body_costs, "Custo Fixo", c.custoFixo);
		addPricingRow(
			table_body_costs,
			"Custos Operacionais",
			c.custoOperacional,
		);

		addPricingRow(table_body_pricing, "Impostos", p.imposto);
		addPricingRow(table_body_pricing, "Comissões", p.comissao);
		addPricingRow(
			table_body_pricing,
			"Custos Operacionais",
			p.custoOperacional,
		);
		addPricingRow(
			table_body_pricing,
			"Ponto de equilíbrio",
			p.pontoEquilibrio,
		);
		addPricingRow(table_body_pricing, "Lucro Real", p.lucroAbsoluto || 0);
		addPricingRow(
			table_body_pricing,
			"Margem de Lucro",
			p.lucroPercentual || 0,
			true,
		);
	},
};

document.addEventListener("DOMContentLoaded", () => {
	const inputsMonitorados = [
		"preco_venda",
		"impostos_percent",
		"comissoes_percent",
	];
	inputsMonitorados.forEach((id) => {
		document
			.getElementById(id)
			?.addEventListener("input", () => pricing.render());
	});

	document.addEventListener("change", function (e) {
		if (
			e.target.closest("#container-impostos") ||
			e.target.closest("#container-custos-fixos")
		) {
			pricing.render();
		}
	});

	pricing.render();
});

export function pricingRender() {
	pricing.render();
}
