const imgDiv = document.querySelector(".profile-pic-div");
const img = document.querySelector("#photo");
const file = document.querySelector("#file");
const uploadBtn = document.querySelector("#uploadBtn");

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
        location.assign("/");
      }
    });
}
memberstatus();

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
//if user hover on img div

imgDiv.addEventListener("mouseenter", function () {
  uploadBtn.style.display = "block";
});

//if we hover out from img div

imgDiv.addEventListener("mouseleave", function () {
  uploadBtn.style.display = "none";
});

function render(imageURL) {
  // render 留言
  let photo = document.getElementById("photo");
  photo.setAttribute("src", imageURL);
}

window.addEventListener("load", () => {
  // 網頁載入時 render 畫面
  fetch("/api/accountPic", {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      let accountName = document.getElementById("accountName");
      let nameText = document.createTextNode("Name  :  " + data.name);
      let accountEmail = document.getElementById("accountEmail");
      let emailText = document.createTextNode("Email  :  " + data.email);
      accountName.appendChild(nameText);
      accountEmail.appendChild(emailText);
      render(data.data[0].image);
    });
});

let imgData = new FormData();
let image = "";
//lets work for image showing functionality when we choose an image to upload

//when we choose a foto to upload

file.addEventListener("change", (e) => {
  image = e.target.files[0];
  console.log(image);
  imgData.append("file", image);
  fetch("/api/accountPic", {
    method: "POST",
    body: imgData,
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
    });

  if (image) {
    const reader = new FileReader(); //FileReader is a predefined function of JS
    console.log(reader);

    reader.addEventListener("load", function () {
      img.setAttribute("src", reader.result);
    });

    reader.readAsDataURL(image);
  }
});

function history() {
  fetch("/api/hidtory", {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      datahistory = data.data;
      console.log(datahistory);
      let historyTitleBox = document.getElementById("historyTitleBox");
      if (datahistory !== []) {
        for (let i = 0; i < datahistory.length; i++) {
          let historyBox = document.createElement("div");
          historyBox.id = "historyBox";
          let ordernumberBox = document.createElement("div");
          ordernumberBox.id = "ordernumberBox";
          let ordernumber = document.createTextNode(datahistory[i].number);
          let orderNameBox = document.createElement("div");
          orderNameBox.id = "orderNameBox";
          let orderName = document.createTextNode(datahistory[i].name);
          let orderAuthorBox = document.createElement("div");
          orderAuthorBox.id = "orderAuthorBox";
          let orderAuthor = document.createTextNode(datahistory[i].author);
          let orderPriceBox = document.createElement("div");
          orderPriceBox.id = "orderPriceBox";
          let orderPrice = document.createTextNode(
            datahistory[i].price + " 元"
          );
          orderPriceBox.appendChild(orderPrice);
          ordernumberBox.appendChild(ordernumber);
          orderNameBox.appendChild(orderName);
          orderAuthorBox.appendChild(orderAuthor);
          historyBox.appendChild(ordernumberBox);
          historyBox.appendChild(orderNameBox);
          historyBox.appendChild(orderAuthorBox);
          historyBox.appendChild(orderPriceBox);
          historyTitleBox.appendChild(historyBox);
        }
      } else {
        return;
      }
    });
}
history();
