function thankyouPage() {
  x = String(window.location.href);
  let orderNumber = x.slice(-14);
  fetch("/api/orders/" + orderNumber, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((res) => {
      console.log(res);
      let ordernumber = res.data.number;
      console.log(ordernumber);
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
