const per = document.querySelectorAll(".recipe_per");

// 메인함수
let count = 0;
const changePer = () => {
  for (const x of per) {
    x.innerHTML = "{{percent}}";
    count += 1;
  }
};

changePer();
