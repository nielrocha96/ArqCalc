/** @format */
//EDITADO MAR-14
const actions_bar = document.querySelector(".btn_filter");

if (actions_bar) {
	actions_bar.addEventListener("click", (e) => {
		e.stopPropagation();

		const filter = document.querySelector(".container_filter");
		if (filter.closest(".active")) {
			filter.classList.remove("active");
		} else {
			filter.classList.add("active");
		}
	});
}
document.addEventListener("click", (e) => {
	const target = e.target;
	const is_filter = target.closest(".container_filter");
	const filter = document.querySelector(".container_filter.active");

	if (filter && !is_filter) {
		filter.classList.remove("active");
	}
});
