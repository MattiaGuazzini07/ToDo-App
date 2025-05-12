/** @type {typeof import("shepherd.js").default} */
document.addEventListener("DOMContentLoaded", () => {
    if (typeof Shepherd === 'undefined') {
        console.error("❌ Shepherd.js non è caricato!");
        return;
    }

    console.log("✅ Shepherd caricato");

    // 🔐 Recupera il CSRF token dal cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    window.startTour = function () {
        const tour = new Shepherd.Tour({
            useModalOverlay: true,
            defaultStepOptions: {
                scrollTo: true,
                cancelIcon: { enabled: true },
                classes: 'shadow-md bg-purple-dark',
                modalOverlayOpeningPadding: 5,
                modalOverlayOpeningRadius: 8,
            }
        });

        tour.addStep({
            title: 'Benvenuto su ToDo! 🎉',
            text: 'Questa è la tua area personale. Ti mostro come iniziare!',
            buttons: [
                { text: 'Avanti', action: tour.next }
            ]
        });

        if (document.querySelector('.form-box')) {
            tour.addStep({
                title: 'Crea una nuova attività 📝',
                text: 'Qui puoi inserire titolo, scadenza e priorità.',
                attachTo: { element: '.form-box', on: 'right' },
                buttons: [
                    { text: 'Avanti', action: tour.next },
                    { text: 'Chiudi', action: tour.cancel }
                ]
            });
        }

        if (document.querySelector('.order-form')) {
            tour.addStep({
                title: 'Filtri e ricerca 🔍',
                text: 'Filtra le attività per priorità, stato o testo.',
                attachTo: { element: '.order-form', on: 'bottom' },
                buttons: [
                    { text: 'Avanti', action: tour.next },
                    { text: 'Chiudi', action: tour.cancel }
                ]
            });
        }

        tour.addStep({
            title: 'Calendario 📅',
            text: 'Visualizza le attività in formato calendario.',
            attachTo: { element: 'a[href$="calendar"]', on: 'left' },
            buttons: [
                {
                    text: 'Fine',
                    action: () => {
                        tour.complete();
                        if (window.location.pathname === "/") {
                            fetch("/tour/seen/", {
                                method: "POST",
                                headers: {
                                    "X-CSRFToken": getCookie("csrftoken"),
                                    "Content-Type": "application/json"
                                },
                                body: "{}"
                            });
                        }
                    }
                }
            ]
        });

        tour.start();
    };
});
