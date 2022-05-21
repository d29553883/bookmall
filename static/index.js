function createdata() {
  let src = "/api/books";
  fetch(src)
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      console.log(result);
      let dotbox = document.getElementsByClassName("dotbox")[0];
      dotbox.parentElement.removeChild(dotbox);
      let science_author_list = [];
      let science_description_list = [];
      let science_image_list = [];
      let science_price_list = [];
      let science_name_list = [];
      let science_id_list = [];
      let data1 = result.data1;
      for (let i in data1) {
        science_author_list.push(data1[i].author);
        science_description_list.push(data1[i].description);
        science_image_list.push(data1[i].image);
        science_price_list.push(data1[i].price);
        science_name_list.push(data1[i].name);
        science_id_list.push(data1[i].bookid);
      }
      for (let i = 0; i < data1.length; i++) {
        console.log(science_id_list);
        let swiper_wrapper =
          document.getElementsByClassName("swiper-wrapper")[0];
        let swiper_slide = document.createElement("div");
        swiper_slide.className = "swiper-slide card";
        let card_content = document.createElement("div");
        card_content.className = "card-content";
        let image_box = document.createElement("div");
        image_box.className = "image";
        let image = document.createElement("img");
        image.src = science_image_list[i];
        let pictag = document.createElement("a");
        pictag.href = "/book/" + science_id_list[i];
        let name_author = document.createElement("div");
        name_author.className = "name-author";
        let name = document.createElement("div");
        name.className = "name";
        name.textContent = science_name_list[i];
        let author = document.createElement("div");
        author.className = "author";
        author.textContent = science_author_list[i];
        name_author.appendChild(name);
        name_author.appendChild(author);
        image_box.appendChild(image);
        card_content.appendChild(image_box);
        card_content.appendChild(name_author);
        pictag.appendChild(card_content);
        swiper_slide.appendChild(pictag);
        swiper_wrapper.appendChild(swiper_slide);
      }
    });
}

createdata();

function createdata2() {
  let src = "/api/books";
  fetch(src)
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      let dotbox = document.getElementsByClassName("dotbox2")[0];
      dotbox.parentElement.removeChild(dotbox);
      let language_author_list = [];
      let language_description_list = [];
      let language_image_list = [];
      let language_price_list = [];
      let language_name_list = [];
      let language_id_list = [];
      let data2 = result.data2;
      for (let i in data2) {
        language_author_list.push(data2[i].author);
        language_description_list.push(data2[i].description);
        language_image_list.push(data2[i].image);
        language_price_list.push(data2[i].price);
        language_name_list.push(data2[i].name);
        language_id_list.push(data2[i].bookid);
      }
      for (let i = 0; i < data2.length; i++) {
        let swiper_wrapper = document.getElementById("language_swiper-wrapper");
        let swiper_slide = document.createElement("div");
        swiper_slide.className = "swiper-slide card";
        let card_content = document.createElement("div");
        card_content.className = "card-content";
        let image_box = document.createElement("div");
        image_box.className = "image";
        let image = document.createElement("img");
        image.src = language_image_list[i];
        let pictag = document.createElement("a");
        pictag.href = "/book/" + language_id_list[i];
        let name_author = document.createElement("div");
        name_author.className = "name-author";
        let name = document.createElement("div");
        name.className = "name";
        name.textContent = language_name_list[i];
        let author = document.createElement("div");
        author.className = "author";
        author.textContent = language_author_list[i];
        name_author.appendChild(name);
        name_author.appendChild(author);
        image_box.appendChild(image);
        card_content.appendChild(image_box);
        card_content.appendChild(name_author);
        pictag.appendChild(card_content);
        swiper_slide.appendChild(pictag);
        swiper_wrapper.appendChild(swiper_slide);
      }
    });
}
createdata2();

function createdata3() {
  let src = "/api/books";
  fetch(src)
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      let dotbox = document.getElementsByClassName("dotbox3")[0];
      dotbox.parentElement.removeChild(dotbox);
      let art_author_list = [];
      let art_description_list = [];
      let art_image_list = [];
      let art_price_list = [];
      let art_name_list = [];
      let art_id_list = [];
      let data3 = result.data3;
      for (let i in data3) {
        art_author_list.push(data3[i].author);
        art_description_list.push(data3[i].description);
        art_image_list.push(data3[i].image);
        art_price_list.push(data3[i].price);
        art_name_list.push(data3[i].name);
        art_id_list.push(data3[i].bookid);
      }
      for (let i = 0; i < data3.length; i++) {
        let swiper_wrapper = document.getElementById("art_swiper-wrapper");
        let swiper_slide = document.createElement("div");
        swiper_slide.className = "swiper-slide card";
        let card_content = document.createElement("div");
        card_content.className = "card-content";
        let image_box = document.createElement("div");
        image_box.className = "image";
        let image = document.createElement("img");
        image.src = art_image_list[i];
        let pictag = document.createElement("a");
        pictag.href = "/book/" + art_id_list[i];
        let name_author = document.createElement("div");
        name_author.className = "name-author";
        let name = document.createElement("div");
        name.className = "name";
        name.textContent = art_name_list[i];
        let author = document.createElement("div");
        author.className = "author";
        author.textContent = art_author_list[i];
        name_author.appendChild(name);
        name_author.appendChild(author);
        image_box.appendChild(image);
        card_content.appendChild(image_box);
        card_content.appendChild(name_author);
        pictag.appendChild(card_content);
        swiper_slide.appendChild(pictag);
        swiper_wrapper.appendChild(swiper_slide);
      }
    });
}
createdata3();

function createdata4() {
  let src = "/api/books";
  fetch(src)
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      let dotbox = document.getElementsByClassName("dotbox4")[0];
      dotbox.parentElement.removeChild(dotbox);
      let humanities_author_list = [];
      let humanities_description_list = [];
      let humanities_image_list = [];
      let humanities_price_list = [];
      let humanities_name_list = [];
      let humanities_id_list = [];
      let data4 = result.data4;
      for (let i in data4) {
        humanities_author_list.push(data4[i].author);
        humanities_description_list.push(data4[i].description);
        humanities_image_list.push(data4[i].image);
        humanities_price_list.push(data4[i].price);
        humanities_name_list.push(data4[i].name);
        humanities_id_list.push(data4[i].bookid);
      }
      for (let i = 0; i < data4.length; i++) {
        let swiper_wrapper = document.getElementById(
          "humanities_swiper-wrapper"
        );
        let swiper_slide = document.createElement("div");
        swiper_slide.className = "swiper-slide card";
        let card_content = document.createElement("div");
        card_content.className = "card-content";
        let image_box = document.createElement("div");
        image_box.className = "image";
        let image = document.createElement("img");
        image.src = humanities_image_list[i];
        let pictag = document.createElement("a");
        pictag.href = "/book/" + humanities_id_list[i];
        let name_author = document.createElement("div");
        name_author.className = "name-author";
        let name = document.createElement("div");
        name.className = "name";
        name.textContent = humanities_name_list[i];
        let author = document.createElement("div");
        author.className = "author";
        author.textContent = humanities_author_list[i];
        name_author.appendChild(name);
        name_author.appendChild(author);
        image_box.appendChild(image);
        card_content.appendChild(image_box);
        card_content.appendChild(name_author);
        pictag.appendChild(card_content);
        swiper_slide.appendChild(pictag);
        swiper_wrapper.appendChild(swiper_slide);
      }
    });
}
createdata4();

const searchkeyword = document.getElementById("searchkeyword");
const searchBtn = document.getElementById("searchBtn");

function searchdata() {
  let ky = searchkeyword.value;
  let image_list = [];
  let name_list = [];
  let author_list = [];
  let description_list = [];
  let id_list = [];
  let src = "api/books?keyword=" + ky;
  fetch(src)
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      let data = result.data;
      if (searchkeyword.value !== "" && result.data.length !== 0) {
        console.log(result.data.length);
        console.log(searchkeyword.value);
        let datas = result.data;
        // let nextpage = result.nextPage;
        Page = 0;
        let oldpic = document.getElementById("section_warp");
        while (oldpic.firstChild) {
          oldpic.removeChild(oldpic.firstChild);
        }
        for (let i in data) {
          author_list.push(data[i].author);
          description_list.push(data[i].description);
          image_list.push(data[i].image);
          name_list.push(data[i].name);
          id_list.push(data[i].bookid);
        }
        for (let i = 0; i < data.length; i++) {
          document.getElementsByClassName("error")[0].innerHTML = "";
          let oldpic = document.getElementById("section_warp");
          let section_box = document.createElement("div");
          section_box.className = "section_box";
          let card_box = document.createElement("div");
          card_box.className = "card";
          let card_content = document.createElement("div");
          card_content.className = "card-content";
          let image_box = document.createElement("div");
          image_box.className = "image";
          let image = document.createElement("img");
          image.src = image_list[i];
          let pictag = document.createElement("a");
          pictag.href = "/book/" + id_list[i];
          let name_author = document.createElement("div");
          name_author.className = "name-author";
          let name = document.createElement("div");
          name.className = "name";
          name.textContent = name_list[i];
          let author = document.createElement("div");
          author.className = "author";
          author.textContent = author_list[i];
          name_author.appendChild(name);
          name_author.appendChild(author);
          image_box.appendChild(image);
          card_content.appendChild(image_box);
          card_content.appendChild(name_author);
          pictag.appendChild(card_content);
          card_box.appendChild(pictag);
          section_box.appendChild(card_box);
          oldpic.appendChild(section_box);
        }
      } else {
        let oldpic = document.getElementById("section_warp");
        while (oldpic.firstChild) {
          oldpic.removeChild(oldpic.firstChild);
        }
        let error = document.getElementsByClassName("error")[0];
        let noresult = document.createTextNode("查無此資料");
        error.appendChild(noresult);
      }
    });
}

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

searchBtn.addEventListener("click", function () {
  document.getElementById("section_warp").style.flexDirection = "row";
  searchdata();
});

// window.addEventListener("fetch", () => {
//   const loader = document.querySelector(".loader");
//   loader.classList.add("loader--hidden");

//   loader.addEventListener("result", () => {
//     document.body.removeChild(loader);
//   });
// });

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
