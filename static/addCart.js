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

function cartInfo() {
  fetch("/api/addCart")
    .then(function (response) {
      return response.json();
    })
    .then((result) => {
      console.log(result);
      if (result.error !== true) {
        if (result.data !== null) {
          let data = result.data;
          console.log(data);
          let name_list = [];
          let author_list = [];
          let id_list = [];
          let price_list = [];
          let image_list = [];
          let category_list = [];

          for (let i = 0; i < data.length; i++) {
            name_list.push(data[i].name);
            author_list.push(data[i].author);
            id_list.push(data[i].id);
            price_list.push(data[i].price);
            category_list.push(data[i].category);
            image_list.push(data[i].image);
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
            let cart_price = document.createElement("div");
            cart_price.className = "price_box";
            let priceTextNode = document.createTextNode(price_list[i] + " 元 ");
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
            cartItemText.appendChild(name_box);
            cartItemText.appendChild(author_box);
            cart_price.appendChild(priceTextNode);
            cartItemImage.appendChild(image);
            cartItemBox.appendChild(cartItemImage);
            cartItemBox.appendChild(cartItemText);
            cartItemBox.appendChild(cart_price);
            cartItemBox.appendChild(delete_button);
            cart_items.appendChild(cartItemBox);
          }
        }
      } else {
        location.assign("/");
      }
    });
}

cartInfo();

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
        deleteButtonIcon.parentElement.parentElement.innerHTML = "";
      }
    });
}
