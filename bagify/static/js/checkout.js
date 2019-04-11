function checkout() {

  const view = {
    saveBtn: document.querySelector(".js-save"),
    proceedBtn: document.querySelector(".js-proceed"),
    saveInput: document.querySelector('[name="save-address"]'),
    addressForm: document.querySelector(".js-addressForm"),
    addressStep: document.querySelector(".address-step"),
    paymentStep: document.querySelector(".payment-step"),
    addressSection: document.querySelector(".address"),
    paymentSection: document.querySelector(".payment"),
    selectButton: document.querySelector('.select-button'),

    showPayment() {
      view.paymentStep.classList.add("active");
      view.addressStep.classList.remove("active");

      view.addressSection.hidden = true;
      view.paymentSection.hidden = false;
    },

    showAddress() {
      view.paymentStep.classList.remove("active");
      view.addressStep.classList.add("active");

      view.addressSection.hidden = false;
      view.paymentSection.hidden = true;
    },

    addressFormCompleted() {
      view.addressSection.hidden = true;
      view.paymentSection.hidden = false;

      view.addressStep.classList.remove("active");
      view.addressStep.querySelector("span").classList.add("bg-success");
      view.addressStep.querySelector("i").className = "fas fa-check";

      view.paymentStep.classList.add("active");
    }
  };

  function init() {
    view.addressStep
      .querySelector("a")
      .addEventListener("click", view.showAddress);

    view.paymentStep
      .querySelector("a")
      .addEventListener("click", view.showPayment);

    view.saveBtn.addEventListener(
      "click",
      () => (view.saveInput.value = "true")
    );
    view.proceedBtn.addEventListener(
      "click",
      () => (view.saveInput.value = "false")
    );

    view.addressForm.addEventListener("submit", submitAddress);

    if(view.selectButton) {
        view.selectButton.addEventListener('click', selectAddress);
    }
  }

  function selectAddress(evt) {
      const input = document.querySelector('.select-address input:checked');
      if(input) {
          const body = {
              select: true,
              addressId: input.value
          }
          addressDetails = JSON.stringify(body)
          view.addressFormCompleted();
      }

  }

  function submitAddress(evt) {
    evt.preventDefault();

    const form = new FormData(evt.target);
    let jsonForm = {};

    for (entry of form.entries()) {
      jsonForm[entry[0]] = entry[1];
    }

    addressDetails = JSON.stringify(jsonForm)
    view.addressFormCompleted();
  }


  init();
}
checkout();
