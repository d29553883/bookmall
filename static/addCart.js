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
            let cartItemNames = document.createElement("div");
            cartItemNames.className = "cart-item-title";
            let nameTextNode = document.createTextNode(name_list[i]);
            let cart_price = document.createElement("div");
            cart_price.className = "cart-price";
            let priceTextNode = document.createTextNode(price_list[i]);
            cartItemNames.appendChild(nameTextNode);
            cart_price.appendChild(priceTextNode);
            cartItemImage.appendChild(image);
            cartItemBox.appendChild(cartItemImage);
            cartItemBox.appendChild(cartItemNames);
            cartItemBox.appendChild(cart_price);
            cart_items.appendChild(cartItemBox);
          }
        }
      } else {
        location.assign("/");
      }
    });
}

cartInfo();
