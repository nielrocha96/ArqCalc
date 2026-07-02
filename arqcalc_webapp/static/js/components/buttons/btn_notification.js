/**
 * EDITADO MAR-20
 *
 * @format
 */

// notificações.js
import { toggleModal } from "../../main.js";

const bellIcon = document.getElementById("bell_icon");
const notificationBtn = document.getElementById("notification_btn");
const container = document.getElementById("notifications-container");

// Caminhos das imagens (ajuste conforme seu static)
const ICON_NORMAL = "/static/assets/icons/notification.png";
const ICON_ACTIVE = "/static/assets/icons/notification_active.png"; // O ícone com ponto verde

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");

		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();

			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1),
				);
				break;
			}
		}
	}
	return cookieValue;
}

function setNotificationIcon(hasNew) {
	if (!bellIcon) return;
	bellIcon.src = hasNew ? ICON_ACTIVE : ICON_NORMAL;
}

async function checkNotifications() {
	// A URL deve corresponder à rota no urls.py
	const url = "/buscar_notificacoes/";

	try {
		const response = await fetch(url, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
		});

		if (!response.ok) {
			console.warn("Erro na resposta de notificações:", response.status);
			setNotificationIcon(false);
			return;
		}

		const data = await response.json();

		// Ajusta ícone sempre, com base no estado has_new
		setNotificationIcon(data.has_new);

		// Injeta o HTML renderizado pelo Django diretamente
		if (container && data.html) {
			container.innerHTML = data.html;
		}

		return data;
	} catch (error) {
		console.error("Erro ao buscar notificações:", error);
		setNotificationIcon(false);
	}
}

// Para executa na inicialização a cada refresh
// checkNotifications();

//realiza a busca por notificação após um periodo de tempo
setInterval(checkNotifications, 10800000); // 3 horas em milissegundos

// Resetar o ícone ao clicar no botão (opcional)
if (notificationBtn) {
	notificationBtn.addEventListener("click", () => {
		setNotificationIcon(false);
		toggleModal("modal_notification");
	});
}

document.addEventListener("click", (e) => {
	const target = e.target;
	if (target.closest(".btn_close_modal_notification")) {
		toggleModal("modal_notification");
	}
});

