document.addEventListener("DOMContentLoaded", function () {
  const selected = document.getElementById("dropdown-selected");
  const selectedImg = document.getElementById("dropdown-selected-img");
  const options = document.getElementById("dropdown-options");
  const input = document.getElementById("avatar-input");

  if (selected && selectedImg && options && input) {
    selected.addEventListener("click", () => {
      options.style.display = options.style.display === "block" ? "none" : "block";
    });

    document.querySelectorAll(".dropdown-option").forEach(option => {
      option.addEventListener("click", () => {
        const value = option.getAttribute("data-value");
        const imgSrc = option.querySelector("img").getAttribute("src");

        input.value = value;
        selectedImg.setAttribute("src", imgSrc);
        options.style.display = "none";
      });
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".custom-dropdown")) {
        options.style.display = "none";
      }
    });
  }
});
