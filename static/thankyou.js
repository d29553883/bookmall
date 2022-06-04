function thankyouPage() {
  x = String(window.location.href);
  let orderNumber = x.slice(-14);
  fetch("/api/orders/" + orderNumber, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((res) => {
      let ordernumber = res.data.number;
      let numberBox = document.getElementById("numberBox");
      let textBox = document.createElement("div");
      textBox.className = "ordernumber";
      let number_text = document.createTextNode(ordernumber);
      textBox.appendChild(number_text);
      numberBox.appendChild(textBox);
    });
}

thankyouPage();

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

document.getElementById("refundBtn").addEventListener("click", function () {
  x = String(window.location.href);
  let orderNumber = x.slice(-14);
  let data = {
    orderNumber: orderNumber,
  };
  fetch("/api/refund", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      let booktitlebox = document.getElementById("booktitlebox");
      let refundTextBox = document.createElement("div");
      refundTextBox.id = "refundTextBox";
      console.log(data);
      if (data.data.message === "退款成功") {
        let refundText = document.createTextNode("退款成功!");
        refundTextBox.appendChild(refundText);
        booktitlebox.appendChild(refundTextBox);
      } else if (data.data.message === "退款失敗") {
        let refundText = document.createTextNode("退款失敗!");
        refundTextBox.appendChild(refundText);
        booktitlebox.appendChild(refundTextBox);
      }
    });
});
