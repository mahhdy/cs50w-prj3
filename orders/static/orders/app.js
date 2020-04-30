/*jshint esversion: 8 */
var basket = [];
const total = () => _.round(basket.reduce((a, b) => a + Number(b.price), 0), 2);

class items {
  constructor(id, name, quantity, price, topping, extra) {
    this.id = id;
    this.name = name;
    this.quantity = quantity;
    this.price = price;
    this.topping = topping;
    this.extra = extra;
    this.total = function () {
      return Number(this.quantity) * Number(this.price);
    };
  }
}
const updatePrice = el => {
  let p = $(el).find(':selected').data('price');
  $(el).next().find('span:first').text(p);
};

function addMeToBasket(th) {
  const el = $(th).closest('div').prev().find(':selected');
  const n = new items($(el).val(), $(el).text(), 1, $(el).data('price'), $(el).data('toppings'), $(el).data('extra'));
  if (!n.price) {
    return false;
  }
  askForToppings(n);
}
const loadToppings=()=>{
  var top={};
  $.ajax({
    url: 'order/toppings/',
    success: d=>{
      d.forEach(a=>top[a.name]=a.name);
    },
    async:false,
  });
  return top;
};
const askForToppings = async obj => {
  const q = ['1', '2', '3', '4', '5'];
  const Questions = [{
      title: 'Toppings 1',
      text: 'Please Select your First Toppings of ' + obj.name
    },
    {
      title: 'Toppings 2',
      text: 'Please Select your Second Toppings'
    },
    {
      title: 'Toppings 3',
      text: 'Please Select your Third Toppings'
    },
    {
      title: 'Toppings 4',
      text: 'Please Select your Forth Toppings'
    },
    {
      title: 'Toppings 5',
      text: 'Finally your Last Available Toppings is:'
    },
  ];
  if (obj.topping) {
    const topps= await loadToppings();
    await swal.mixin({
      input: 'select',
      inputOptions: topps,
      inputPlaceholder: 'Choose The Toppings',
      confirmButtonText: 'Next &rarr;',
      showCancelButton: true,
      progressSteps: q.slice(0, obj.topping)
    }).queue(Questions.slice(0, obj.topping)).then((result) => {
      if (result.value) {
        obj.topping = result.value.join(' + ');
        pushToBasket(obj);
      }
    }).catch(() => {
      Swal.insertQueueStep({
        icon: 'error',
        title: 'Unable to proceed!, Please Try Again.'
      });
    });
  } else if (obj.id == 31 || obj.id == 32) {
    const steakExtra = ['Mushrooms', 'Green Peppers', 'Onions', 'Cheese'];
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
      title: 'Steak+Cheese Extra Options',
      html: h,
      focusConfirm: false,
      preConfirm: () => $.map($('[data-steek]'), e => $(e).is(':checked')),
    });
    if (fv) {
      obj.price=Number(obj.price);
      obj.extra='';
      steakExtra.forEach((e, i) => {
        if (fv[i]) {
          obj.extra += ' ' + e;
          obj.price += 0.5;
        }
      });
    }
    pushToBasket(obj);
  } else if (obj.extra) {
    const {
      value: accept
    } = await Swal.fire({
      title: 'Subs Extra Options',
      input: 'checkbox',
      inputValue: 0,
      inputPlaceholder: 'Add extra cheese for 50 cents.',
      confirmButtonText: 'add to order',
    });
    if (accept) {
      obj.extra = 'Extra Cheese';
      obj.price += 0.5;
    } else {
      obj.extra = '';
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
  /*n.csrfmiddlewaretoken = '{{ csrf_token }}'
  $.post('order/add/', n, function (data) {
  console.log(data);
  });*/
};
const addToBasket = obj => {
  let secondLine ='';
  if (obj.topping || obj.extra) {
    secondLine =`<small class="text-muted">${obj.topping?obj.topping:''} ${obj.extra?'Plus ' + obj.extra:''}</small>`;
  }
  let dataset = '';
  for (let k in obj) {
    if (k != 'csrfmiddlewaretoken') {
      dataset += ` data-${k}="${obj[k].toString()}" `;
    }
  }
  $(`<li class="list-group-item d-flex justify-content-between lh-condensed py-1">
        <div>
          <h6 class="my-0">${obj.name}</h6>
          ${ secondLine?secondLine:'' }
        </div>
        <span class="text-muted">$${obj.price * obj.quantity} <button type="button" class="close" ${dataset}
            aria-label="Close" onclick='removeFromBasket(this)'>
            <small class="align-top ml-1" aria-hidden="true">×</small>
          </button></span>
      </li>`).appendTo('#theBasket');
};
const updateTotal = () => {
  localStorage.setItem('pizzaOrder', JSON.stringify(basket));
  $('[data-inBasket]').text(basket.length);
  $('h5+h5 strong').text('$' + total().toString());
};
const removeFromBasket = el => {
  d = $(el).data();
  basket = basket.filter(e => !(e.id == d.id && e.quantity == d.quantity && e.topping == d.topping && e.extra == d
    .extra));
  updateTotal();
  $(el).closest('li').remove();
  updateTotal();
};
const resetBasket = () => {
  basket = [];
  $('#theBasket').empty();
  updateTotal();
  return false;
};
const submitOrder= async()=>{
  const { value: accept } = await Swal.fire({
    title: 'Submit Order',
    input: 'checkbox',
    inputValue: 0,
    showCancelButton: true,
    inputPlaceholder:'Order Details Are All Correct.',
    confirmButtonText:'Continue<i class="fa fa-arrow-right"></i>',
    inputValidator: (result) => {
      return !result && 'You need to Mark the CheckBox!';
    }
  });  
  if (accept) {
    Swal.fire('Confirmation','Order is initiated, Please Check your email','success');
    resetBasket();
  }

};