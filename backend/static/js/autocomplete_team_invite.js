document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("username-input");
    const resultsBox = document.getElementById("autocomplete-results");

    input.addEventListener("input", function () {
        const query = input.value;
        if (query.length < 2) {
            resultsBox.innerHTML = "";
            return;
        }

        fetch(`/accounts/autocomplete/user/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                resultsBox.innerHTML = "";
                data.forEach(user => {
                    const div = document.createElement("div");
                    div.classList.add("autocomplete-item");
                    div.innerHTML = `
                        <img src="/static/img/avatars/${user.avatar}" width="32" class="me-2 rounded-circle">
                        <strong>${user.username}</strong>
                    `;
                    div.style.cursor = "pointer";
                    div.addEventListener("click", () => {
                        input.value = user.username;
                        resultsBox.innerHTML = "";
                    });
                    resultsBox.appendChild(div);
                });
            });
    });
});