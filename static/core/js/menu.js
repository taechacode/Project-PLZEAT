// 변수 선언
const menu = document.querySelector(".jsMenu");
const hiddenMenu = document.querySelector(".jsHiddenMenu");
const jsHtml = document.querySelector("html");

// 함수 정의

const clickOutside = (event) => {
  if (
    !hiddenMenu.classList.contains("jsClickedHiddenMenu") ||
    event.target.classList.contains("power-off") ||
    event.target.classList.contains("cog") ||
    event.target.classList.contains("menu_middle_menus")
  ) {
    return;
  }
  event.preventDefault();
  if (
    !(
      event.target.classList.contains("hidden_menu") ||
      event.target.classList.contains("menu_top") ||
      event.target.classList.contains("menu_middle") ||
      event.target.classList.contains("menu_bottom") ||
      event.target.classList.contains("cog") ||
      event.target.classList.contains("jsMenu") ||
      event.target.classList.contains("menu_middle_menus") ||
      event.target.classList.contains("power-off")
    )
  ) {
    hiddenMenu.classList.remove("jsClickedHiddenMenu");
  }
};

const clickMenu = (event) => {
  event.preventDefault();
  if (hiddenMenu.classList.contains("jsClickedHiddenMenu")) {
    hiddenMenu.classList.remove("jsClickedHiddenMenu");
  } else {
    hiddenMenu.classList.add("jsClickedHiddenMenu");
  }
};

const main = () => {
  menu.addEventListener("click", clickMenu);
  jsHtml.addEventListener("click", clickOutside);
};

// 함수 호출
main();
