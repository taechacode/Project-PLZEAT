const need_plus = document.querySelector(".jsNeedPlus");
const copyed = document.querySelector(".jsNeed");
const gijun = document.querySelector(".need_plus");
const submit_btn = document.querySelector(".jsSubmit");
console.log(submit_btn);

const clickedPlusIcon = (event) => {
  event.preventDefault();
  gijun.insertAdjacentHTML(
    "beforebegin",
    `
    <div class="input need_food">
        <input class="please_input" type="text" name="need_food" placeholder="식자재">
    </div>
  `
  );
};

const clickedNeedPlus = () => {
  need_plus.addEventListener("click", clickedPlusIcon);
};

clickedNeedPlus();
