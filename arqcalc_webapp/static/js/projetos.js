/** @format */
// Arquivo com código devalidação para a tela de novo_projeto
import "./validate_fields.js";

import { add_item_table } from "./add_item_table.js";
import { pricingRender } from "./components/tabs/tab_pricing.js";
import { CurrencyManager } from "./main.js";

/**
 * # EDITADO - ABRIL/11

 */

// Lista de profissionais global
export let profs = [];

// Variáveis de controle de estado de ordenação
let sortState = {
	etapas: { column: null, direction: 0 },
	profissionais: { column: null, direction: 0 },
};

// Converte tempo no formato "HH:MM" para um número decimal representando horas
const timeToFloat = (tempo) => {
	// Se não houver valor ou não for string, retorna 0 ou o próprio número
	if (!tempo || !String(tempo).includes(":")) return parseFloat(tempo) || 0;

	const [horas, minutos] = tempo.split(":").map(Number);

	const tempoFormated = horas + minutos / 60;
	// Retorna a soma das horas com a fração dos minutos
	return tempoFormated;
};

// Converte um número decimal representando horas para o formato "HH:MM"
const floatToTime = (valorFloat) => {
	if (!valorFloat || isNaN(valorFloat)) return "00:00";

	// 1. Pega a parte inteira (horas)
	const horas = Math.floor(valorFloat);

	// 2. Pega a sobra decimal e transforma em minutos (arredondando para evitar 29.999)
	const minutos = Math.round((valorFloat - horas) * 60);

	// 3. Formata para ter sempre 2 dígitos (ex: "1" vira "01")
	const hFormatadas = String(horas).padStart(2, "0");
	const mFormatados = String(minutos).padStart(2, "0");

	return `${hFormatadas}:${mFormatados}`;
};

// Função para criar a lista de profissionais a partir da tabela e atualizar os selects
const create_professional_list = () => {
	const tab_profissionais = document.querySelector("#tab-profissional");
	if (!tab_profissionais) return;

	const profissionais_table_body =
		tab_profissionais.querySelectorAll(".table_body tr");

	// Limpa o array para re-popular com dados atualizados
	profs = [];

	profissionais_table_body.forEach((prof, index) => {
		const inputs_prof = Array.from(prof.querySelectorAll("input")).slice(1);

		// Validação: verifica se os campos (nome e valor/hora) estão preenchidos
		const validate_inputs = inputs_prof.every(
			(inp) => inp.value.trim() !== "",
		);

		if (validate_inputs && inputs_prof.length > 0) {
			const prof_obj = { id: index + 1 };
			inputs_prof.forEach((inp) => {
				prof_obj[inp.name] = inp.value;
			});
			// Assume que o input com name="nome" ou "name" existe
			prof_obj.nome =
				prof_obj.name ||
				prof_obj.nome_profissional ||
				inputs_prof[0].value;
			profs.push(prof_obj);
		}
	});

	// Atualiza todos os selects de profissionais existentes na tela
	update_all_professional_selects();
};

// Função para atualizar os selects de profissionais em toda a aplicação
export const update_all_professional_selects = () => {
	const prof_select_containers = document.querySelectorAll(
		".professional_select_container, #professional_select",
	);

	prof_select_containers.forEach((container) => {
		const btn_selec = container.querySelector(".selected_item_base");
		const list = container.querySelector(".custom_options_base");

		if (profs.length > 0) {
			// Habilita e remove o aviso
			if (btn_selec) {
				btn_selec.removeAttribute("disabled");
				btn_selec.removeAttribute("title"); // Remove o aviso pois agora há dados
			}
			if (list) {
				list.innerHTML = "";
				profs.forEach((prof) => {
					const li = document.createElement("li");
					li.setAttribute("data-value", prof.nome);
					li.setAttribute("data-id", prof.id);
					li.className = `option-item`;
					li.textContent = prof.nome;
					list.appendChild(li);
				});
			}
		} else {
			// Garante que continue desabilitado se a lista estiver vazia
			if (btn_selec) {
				btn_selec.setAttribute("disabled", "true");
				btn_selec.setAttribute(
					"title",
					"Adicione profissionais na aba 'Profissionais' para habilitar",
				);
			}
		}
	});
};

// Função para adicionar uma nova etapa (bloco completo) com uma linha de item já criada
export const add_phase = () => {
	const listPhaseContainer = document.querySelector("#phases_list");
	const phaseTemplate = document.querySelector("#phase-template");

	const id_temp = listPhaseContainer.querySelectorAll(".phase_container").length + 1;

	const etapas_container = document.querySelector(".etapas-container");

	const rowTemplate = etapas_container.querySelector("#row-body-template"); // Template da linha

	if (!listPhaseContainer || !phaseTemplate) {
		console.error("Containers de etapa não encontrados.");
		return;
	}
	// Gerar um ID temporário único para a nova etapa, o id recebe o ultimo id do array de etapas + 1 ou começa em 1 se não houver etapas
	const tempId = `temp-${id_temp}`;
	let phaseHtml = phaseTemplate.innerHTML.replace(/__prefix__/g, tempId);

	const tempDiv = document.createElement("div");
	tempDiv.innerHTML = phaseHtml;
	const newPhase = tempDiv.firstElementChild;

	// Configura identificadores
	newPhase.dataset.id = tempId;

	// Adiciona a primeira linha obrigatória na tabela da nova etapa
	const tableBody = newPhase.querySelector(".table_body");

	if (tableBody && rowTemplate) {
		// Clonamos o conteúdo do template de linha
		const rowContent = rowTemplate.content.cloneNode(true);

		// Se houver lógica de numeração de itens, podemos ajustar aqui
		// Ex: rowContent.querySelector('.item-index').textContent = "1";

		tableBody.appendChild(rowContent);
	} else {
		console.warn(
			"Aviso: .table_body ou #row-body-template não encontrados ao criar etapa.",
		);
	}

	listPhaseContainer.appendChild(newPhase);

	// Inicialização de componentes UI (Selects, Máscaras de Moeda, etc)
	if (typeof update_all_professional_selects === "function") {
		update_all_professional_selects();
	}

	if (window.CurrencyManager) {
		window.CurrencyManager.updateUI();
	}

	newPhase.scrollIntoView({ behavior: "smooth" });
};

// Função para calcular o custo total de um item com base no tempo e valor/hora
function calculateCostsOfItem(tempo, valor_hora) {
	// 1. Validamos apenas o valor_hora aqui, pois o tempo pode ser String "02:30"
	if (!valor_hora || isNaN(valor_hora)) {
		return 0;
	}

	let tempoEmHoras = 0;

	// 2. Verifica se o tempo contém ":" (formato HH:MM)
	if (String(tempo).includes(":")) {

		tempoEmHoras = timeToFloat(tempo);
		
	} else {
		// 3. Se não tem ":", assume que já é um número decimal (ex: 2 ou 2.5)
		tempoEmHoras = parseFloat(tempo) || 0;
	}

	// 4. Cálculo final
	const custoTotal = tempoEmHoras * valor_hora;


	return custoTotal;
}

const renderizarTabelaEtapas = (dadosEtapas) => {
	const tableEtapa = document.querySelector(
		"#resumo-custos-etapas .table_body",
	);
	if (!tableEtapa) return;

	tableEtapa.innerHTML = "";

	// Cálculo do custo total global para a proporção (opcional, se já não vier calculado)
	const custoGlobal = dadosEtapas.reduce((acc, curr) => acc + curr.custo, 0);

	dadosEtapas.forEach((item) => {
		const proporcao =
			custoGlobal > 0 ? (item.custo / custoGlobal) * 100 : 0;

		tableEtapa.innerHTML += `
            <tr class="row_body_table">
                <th class="checkbox_collumn_body"></th>
                <th class="content_collumn_body">${floatToTime(item.tempo)}</th>
                <th class="content_collumn_body">${item.etapa}</th>
                <th class="content_collumn_body">${CurrencyManager.format(item.custo)}</th>
                <th class="content_collumn_body">${proporcao.toFixed(1)}%</th>
                <th class="action_collumn_body"></th>
            </tr>`;
	});
};

function renderizarTabelaProfissionais(profissionais) {

	const tableProf = document.querySelector("#resumo-custos-profissionais .table_body");
    if (!tableProf) return;

    tableProf.innerHTML = ""; 
    
    // Se por algum motivo 'profissionais' ainda não for array, fazemos um fallback seguro
	const lista = Array.isArray(profissionais) ? profissionais : Object.values(profissionais);
	
	if (lista) {
		lista.forEach((dados) => {
			tableProf.innerHTML += `
                <tr class="row_body_table">
                    <th class="checkbox_collumn_body"></th>
                    <th class="content_collumn_body">${floatToTime(dados.tempoTotal)}</th>
                    <th class="content_collumn_body">${dados.cargo}</th>
                    <th class="content_collumn_body">${CurrencyManager.format(dados.custoTotal)}</th>
                    <th class="content_collumn_body">${dados.proporcao.toFixed(1)}%</th>
                    <th class="action_collumn_body"></th>
                </tr>`;
		});
	}
}

const getTableType = (element) => {
	if (element.closest("#resumo-custos-etapas")) return "etapas";
	if (element.closest("#resumo-custos-profissionais")) return "profissionais";
	return null;
};

const resetSortIcons = (table) => {
	if (!table) return;

	table.querySelectorAll(".order_by").forEach((el) => {
		el.classList.remove("active");

		const icon = el.querySelector(".order_by_icon");
		if (icon) icon.classList.remove("rotate-180");
	});
};

const updateSortVisual = (btn, icon, direction) => {
	if (!btn || !icon) return;
	let title = "Ordenação padrão";

	if (direction === 0) {
		btn.classList.remove("active");
		icon.classList.remove("rotate-180");
		title = "Ordenação padrão";
	} else if (direction === 1) {
		btn.classList.add("active");
		icon.classList.remove("rotate-180");
		title = "Ordenado crescente";
	} else {
		btn.classList.add("active");
		icon.classList.add("rotate-180");
		title = "Ordenado decrescente";
	}

	btn.setAttribute("title", title);
};

document.addEventListener("DOMContentLoaded", function () {
	// --- MÓDULO 1: NAVEGAÇÃO POR ABAS ---
	const tabs = document.querySelectorAll(".tab");
	const tabContents = document.querySelectorAll(".tab-content");

	tabs.forEach((tab) => {
		tab.addEventListener("click", function () {
			tabs.forEach((t) => t.classList.remove("active"));
			tabContents.forEach((c) => c.classList.remove("active"));

			this.classList.add("active");
			const contentId = "tab-" + this.dataset.tab;
			const content = document.querySelector(`#${contentId}`);

			if (content) content.classList.add("active");

			if (this.dataset.tab == "etapa") {
				create_professional_list();
			}
		});
	});

	// --- CACHE DE ELEMENTOS DO DOM ---
	const form = document.querySelector(".novo_projeto_form");

	// --- DELEGAÇÃO DE EVENTOS GERAIS ---
	if (form) {
		form.addEventListener("click", (e) => {
			const target = e.target;

			//=============== NOVO PROJETO =======================//

			// ADICIONAR CUSTO ESPECIFICO (VIA TABELA E TEMPLATE)
			if (target.closest(".add-custo-btn")) {
				e.preventDefault();
				const tab_container = target.parentNode;
				add_item_table(tab_container);
			}

			// ADICIONAR PROFISSIONAL
			if (target.closest(".add-profissional-btn")) {
				e.preventDefault();
				const tab_container = target.parentNode;
				add_item_table(tab_container);
			}

			// ADICIONAR ITEM NA ETAPA
			if (target.closest(".btn-add-item-etapa")) {
				e.preventDefault();

				const etapas_footer = target.parentNode;
				const tab_container = etapas_footer.parentNode;

				add_item_table(tab_container);
			}

			// ADICIONAR NOVA ETAPA (BLOCO COMPLETO)
			if (target.closest(".add-etapa-btn ")) {
				e.preventDefault();

				add_phase();
			}
			// ABRIR E FECHAR ETAPA
			if (target.closest(".icon_drop_phase")) {
				const phaseContainer = target.closest(".phase_container");

				//  Encontra o ícone (ou a div do ícone) para rotacionar
				const icon = target.closest(".icon_drop_phase");

				if (phaseContainer && icon) {
					// Alterna a classe no container (para esconder a tabela/conteúdo)
					phaseContainer.classList.toggle("close_phase");

					// Alterna a rotação no ícone
					icon.classList.toggle("rotate_icon");
				}
			}

			// Deletar qualquer item (Atualizado para suportar TR da tabela)
			const deleteBtn = target.closest(".delete-btn");
			if (deleteBtn) {
				e.preventDefault();
				const itemParaRemover = deleteBtn.closest(
					"tr, .custo-item, .profissional-item, .etapa-bloco, .item-tarefa",
				);
				if (itemParaRemover) itemParaRemover.remove();
			}

			// Expandir/Recolher etapa
			const toggleBtn = target.closest(".toggle-etapa-btn");
			if (toggleBtn) {
				e.preventDefault();
				toggleBtn.closest(".etapa-bloco").classList.toggle("is-closed");
			}

			if (target.closest(".order_by")) {
				// ======================
				//       ORDENAÇÃO
				// ======================

				 const btn = target.closest(".order_by");
					const tableType = getTableType(btn);
					if (!tableType) return;

					const column = btn.getAttribute("data-column");
					const icon = btn.querySelector(".order_by_icon");

					const state = sortState[tableType];

					// Troca de coluna → reset
					if (state.column !== column) {
						resetSortIcons(btn.closest("table"));
						state.column = column;
						state.direction = 1;
					} else {
						state.direction = (state.direction + 1) % 3;
					}

					updateSortVisual(btn, icon, state.direction);

					renderizarResumoCompleto();
			}

		});

		// OUVE ALTERAÇÕES EM INPUTS
		form.addEventListener("input", (e) => {
			// ETAPA
			const target = e.target;

			if (target.closest("#tab-etapa")) {
				renderizarResumoCompleto();
			}

			// Atualiza o campo total do item (ETAPAS) com base no tempo e tabela de resumo  e de precificação
			if (target.name === "time") {
				const row = target.closest("tr");
				if (!row) return;

				const inputTempo = row.querySelector('input[name="time"]');
				const inputTotal = row.querySelector(
					'input[name="total_item"]',
				);
				// O ID do profissional é armazenado no input hidden do componente select_base
				const inputResponsavel = row.querySelector(
					'input[name="responsible"]',
				);
				const profId = inputResponsavel ? inputResponsavel.id : null;

				if (inputTempo && inputTotal) {
					const tempo = inputTempo.value;

					// Busca o valor/hora na lista global de profissionais 'profs'
					const profData = profs.find((p) => p.id == profId);

					// Atualiza o campo Total do Item formatado numero float para o cálculo e formata para moeda apenas na exibição
					const valorHora =
						profData ?
							CurrencyManager.parseCurrency(profData.value_hour)
						:	0;

					// Realiza o cálculo para o campo Total do Item em etapa
					const total = calculateCostsOfItem(tempo, valorHora);

					// Atualiza o campo Total do Item formatado como moeda
					inputTotal.value = CurrencyManager.format(total);

					//Armazena o valor numérico puro em um data-attribute
					// caso precise recalcular algo depois sem ter que "limpar" a string da moeda
					inputTotal.dataset.rawTotal = total;
				}

				renderizarResumoCompleto();
				pricingRender();
				CurrencyManager.updateUI();
			}

			// Atualiza tabela de precificação ao adicionar/alterar Custos Especificos
			if (target.name === "cost_value") {
				pricingRender();
				CurrencyManager.updateUI();
			}
			// ESCUTADOR PARA FORMATAÇÃO DE MOEDA NOS INPUTS
			if (
				e.target.classList.contains("input-currency") ||
				e.target.classList.contains("currency-input")
			) {
				CurrencyManager.formatInput(e.target);
			}
		});
	}

	// Renderização inicial do resumo e atualização de UI
	document.addEventListener("change", (e) => {
		const target = e.target;

		// Atualiza o campo total do item com base no selec de responsavel e tabela de resumo e de precificação
		if (target.name === "responsible") {
			const row = target.closest("tr");
			if (!row) return;

			const inputTempo = row.querySelector('input[name="time"]');
			const inputTotal = row.querySelector('input[name="total_item"]');

			// O ID do profissional é armazenado no input hidden do componente select_base
			const inputResponsavel = row.querySelector(
				'input[name="responsible"]',
			);
			const profId = inputResponsavel ? inputResponsavel.id : null;

			if (inputTempo && inputTotal) {
				const tempo = inputTempo.value;

				// Busca o valor/hora na lista global de profissionais 'profs'
				const profData = profs.find((p) => p.id == profId);
				const valorHora =
					profData ? CurrencyManager.parseCurrency(profData.value_hour) : 0;

				// Realiza o cálculo para o campo Total do Item em etapa
				const total = calculateCostsOfItem(tempo, valorHora);

				// Atualiza o campo Total do Item formatado como moeda
				inputTotal.value = CurrencyManager.format(total);

				//Armazena o valor numérico puro em um data-attribute
				// caso precise recalcular algo depois sem ter que "limpar" a string da moeda
				inputTotal.dataset.rawTotal = total;
			}

			renderizarResumoCompleto();
			pricingRender();
			CurrencyManager.updateUI();
		}
	});

	const resumoService = {
		extrairDadosEtapas() {
			const itens = [];
			const rows = document.querySelectorAll(
				".phase_container .table_body tr",
			);

			rows.forEach((row) => {
				const profId = row.querySelector(
					'input[name="responsible"]',
				)?.id;

				const itemId = row.dataset.id || null;

				const profData = profs.find((p) => p.id == profId);

				const valorHora =
					profData ? CurrencyManager.parseCurrency(profData.value_hour) : 0;
				
				const tempo = row.querySelector('input[name="time"]')?.value || 0;
					
				
				const total = calculateCostsOfItem(tempo, valorHora);

				itens.push({
					id: profId || null,
					tempo: timeToFloat(tempo),
					cargo: profData?.position || "sem nome",
					valorTotal: total,
					profissional: profData?.nome || "Não definido",
				});
			});
			return itens;
		},

		gerarResumoConsolidado() {
			const todosItens = this.extrairDadosEtapas();

			const consolidado = {};
			let custoGeralProjeto = 0;

			// Primeiro passo: Agrupar e somar o total geral
			todosItens.forEach((item) => {
				if (!consolidado[item.id]) {
					consolidado[item.id] = {
						responsavel: item.profissional,
						tempoTotal: 0,
						custoTotal: 0,
						cargo: item.cargo,
					};
				}
				consolidado[item.id].tempoTotal += item.tempo;
				consolidado[item.id].custoTotal += item.valorTotal;
				custoGeralProjeto += item.valorTotal;
			});

			// Segundo passo: Calcular a porcentagem
			Object.keys(consolidado).forEach((nome) => {
				const custoIndiv = consolidado[nome].custoTotal;
				consolidado[nome].proporcao =
					custoGeralProjeto > 0 ?
						(custoIndiv / custoGeralProjeto) * 100
					:	0;
			});

			return {
				profissionais: consolidado,
				totalProjeto: custoGeralProjeto,
			};
		},
	};

	const resumoEtapaService = {
		gerarResumoEtapas() {
			const resumoEtapas = [];
			// Seleciona cada bloco de etapa (cada container que contém uma tabela e um nome)
			const blocosEtapas = document.querySelectorAll(".phase_container");

			blocosEtapas.forEach((bloco, index) => {
				// 1. Captura o nome da etapa (input no topo do bloco)
				const nomeEtapa =
					bloco.querySelector(`input[name="phase_name"]`)?.value ||
					"Etapa sem nome";

				const rows = bloco.querySelectorAll(".table_body tr");
				let custoTotalEtapa = 0;
				const temposPorProfissional = {};

				rows.forEach((row) => {
					// Captura ID do responsável e tempo do item
					const profId = row.querySelector(
						'input[name="responsible"]',
					)?.id;
					const tempoItem = timeToFloat(row.querySelector('input[name="time"]')?.value) || 0;
					
					// Cálculo do Custo do Item
					const profData = profs.find((p) => p.id == profId);
					const valorHora =
						profData ? CurrencyManager.parseCurrency(profData.value_hour) : 0;
					
					custoTotalEtapa += calculateCostsOfItem(tempoItem, valorHora);

					// Regra de Tempo: Agrupar tempo por profissional dentro desta etapa
					if (profId) {
						temposPorProfissional[profId] =
							(temposPorProfissional[profId] || 0) + tempoItem;
					} else {
						temposPorProfissional[0] = 0
					}
				});

				// O tempo total da etapa é o maior resultado da soma dos tempos acumulados de cada profissional que trabalhou nela
				const tempoTotalEtapa = Math.max(...Object.values(temposPorProfissional));

				resumoEtapas.push({
					etapa: nomeEtapa,
					tempo: tempoTotalEtapa,
					custo: custoTotalEtapa,
					proporcao: 0,
				});
			});

			 //  CALCULAR PROPORÇÃO
			const custoGlobal = resumoEtapas.reduce((acc, item) => acc + item.custo, 0);

			resumoEtapas.forEach((item) => {
				item.proporcao = custoGlobal > 0
					? (item.custo / custoGlobal) * 100
					: 0;
			});


			return resumoEtapas;
		},
	};

	const renderizarResumoCompleto = () => {
		// --- Renderiza Resumo por Profissional ---
		const resultadoConsolidado = resumoService.gerarResumoConsolidado();

		let profissionais = resultadoConsolidado.profissionais;
		if (profissionais && !Array.isArray(profissionais)) {
			profissionais = Object.values(profissionais);
		}

		// --- Lógica de Ordenação ---
		if (
			sortState.profissionais.column &&
			sortState.profissionais.direction !== 0
		) {
			const mapProf = {
				"total-h": "tempoTotal",
				cargo: "cargo",
				custo: "custoTotal",
				"proporcao-de-custo": "proporcao",
			};

			const key = mapProf[sortState.profissionais.column];
						
			if (key) {

				profissionais.sort((a, b) => {
					let valA = a[key];
					let valB = b[key];

					// 🔢 TEMPO (HH:MM → float)
					if (key === "tempoTotal") {
						valA = Number(valA);
						valB = Number(valB);
					}

					// 💰 CUSTO (moeda → número)
					else if (key === "custoTotal") {
						valA =
							typeof valA === "string" ?
								CurrencyManager.parseCurrency(valA)
							:	valA;

						valB =
							typeof valB === "string" ?
								CurrencyManager.parseCurrency(valB)
							:	valB;
					}

					// 📊 PROPORÇÃO (% → número)
					else if (key === "proporcao") {
						valA =
							typeof valA === "string" ?
								parseFloat(valA.replace("%", ""))
							:	valA;

						valB =
							typeof valB === "string" ?
								parseFloat(valB.replace("%", ""))
							:	valB;
					}

					// 🔤 STRING (cargo)
					else {
						valA = String(valA).toLowerCase();
						valB = String(valB).toLowerCase();
					}

					// 🔄 DIREÇÃO
					if (valA < valB) {
						return sortState.profissionais.direction === 1 ? -1 : 1;
					}
					if (valA > valB) {
						return sortState.profissionais.direction === 1 ? 1 : -1;
					}
					return 0;
				});
			}
		}

		renderizarTabelaProfissionais(profissionais);

		// --- Renderiza Resumo por Etapa ---
		let dadosEtapas = resumoEtapaService.gerarResumoEtapas();

		// Lógica de ordenação das etapas
		if (sortState.etapas.column && sortState.etapas.direction !== 0) {
			const mapEtapa = {
				"total-h": "tempo",
				cargo: "etapa",
				custo: "custo",
				"proporcao-de-custo": "proporcao",
			};

			
			const key = mapEtapa[sortState.etapas.column];

			if (key) {
				dadosEtapas.sort((a, b) => {
					let valA = a[key];
					let valB = b[key];

					// Tempo
					if (key === "tempo") {
						valA = Number(valA);
						valB = Number(valB);
					}

					// Custo
					else if (key === "custo") {
						valA =
							typeof valA === "string" ?
								CurrencyManager.parseCurrency(valA)
							:	valA;

						valB =
							typeof valB === "string" ?
								CurrencyManager.parseCurrency(valB)
							:	valB;
					}

					// Etapa (string)
					else {
						valA = String(valA).toLowerCase();
						valB = String(valB).toLowerCase();
					}

					if (valA < valB) {
						return sortState.etapas.direction === 1 ? -1 : 1;
					}
					if (valA > valB) {
						return sortState.etapas.direction === 1 ? 1 : -1;
					}
					return 0;
				});
			}
		}

		// Passa os dados já ordenados para a função de renderização
		renderizarTabelaEtapas(dadosEtapas);
	};;;

	renderizarResumoCompleto();
	CurrencyManager.updateUI();
});
