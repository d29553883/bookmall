function memberstatus() {
  fetch("/api/user", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((res) => {
      if (res.data !== null) {
        document.getElementById("logout_button").style.display = "flex";
        document.getElementById("login_button").style.display = "none";
      } else {
        document.getElementById("logout_button").style.display = "none";
        document.getElementById("login_button").style.display = "flex";
      }
    });
}
memberstatus();

function userinfo() {
  fetch("/api/user")
    .then(function (response) {
      return response.json();
    })
    .then((result) => {
      if (result.data !== null) {
        let data = result.data;
        let username = document.getElementById("name");
        username.value = data.name;
        let email = document.getElementById("email");
        email.value = data.email;
      }
    });
}
userinfo();

function cleanCart() {
  let container = document.getElementsByClassName("container")[0];
  container.innerHTML = "";
  let cartEmpty = document.createElement("div");
  cartEmpty.className = "cartEmpty";
  let img = document.createElement("img");
  img.src = "../static/Cart illustartion.svg";
  let cartTextBox = document.createElement("div");
  cartTextBox.id = "cartTextBox";
  let cartText = document.createTextNode("你的購物車沒有商品");
  cartEmpty.appendChild(img);
  cartTextBox.appendChild(cartText);
  container.appendChild(cartEmpty);
  cartEmpty.appendChild(cartTextBox);
  let backBtn = document.createElement("button");
  backBtn.id = "backBtn";
  let backBtntextBox = document.createElement("tag");
  let backBtntext = document.createTextNode("現在就去逛逛吧 !");
  backBtntextBox.appendChild(backBtntext);
  backBtn.appendChild(backBtntextBox);
  cartEmpty.appendChild(backBtn);
  backBtn.addEventListener("click", function () {
    location.assign("/");
  });
}

if (document.readyState == "loading") {
  document.addEventListener("DOMContentLoaded", cartInfo);
} else {
  cartInfo();
}

function cartInfo() {
  fetch("/api/addCart")
    .then(function (response) {
      return response.json();
    })
    .then((result) => {
      if (result.error !== true) {
        if (result.data !== null) {
          let data = result.data;
          let name_list = [];
          let author_list = [];
          let id_list = [];
          let price_list = [];
          let image_list = [];
          let category_list = [];
          let stock_list = [];

          for (let i = 0; i < data.length; i++) {
            name_list.push(data[i].name);
            author_list.push(data[i].author);
            id_list.push(data[i].id);
            price_list.push(data[i].price);
            category_list.push(data[i].category);
            image_list.push(data[i].image);
            stock_list.push(data[i].stock);
          }
          for (let i = 0; i < data.length; i++) {
            let cart_items = document.getElementsByClassName("cart-items")[0];
            let cartItemBox = document.createElement("div");
            cartItemBox.className = "cartItemBox";
            let cartItemImage = document.createElement("div");
            cartItemImage.className = "cart-item-image";
            let image = document.createElement("img");
            image.src = image_list[i];
            let cartItemText = document.createElement("div");
            cartItemText.className = "cart-item-text";
            let name_box = document.createElement("div");
            name_box.className = "name_box";
            let nameTextNode = document.createTextNode(
              "書名 : " + name_list[i]
            );
            let author_box = document.createElement("div");
            let authorTextNode = document.createTextNode(
              "作者 : " + author_list[i]
            );
            let stock_box = document.createElement("div");
            stock_box.className = "stock_box";
            let stockText = document.createTextNode("剩餘 : " + stock_list[i]);
            let cart_price = document.createElement("div");
            cart_price.className = "price_box";
            let priceTextNode = document.createTextNode(price_list[i] + " 元");
            let cart_quantity_box = document.createElement("div");
            cart_quantity_box.id = "cart_quantity_box";
            let cart_quantity = document.createElement("input");
            cart_quantity.className = "cart_quantity";
            cart_quantity.setAttribute("type", "number");
            cart_quantity.value = 1;
            cart_quantity.addEventListener("change", quantityChanged);
            cart_quantity.addEventListener("click", updateCartTotal);
            let delete_button = document.createElement("div");
            delete_button.id = "delete";
            delete_button.setAttribute("type", "button");
            let icon = document.createElement("img");
            icon.id = id_list[i];
            icon.setAttribute("onclick", "deleteBook(" + icon.id + ")");
            icon.src = "../static/icon_delete.svg";
            delete_button.appendChild(icon);
            name_box.appendChild(nameTextNode);
            author_box.appendChild(authorTextNode);
            stock_box.appendChild(stockText);
            cart_quantity_box.appendChild(cart_quantity);
            cartItemText.appendChild(name_box);
            cartItemText.appendChild(author_box);
            cartItemText.appendChild(stock_box);
            cart_price.appendChild(priceTextNode);
            cartItemImage.appendChild(image);
            cartItemBox.appendChild(cartItemImage);
            cartItemBox.appendChild(cartItemText);
            cartItemBox.appendChild(cart_price);
            cartItemBox.appendChild(cart_quantity_box);
            cartItemBox.appendChild(delete_button);
            cart_items.appendChild(cartItemBox);
            let quantity = cart_quantity.value;
            let cart_total_price =
              document.getElementsByClassName("cart-total-price")[0];
            let sum = 0;
            for (let x = 0; x < price_list.length; x++) {
              sum += price_list[x] * quantity;
            }
            cart_total_price.innerText = sum + " 元";
          }
        } else {
          cleanCart();
        }
      } else {
        location.assign("/");
      }
    });
}

function updateCartTotal() {
  let cart_items = document.getElementsByClassName("cart-items")[0];
  let cartItemBoxs = cart_items.getElementsByClassName("cartItemBox");
  fetch("/api/addCart")
    .then(function (response) {
      return response.json();
    })
    .then((result) => {
      if (result.error !== true) {
        if (result.data !== null) {
          let data = result.data;
          let price_list = [];
          let sum = 0;
          for (let i = 0; i < data.length; i++) {
            price_list.push(data[i].price);
          }
          for (let i = 0; i < cartItemBoxs.length; i++) {
            let cartItemBox = cartItemBoxs[i];
            let price = Number(
              cartItemBox
                .getElementsByClassName("price_box")[0]
                .innerText.replace(" 元", "")
            );
            let quantity =
              cartItemBox.getElementsByClassName("cart_quantity")[0].value;
            let cart_total_price =
              document.getElementsByClassName("cart-total-price")[0];
            sum = sum + price * quantity;
            cart_total_price.innerText = sum + " 元";
          }
        } else {
          cleanCart();
        }
      } else {
        location.assign("/");
      }
    });
}
updateCartTotal();
function quantityChanged(event) {
  let input = event.target;
  if (isNaN(input.value) || input.value <= 0) {
    input.value = 1;
  }
  if (input.value > 5) {
    input.value = 5;
  }
  stock = event.target.parentElement.parentElement
    .getElementsByClassName("stock_box")[0]
    .innerText.replace("剩餘 : ", "");
  event.target.setAttribute("max", stock);
  updateCartTotal();
}

function deleteBook(datanumber) {
  let myDataObject = { deleteBookId: datanumber };
  let deleteButtonIcon = document.getElementById(datanumber);
  fetch("/api/addCart", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(myDataObject),
  })
    .then(function (response) {
      return response.json();
    })
    .then((result) => {
      if (result.ok === true) {
        let cart_items = document.getElementsByClassName("cart-items")[0];
        let outBox = deleteButtonIcon.parentElement.parentElement;
        outBox.remove();
        updateCartTotal();
      }
    });
}

TPDirect.setupSDK(
  123992,
  "app_XpdqJEzCUtW3DqRCgzOrLSNfYRFz3ae3Zu6pxTdyp1qWYKOqWbuvN1lU4VFz",
  "sandbox"
);
TPDirect.card.setup({
  // Display ccv field
  fields: {
    number: {
      // css selector
      element: "#card-number",
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      // DOM object
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: "#card-ccv",
      placeholder: "ccv",
    },
  },
  styles: {
    // Style all elements
    input: {
      color: "gray",
      backgroundcolor: "#BCC3D1",
    },
    // Styling ccv field
    "input.ccv": {
      "font-size": "16px",
    },
    // Styling expiration-date field
    "input.expiration-date": {
      "font-size": "16px",
    },
    // Styling card-number field
    "input.card-number": {
      "font-size": "16px",
    },
    // style focus state
    ":focus": {
      color: "black",
    },
    // style valid state
    ".valid": {
      color: "green",
    },
    // style invalid state
    ".invalid": {
      color: "red",
    },
    // Media queries
    // Note that these apply to the iframe, not the root window.
    "@media screen and (max-width: 400px)": {
      input: {
        color: "orange",
      },
    },
  },
});
let submitButton = document.getElementById("confirmBtn");
TPDirect.card.onUpdate(function (update) {
  // update.canGetPrime === true
  // --> you can call TPDirect.card.getPrime()
  if (update.canGetPrime) {
    // Enable submit Button to get prime.
    let submitButton = document.getElementById("confirmBtn");
    submitButton.removeAttribute("disabled");
  } else {
    // Disable submit Button to get prime.
    let submitButton = document.getElementById("confirmBtn");
    submitButton.setAttribute("disabled", true);
  }
  // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
  if (update.cardType === "visa") {
    // Handle card type visa.
  }
  // number 欄位是錯誤的
  if (update.status.number === 2) {
    setNumberFormGroupToError(".card-number-group");
  } else if (update.status.number === 0) {
    setNumberFormGroupToSuccess(".card-number-group");
  } else {
    setNumberFormGroupToNormal(".card-number-group");
  }

  if (update.status.expiry === 2) {
    setNumberFormGroupToError(".expiration-date-group");
  } else if (update.status.expiry === 0) {
    setNumberFormGroupToSuccess(".expiration-date-group");
  } else {
    setNumberFormGroupToNormal(".expiration-date-group");
  }

  if (update.status.cvc === 2) {
    setNumberFormGroupToError(".cvc-group");
  } else if (update.status.cvc === 0) {
    setNumberFormGroupToSuccess(".cvc-group");
  } else {
    setNumberFormGroupToNormal(".cvc-group");
  }
});

submitButton.addEventListener("click", function () {
  onSubmit();
});

function onSubmit(event) {
  // event.preventDefault();
  // 取得 TapPay Fields 的 status
  let bookNameList = [];
  let countList = [];
  let cart_items = document.getElementsByClassName("cart-items")[0];
  let cartItemBoxs = cart_items.getElementsByClassName("cartItemBox");
  for (let i = 0; i < cartItemBoxs.length; i++) {
    let cartItemBox = cartItemBoxs[i];
    let bookName = cartItemBox
      .getElementsByClassName("name_box")[0]
      .innerText.replace("書名 : ", "");
    let quantity = cartItemBox.getElementsByClassName("cart_quantity")[0].value;
    bookNameList.push(bookName);
    countList.push(quantity);
  }
  let phoneValue = document.getElementById("cellphone").value;
  let addressValue = document.getElementById("address").value;
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();
  // 確認是否可以 getPrime
  if (
    tappayStatus.canGetPrime === false ||
    phoneValue === "" ||
    addressValue === ""
  ) {
    document.getElementById("checkinfoBox").innerHTML = "";
    let checkinfoBox = document.getElementById("checkinfoBox");
    let checkinfo = document.createElement("div");
    checkinfo.id = "checkinfo";
    let checkinfo_text = document.createTextNode("請確實填寫聯絡資訊與卡號");
    checkinfo.appendChild(checkinfo_text);
    checkinfoBox.appendChild(checkinfo);
    return;
  } else {
    // Get prime
    TPDirect.card.getPrime((result) => {
      if (result.status !== 0) {
        return;
      }
      let data = {
        prime: result.card.prime,
        username: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: phoneValue,
        address: addressValue,
        bookName: bookNameList,
        count: countList,
      };
      fetch("/api/orders", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((res) => {
          if (res.data !== "") {
            if (res.data.payment.status === 0) {
              cleanCart();
              let orderNumber = res.data.number;
              location.assign("/thankyou?number=" + orderNumber);
            } else {
              document.getElementById("checkinfoBox").innerHTML = "";
              let checkinfoBox = document.getElementById("checkinfoBox");
              let checkinfo = document.createElement("div");
              checkinfo.id = "checkinfo";
              let checkinfo_text = document.createTextNode("付款失敗");
              checkinfo.appendChild(checkinfo_text);
              checkinfoBox.appendChild(checkinfo);
            }
          } else {
            document.getElementById("checkinfoBox").innerHTML = "";
            let checkinfoBox = document.getElementById("checkinfoBox");
            let checkinfo = document.createElement("div");
            checkinfo.id = "checkinfo";
            let checkinfo_text = document.createTextNode("付款失敗");
            checkinfo.appendChild(checkinfo_text);
            checkinfoBox.appendChild(checkinfo);
          }
        });

      // send prime to your server, to pay with Pay by Prime API .
    });
  }
}
function setNumberFormGroupToError(selector) {
  $(selector).addClass("has-error");
  $(selector).removeClass("has-success");
}

function setNumberFormGroupToSuccess(selector) {
  $(selector).removeClass("has-error");
  $(selector).addClass("has-success");
}

function setNumberFormGroupToNormal(selector) {
  $(selector).removeClass("has-error");
  $(selector).removeClass("has-success");
}
