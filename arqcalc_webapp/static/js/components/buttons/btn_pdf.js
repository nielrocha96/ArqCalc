/** @format */
// # EDITADO - ABRIL/12

const btn_pdf = document.getElementById("btn_pdf");

document.addEventListener("click", (event) => {
	const target = event.target.closest("#btn_pdf");

	if (target) {
		const projetoId = target.getAttribute("data-id");

		// 1. Pega a moeda do localStorage
		const savedCurrency = localStorage.getItem("user_currency") || "BRL";

		// 2. Monta a URL exatamente como a View espera
		const urlDestino = `/exportar_projeto_pdf/${projetoId}/${savedCurrency}/`;

		// 3. Redireciona o navegador para a URL
		// Isso faz o navegador "bater" na rota e iniciar o download/abertura do PDF
		window.location.href = urlDestino;

	}
});