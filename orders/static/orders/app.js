/*jshint esversion: 8 */
var basket = [];
const total = () => {
  return _.round(basket.reduce((a, b) => a + Number(b.price), 0), 2);
};
$(() => {
  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover({
    container: "body",
    html: true,
    placement: "bottom",
    sanitize: false,
    content: function () {
      return $("#login-content").html();
    },

  });
});

class items {
  constructor(id, name, quantity, price, topping, extra) {
    this.id = id;
    this.name = name.trim();
    this.quantity = Number(quantity);
    this.price = Number(price);
    this.topping = topping;
    this.extra = extra;
  }
  total() {
    return this.quantity * this.price;
  }
}
const updatePrice = (el) => {
  let p = $(el).find(":selected").data("price");
  $(el).next().find("span:first").text(p);
};

function addMeToBasket(th, page) {
  let el;
  let id = 0;
  let name = '';
  if (page == 'a') {
    el = $(th).closest("div").prev().find(":selected");
    id = $(el).val();
    name = $(el).text();
  } else if (page == 'b') {
    el = $(th);
    id = $(el).data("id");
    name = $(el).data("size") + ' ' + $(el).data("name");
  } else if (page == 'c') {
    el = $(th).closest("p").prev().find(":selected");
    id = $(el).data("id");
  }
  const n = new items(
    id,
    name.trim(),
    1,
    Number($(el).data("price")),
    $(el).data("toppings"),
    $(el).data("extra")
  );
  if (!n.price) {
    return false;
  }
  askForToppings(n);
}
const loadToppings = () => {
  var top = {};
  $.ajax({
    url: document.location.origin + "/order/toppings/",
    success: (d) => {
      d.forEach((a) => (top[a.name] = a.name));
    },
    async: false,
  });
  return top;
};
const askForToppings = async (obj) => {
  const q = ["1", "2", "3", "4", "5"];
  const Questions = [{
      title: "Toppings 1",
      text: "Please Select your First Toppings of " + obj.name,
    },
    {
      title: "Toppings 2",
      text: "Please Select your Second Toppings",
    },
    {
      title: "Toppings 3",
      text: "Please Select your Third Toppings",
    },
    {
      title: "Toppings 4",
      text: "Please Select your Forth Toppings",
    },
    {
      title: "Toppings 5",
      text: "Finally your Last Available Toppings is:",
    },
  ];
  if (obj.topping) {
    const topps = await loadToppings();
    await swal
      .mixin({
        input: "select",
        inputOptions: topps,
        inputPlaceholder: "Choose The Toppings",
        confirmButtonText: "Next &rarr;",
        showCancelButton: true,
        progressSteps: q.slice(0, obj.topping),
      })
      .queue(Questions.slice(0, obj.topping))
      .then((result) => {
        if (result.value) {
          obj.topping = result.value.join(" + ");
          pushToBasket(obj);
        }
      })
      .catch(() => {
        Swal.insertQueueStep({
          icon: "error",
          title: "Unable to proceed!, Please Try Again.",
        });
      });
  } else if (obj.id == 30 || obj.id == 45) {
    const steakExtra = ["Mushrooms", "Green Peppers", "Onions", "Cheese"];
    let h = ``;
    steakExtra.forEach((e, i) => {
      h += `<div class="custom-control custom-switch text-left">
          <input type="checkbox" data-steek class="custom-control-input" id="customSwitch${i}">
          <label class="custom-control-label" for="customSwitch${i}">${e} <span class="ml-3">(50￠)</span></label></div>`;
    });
    h += `</div>`;
    const {
      value: fv
    } = await Swal.fire({
      title: "Steak+Cheese Extra Options",
      html: h,
      focusConfirm: false,
      preConfirm: () => $.map($("[data-steek]"), (e) => $(e).is(":checked")),
    });
    if (fv) {
      obj.price = Number(obj.price);
      obj.extra = "";
      steakExtra.forEach((e, i) => {
        if (fv[i]) {
          obj.extra += " " + e;
          obj.price += 0.5;
        }
      });
    }
    pushToBasket(obj);
  } else if (obj.extra) {
    const {
      value: accept
    } = await Swal.fire({
      title: "Subs Extra Options",
      input: "checkbox",
      inputValue: 0,
      inputPlaceholder: "Add extra cheese for 50 cents.",
      confirmButtonText: "add to order",
    });
    if (accept) {
      obj.extra = "Extra Cheese";
      obj.price += 0.5;
    } else {
      obj.extra = "";
    }
    pushToBasket(obj);
  } else {
    pushToBasket(obj);
  }
};
const pushToBasket = (obj) => {
  basket.push(obj);
  addToBasket(obj);
  updateTotal();
  pushToServer();
};
const pushToServer = () => {
  if ($('#nav_profile').length) {
    $.post(document.location.origin + '/order/add/', {
      csrfmiddlewaretoken: $('#token').text(),
      obj: JSON.stringify(basket)
    });
  }
};
const addToBasket = (obj) => {
  let secondLine = "";
  if (obj.topping || obj.extra) {
    secondLine = `<small class="text-muted">${obj.topping ? obj.topping : ""} ${
      obj.extra ? "+ " + obj.extra : ""
    }</small>`;
  }
  let dataset = "";
  for (let k in obj) {
    if (k != "csrfmiddlewaretoken") {
      dataset += ` data-${k}="${obj[k].toString()}" `;
    }
  }
  $(`<li class="list-group-item d-flex justify-content-between lh-condensed py-1">
        <div>
          <h6 class="my-0 mr-auto text-left">${obj.name}</h6>
          ${secondLine ? secondLine : ""}
        </div>
        <span class="text-muted">$${
          obj.price * obj.quantity
        } <button type="button" class="close" ${dataset}
            aria-label="Close" onclick='removeFromBasket(this)'>
            <small class="align-top ml-1" aria-hidden="true">×</small>
          </button></span>
      </li>`).appendTo("#theBasket");
};
const updateTotal = () => {
  localStorage.setItem("pizzaOrder", JSON.stringify(basket));
  $("[data-inBasket]").text(basket.length);
  $("h5+h5 strong").text("$" + total().toString());
};
const removeFromBasket = (el) => {
  d = $(el).data();
  basket = basket.filter(
    (e) =>
    !(
      e.id == d.id &&
      e.quantity == d.quantity &&
      e.topping == d.topping &&
      e.extra == d.extra
    )
  );
  updateTotal();
  $(el).closest("li").remove();
  updateTotal();
  pushToServer();
};
const resetBasket = () => {
  basket = [];
  $("#theBasket").empty();
  updateTotal();
  return false;
};
const submitOrder = async () => {
  if (total() == 0) {
    return Swal.fire(
      "Empty Cart",
      "Please First Add some items to your Cart",
      "warning"
    );
  }
  if ($('#nav_profile').length==0) {
    await Swal.fire(
      "Need Login",
      "Please Login Before Submitting the Order",
      "warning"
    );
    await $('a.nav-link[data-toggle="popover"]').trigger('click'); 
    return $('h3.popover-header').add('div.popover-body').addClass('bg-danger');
  }  
  $("#theBasket li").addClass("disabled");
  const {
    value: accept
  } = await Swal.fire({
    title: "Confirm Order",
    html: $("#theBasket")[0].outerHTML,
    input: "checkbox",
    inputValue: 0,
    showCancelButton: true,
    inputPlaceholder: `Is above order details with total of ${total()}$ correct?`,
    confirmButtonText: 'Continue<i class="fa fa-arrow-right"></i>',
    inputValidator: (result) => {
      return !result && "You need to confirm teh details to submit the order!";
    },
  });
  if (accept) {
    $.post(document.location.origin + '/order/submit/',{csrfmiddlewaretoken:$('#token').text(),obj:JSON.stringify(basket)}).done(d=>{
      Swal.fire(
        "Confirmation",
        `Order #${d.orderNo} is initiated, Please Check your email`,
        "success"
      );
      resetBasket();
      window.location.replace(document.location.origin);
    }).fail((d)=>alert('Something was wrong! try again!')
    );    
  }
  $("#theBasket li").removeClass("disabled");
};