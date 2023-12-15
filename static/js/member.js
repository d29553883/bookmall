function siginin() {
  let data = {
    email: document.getElementById("inputemail").value,
    password: document.getElementById("inputpassword").value,
  };
  fetch("/api/user", {
    method: "PATCH",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((res) => {
      if (res.ok === true) {
        location.reload();
      } else if (res.message === "帳號或密碼錯誤") {
        let loginerror = document.getElementsByClassName("loginerror")[0];
        loginerror.innerHTML = "";
        let failtext = document.createTextNode("帳號或密碼錯誤");
        loginerror.appendChild(failtext);
      }
    });
}

function siginin_google(){
  window.location.href = "https://book-mall.store/login";

}

function singup() {
  let data = {
    name: document.getElementById("singupname").value,
    email: document.getElementById("singupemail").value,
    password: document.getElementById("singuppassword").value,
  };
  fetch("/api/user", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((res) => {
      if (res.ok === true) {
        let successout = document.getElementsByClassName("successlogin")[0];
        successout.innerHTML = "";
        let successtext = document.createTextNode("註冊成功");
        successout.appendChild(successtext);
      } else if (res.message === "此email已存在") {
        let successout = document.getElementsByClassName("successlogin")[0];
        let failtext = document.createTextNode("此email已存在");
        successout.appendChild(failtext);
      }
    });
}

function logout() {
  fetch("/api/user", {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((res) => {
      if (res.ok === true) {
        location.reload();
      }
    });
}
document
  .getElementsByClassName("login_google")[0]
  .addEventListener("click", function () {
    siginin_google();
  });
document.getElementById("logout_button").addEventListener("click", function () {
  logout();
});

document
  .getElementsByClassName("siginup_text")[0]
  .addEventListener("click", function () {
    singup();
  });

document
  .getElementsByClassName("login_text")[0]
  .addEventListener("click", function () {
    siginin();
  });

document
  .getElementsByClassName("maintitle")[0]
  .addEventListener("click", function () {
    // updateCount();
    location.assign("/");
  });

var mo = function (e) {
  e.preventDefault();
};
function stop() {
  document.body.style.overflow = "hidden";
  document.addEventListener("touchmove", mo, { passive: false }); //禁止頁面滑動
}
function move() {
  document.body.style.overflow = ""; //出現滾動條
  document.removeEventListener("touchmove", mo, { passive: false });
}

document.getElementById("login_button").addEventListener("click", function () {
  document.querySelector(".popup").style.display = "flex";
  stop();
});

document.querySelector(".close").addEventListener("click", function () {
  document.querySelector(".popup").style.display = "none";
  move();
});

document.querySelector(".close2").addEventListener("click", function () {
  document.querySelector(".popup_signup").style.display = "none";
  move();
});

document.getElementById("switch_sinup").addEventListener("click", function () {
  document.querySelector(".popup").style.display = "none";
  document.querySelector(".popup_signup").style.display = "flex";
});

document.getElementById("switch_login").addEventListener("click", function () {
  document.querySelector(".popup_signup").style.display = "none";
  document.querySelector(".popup").style.display = "flex";
});

function cartCount() {
  fetch("/api/cartCount")
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      if (result.message === "未登入系統，拒絕存取") {
        return;
      } else {
        let cart = document.getElementById("reservation_button");
        let countBox = document.createElement("div");
        countBox.id = "countBox";
        let countText = document.createTextNode(result.count[0]);
        countBox.appendChild(countText);
        cart.appendChild(countBox);
      }
    });
}
cartCount();
