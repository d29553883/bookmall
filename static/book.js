function singlepage() {
  id = String(window.location.href);
  id = id.substr(-3, 3);
  let src = "/api/book/" + id;
  fetch(src)
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      let titlebox = document.getElementsByClassName("titlebox")[0];
      let title = document.createTextNode(result.name);
      let title2box = document.getElementsByClassName("title2box")[0];
      let title2 = document.createTextNode(result.author);
      let tab = document.getElementById("tab");
      let tabImg = document.createElement("img");
      let category = document.getElementsByClassName("category")[0];
      let category_text = document.createTextNode("分類 : " + result.category);
      tabImg.className = "tabImg";
      tabImg.src = result.image;
      let pricebox = document.getElementsByClassName("b2")[0];
      let price = document.createTextNode("$ " + result.price);
      let contentbox = document.getElementsByClassName("contentbox")[0];
      let content = document.createTextNode(result.description);
      category.appendChild(category_text);
      pricebox.appendChild(price);
      titlebox.appendChild(title);
      title2box.appendChild(title2);
      contentbox.appendChild(content);
      tab.appendChild(tabImg);
    });
}
singlepage();

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

function createinfo() {
  currentid = String(window.location.href);
  currentid = currentid.substr(-3, 3);
  currentid = Number(currentid);
  console.log(currentid);
  let data = {
    id: currentid,
  };
  fetch("/api/addCart", {
    method: "post",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((res) => {
      console.log(res);
      location.assign("/addCart");
    });
}

document.getElementById("addCartBtn").addEventListener("click", function () {
  fetch("/api/user")
    .then(function (response) {
      return response.json();
    })
    .then((result) => {
      let data = result.data;
      console.log(data);
      if (data !== null) {
        createinfo();
      } else {
        document.querySelector(".popup").style.display = "flex";
      }
    });
});

document
  .getElementById("reservation_button")
  .addEventListener("click", function () {
    fetch("/api/user")
      .then(function (response) {
        return response.json();
      })
      .then((result) => {
        let data = result.data;
        console.log(data);
        if (data !== null) {
          location.assign("/addCart");
        } else {
          document.querySelector(".popup").style.display = "flex";
        }
      });
  });
