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
      let stockElement = document.getElementsByClassName("stock")[0];
      let stock_text = document.createTextNode("剩餘 : " + result.stock);
      tabImg.className = "tabImg";
      tabImg.src = result.image;
      let pricebox = document.getElementsByClassName("b2")[0];
      let price = document.createTextNode("$ " + result.price);
      let contentbox = document.getElementsByClassName("contentbox")[0];
      let content = document.createTextNode(result.description);
      category.appendChild(category_text);
      stockElement.appendChild(stock_text);
      pricebox.appendChild(price);
      titlebox.appendChild(title);
      title2box.appendChild(title2);
      contentbox.appendChild(content);
      tab.appendChild(tabImg);
      let stock = stockElement.innerText.replace("剩餘 : ", "");
      if (stock === "0") {
        let soldOutBox = document.createElement("div");
        soldOutBox.className = "soldOutBox";
        let soldOut = document.createElement("img");
        soldOut.className = "soldOut";
        soldOut.src = "../static/out-of-stock.png";
        soldOutBox.appendChild(soldOut);
        tab.appendChild(soldOutBox);
        tabImg.style.filter = "grayscale(100%)";
      }
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
        document.getElementById("account_button").style.display = "flex";
      } else {
        document.getElementById("logout_button").style.display = "none";
        document.getElementById("login_button").style.display = "flex";
        document.getElementById("account_button").style.display = "none";
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
      let book_list = [];
      let stockElement = document.getElementsByClassName("stock")[0];
      let stock = stockElement.innerText.replace("剩餘 : ", "");
      if (data !== null) {
        fetch("/api/addCart")
          .then(function (response) {
            return response.json();
          })
          .then((result) => {
            let titlebox = document.getElementsByClassName("titlebox")[0];
            let title = titlebox.innerText;
            let data = result.data;
            if (stock === "0") {
              return "";
            } else {
              if (data !== null) {
                // 偵測購物車裡是否有重複商品
                for (let i = 0; i < data.length; i++) {
                  book_list.push(data[i].name);
                }
                if (book_list.includes(title)) {
                  alert("此商品已經在購物車裡!");
                } else {
                  createinfo();
                }
              } else {
                createinfo();
              }
            }
          });
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
        if (data !== null) {
          location.assign("/addCart");
        } else {
          document.querySelector(".popup").style.display = "flex";
        }
      });
  });

document
  .getElementById("account_button")
  .addEventListener("click", function () {
    fetch("/api/user")
      .then(function (response) {
        return response.json();
      })
      .then((result) => {
        let data = result.data;
        if (data !== null) {
          location.assign("/account");
        } else {
          document.querySelector(".popup").style.display = "flex";
        }
      });
  });

let board = document.querySelector("#board");

function render(message, imageURL, username) {
  // render 留言
  let board = document.getElementById("board");
  let recommentBox = document.createElement("div");
  recommentBox.id = "recommentBox";

  let pic_name = document.createElement("div");
  pic_name.id = "pic_name";

  let name = document.createElement("div");
  name.id = "name";
  let nameText = document.createTextNode(username);
  name.appendChild(nameText);
  let profile_pic_div = document.createElement("div");
  profile_pic_div.className = "profile-pic-div";
  let photo = document.createElement("img");
  photo.src = imageURL;
  profile_pic_div.appendChild(photo);
  pic_name.appendChild(name);
  pic_name.appendChild(profile_pic_div);
  let recommentTextBox = document.createElement("div");
  recommentTextBox.id = "recommentTextBox";
  let recommentText = document.createTextNode(message);
  recommentTextBox.appendChild(recommentText);
  recommentBox.appendChild(pic_name);
  recommentBox.appendChild(recommentTextBox);
  board.appendChild(recommentBox);
}

window.addEventListener("load", () => {
  id = String(window.location.href);
  id = id.substr(-3, 3);
  let src = "/api/book/" + id;
  fetch(src, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      data.data.forEach((data) =>
        render(data.message, data.image, data.username)
      );
    });
});

let messageData = new FormData();

document.getElementById("postBtn").addEventListener("click", function () {
  let message = document.getElementById("recomment").value;
  if (document.querySelector("#account_button").style.display !== "none") {
    if (message !== "") {
      id = String(window.location.href);
      id = id.substr(-3, 3);
      messageData.append("message", message);
      messageData.append("bookid", id);
      // 帶資料給後端
      fetch("/api/recomment", {
        method: "POST",
        body: messageData,
      })
        .then((res) => res.json())
        .then((data) => {
          document.getElementById("recomment").value = "";
          window.location.reload();
        })
        .catch((err) => console.log("出錯了...", err));
    } else {
      alert("請輸入留言");
    }
  } else {
    document.querySelector(".popup").style.display = "flex";
  }
});
