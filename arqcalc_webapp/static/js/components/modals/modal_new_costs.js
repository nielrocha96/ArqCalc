/** @format */
/*
	EDITADO - ABRIL/5  
 */


document.addEventListener("click", (e) => {
    const target = e.target;

    if (target.closest(".btn_close_modal_new_costs")) {
		e.preventDefault();
		const modal_container = document.querySelector(".modal_new_costs");
		modal_container.classList.remove("active");
	}
    

    
});
