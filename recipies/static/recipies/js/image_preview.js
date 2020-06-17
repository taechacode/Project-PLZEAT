let reader = new FileReader();

reader.onload = (readerEvent) => {
  document
    .querySelector("#image_section")
    .setAttribute("src", readerEvent.target.result);
};
const avatar = document.querySelector("#id_photo");
document
  .querySelector("#id_photo")
  .addEventListener("change", (changeEvent) => {
    console.log("바뀜");
    let imgFile = changeEvent.target.files[0];
    reader.readAsDataURL(imgFile);
  });
