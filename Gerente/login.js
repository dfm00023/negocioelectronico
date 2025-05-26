document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        // Estamos en la página de login
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            if (username === "gerente" && password === "1234") {
                localStorage.setItem("usuario", username);
                window.location.href = "index.html"; // Redirige a la página principal
            } else {
                alert("Usuario o contraseña incorrectos");
            }
        });
    } else {
        // Estamos en otra página
        const usuario = localStorage.getItem("usuario");
        if (usuario) {
            document.getElementById("user-info").innerHTML = `Bienvenido, <strong>${usuario}</strong>`;
        } else {
            window.location.href = "login.html"; // Si no hay usuario, redirige al login
        }

        // Cerrar sesión
        document.getElementById("logout").addEventListener("click", () => {
            localStorage.removeItem("usuario");
            window.location.href = "login.html";
        });
    }
});
