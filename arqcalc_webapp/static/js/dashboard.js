/* EDITADO MAR-13 */

document.addEventListener("DOMContentLoaded", function () {
    // Gráfico de Barras: Projetos Aprovados
    const ctxAprovados = document.getElementById("chartProjetosAprovados");
    if (ctxAprovados) {
      new Chart(ctxAprovados, {
        type: "bar",
        data: {
          labels: ["Jul", "Ago", "Set", "Out", "Nov", "Dez", "Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
          datasets: [{
            label: "Projetos",
            data: [12, 9, 15, 8, 11, 14, 10, 12, 13, 9, 11, 16],
            backgroundColor: "#5EC3F1"
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
  
    // Gráfico de Pizza: Projetos por Tipo
    const ctxTipo = document.getElementById("chartProjetosPorTipo");
    if (ctxTipo) {
      new Chart(ctxTipo, {
        type: "pie",
        data: {
          labels: ["Residencial", "Comercial", "Industrial"],
          datasets: [{
            label: "Tipos",
            data: [40, 35, 25],
            backgroundColor: ["#FF964D", "#B1D05A", "#5EC3F1"]
          }]
        }
      });
    }
  
    // Gráfico de Pizza: Projetos por Classificação
    const ctxClassificacao = document.getElementById("chartProjetosPorClassificacao");
    if (ctxClassificacao) {
      new Chart(ctxClassificacao, {
        type: "pie",
        data: {
          labels: ["A", "B", "C"],
          datasets: [{
            label: "Classificação",
            data: [50, 30, 20],
            backgroundColor: ["#FFC82F", "#5EC3F1", "#FF964D"]
          }]
        }
      });
    }
  });