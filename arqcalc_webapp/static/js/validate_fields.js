// EDITADO ABRIL/11

function validadeFieldsOfTabProspecting() {
	let isValid = true;
	let tabProspecting = document.getElementById("tab-prospeccao");
	const btnTabProspecting = document.querySelector("[data-tab='prospeccao']");

	// pega todos os radios obrigatórios
	let requiredRadios = tabProspecting.querySelectorAll(
		"input[type='radio'][required]",
	);

	// extrai nomes únicos (cada grupo)
	let groupNames = [
		...new Set(Array.from(requiredRadios).map((radio) => radio.name)),
	];

	groupNames.forEach(function (name) {
		let radios = tabProspecting.querySelectorAll(`input[name="${name}"]`);
		let isChecked = Array.from(radios).some((radio) => radio.checked);

		let fieldset = radios[0].closest("fieldset");

		// remove erro anterior
		let oldError = fieldset.querySelector(".invalid-feedback");
		if (oldError) oldError.remove();

		if (!isChecked) {
			isValid = false;

			fieldset.classList.add("is-invalid");

			let errorMessage = document.createElement("div");
			errorMessage.className = "invalid-feedback";
			errorMessage.textContent = "Selecione uma opção.";

			fieldset.appendChild(errorMessage);
		} else {
			fieldset.classList.remove("is-invalid");
		}
	});

	if (!isValid) {
		btnTabProspecting.classList.add("tab-error");
	} else {
		btnTabProspecting.classList.remove("tab-error");
	}

	return isValid;
}

function validateFieldsOfTabData() {
    let isValid = true;
    let tabData = document.getElementById("tab-dados");
    const btnTabData = document.querySelector("[data-tab='dados']");


    let requiredFields = tabData.querySelectorAll("[required]");
    let requiredInputsCustumSelects = tabData.querySelectorAll(".select_item_base button");
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add("is-invalid");
            let errorMessage = document.createElement("div");
            errorMessage.className = "invalid-feedback";
            errorMessage.textContent = "Este campo é obrigatório.";
            if (!field.nextElementSibling || !field.nextElementSibling.classList.contains("invalid-feedback")) {
                field.parentNode.insertBefore(errorMessage, field.nextSibling);
            }
        } else {
            field.classList.remove("is-invalid");
            if (field.nextElementSibling && field.nextElementSibling.classList.contains("invalid-feedback")) {
                field.nextElementSibling.remove();
            }
        }
    });

    requiredInputsCustumSelects.forEach(function (selectCustom) {
        if (!selectCustom.value.trim()) {
            isValid = false;
            selectCustom.classList.add("is-invalid");
            let errorMessage = document.createElement("div");
            errorMessage.className = "invalid-feedback";
            errorMessage.textContent = "Este campo é obrigatório.";
            if (!selectCustom.nextElementSibling || !selectCustom.nextElementSibling.classList.contains("invalid-feedback")) {
                selectCustom.parentNode.insertBefore(errorMessage, selectCustom.nextSibling);
            }
        } else {
            selectCustom.classList.remove("is-invalid");
            if (selectCustom.nextElementSibling && selectCustom.nextElementSibling.classList.contains("invalid-feedback")) {
                selectCustom.nextElementSibling.remove();
            }
        }
    });


    if (!isValid) {
        btnTabData.classList.add("tab-error");
    } else {
        btnTabData.classList.remove("tab-error");
    }
    
    return isValid;
}

function validateFieldsOfTabCustsFixed() {
    let isValid = true;
    let tabCustsFixed = document.getElementById("tab-custo");
    const btnTabCustsFixed = document.querySelector("[data-tab='custo']");

    let requiredFields = tabCustsFixed.querySelectorAll("[required]");
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add("is-invalid");
           
        } else {
            field.classList.remove("is-invalid");
           
        }
    });


    if (!isValid) {
        btnTabCustsFixed.classList.add("tab-error");
    } else {
        btnTabCustsFixed.classList.remove("tab-error");
    }

    return isValid;
}

function validateFieldsOfTabProfissiotional() {
    let isValid = true;
    let tabProfissional = document.getElementById("tab-profissional");
    const btnTabProfissional = document.querySelector("[data-tab='profissional']");
    let requiredFields = tabProfissional.querySelectorAll("[required]");
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add("is-invalid");
          
        } else {
            field.classList.remove("is-invalid");
            
        }
    });
    if (!isValid) {
        btnTabProfissional.classList.add("tab-error");
    } else {
        btnTabProfissional.classList.remove("tab-error");
    }
    return isValid;
}

function validateFieldsOfTabPhases() {
    let isValid = true;
    let tabPhases = document.getElementById("tab-etapa");
    const btnTabPhases = document.querySelector("[data-tab='etapa']");

    let requiredFields = tabPhases.querySelectorAll("[required]");

    let requiredInputsCustumSelects = tabPhases.querySelectorAll(
		".select_item_base button",
	);
   
    
    requiredFields.forEach(function (field) {
         
    
		if (!field.value.trim()) {
			isValid = false;
			field.classList.add("is-invalid");
			
		} else {
			field.classList.remove("is-invalid");
			
		}
	});

    requiredInputsCustumSelects.forEach(function (selectCustom) {
		if (!selectCustom.value.trim()) {
			isValid = false;
			selectCustom.classList.add("is-invalid");
			
		} else {
			selectCustom.classList.remove("is-invalid");
			
		}
	});


    if (!isValid) {
        btnTabPhases.classList.add("tab-error");
    } else {
        btnTabPhases.classList.remove("tab-error");
    }
    return isValid;
}

function validateFieldsOfTabPricing() {
    let isValid = true;
    let tabPricing = document.getElementById("tab-preco");
    const btnTabPricing = document.querySelector("[data-tab='preco']");
    let requiredFields = tabPricing.querySelectorAll("[required]");
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add("is-invalid");
            let errorMessage = document.createElement("div");
            errorMessage.className = "invalid-feedback";
            errorMessage.textContent = "Este campo é obrigatório.";
            if (!field.nextElementSibling || !field.nextElementSibling.classList.contains("invalid-feedback")) {
                field.parentNode.insertBefore(errorMessage, field.nextSibling);
            }
        } else {
            field.classList.remove("is-invalid");
            if (field.nextElementSibling && field.nextElementSibling.classList.contains("invalid-feedback")) {
                field.nextElementSibling.remove();
            }
        }
    });
    if (!isValid) {
        btnTabPricing.classList.add("tab-error");
    } else {
        btnTabPricing.classList.remove("tab-error");
    }
    return isValid;
}



const brn_save = document.querySelector(".btn_save");

brn_save?.addEventListener("click", function (event) {
	if (!validateFieldsOfTabData()) {
		event.preventDefault();
	}
	if (!validateFieldsOfTabCustsFixed()) {
		event.preventDefault();
	}
	if (!validateFieldsOfTabProfissiotional()) {
		event.preventDefault();
	}
	if (!validateFieldsOfTabPhases()) {
		event.preventDefault();
	}
	if (!validateFieldsOfTabPricing()) {
		event.preventDefault();
    }
    if (!validadeFieldsOfTabProspecting()) {
        event.preventDefault();
    }
});