document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.todo-card');
  const now = new Date();

  cards.forEach(card => {
    const created = new Date(card.dataset.created);
    const due = new Date(card.dataset.due);
    if (isNaN(created) || isNaN(due)) return;

    const totalTime = due - created;
    const timePassed = now - created;

    let ratio = Math.max(0, Math.min(1, timePassed / totalTime));

    let r, g, b;

    if (ratio < 0.5) {
      r = 224 + ratio * 2 * (255 - 224); // 224→255
      g = 255;
      b = 224 - ratio * 2 * (224 - 204); // 224→204
    } else {
      r = 255;
      g = 247 - (ratio - 0.5) * 2 * (247 - 224); // 247→224
      b = 204 - (ratio - 0.5) * 2 * (204 - 224); // 204→224 (rosso chiaro)
    }

    card.style.backgroundColor = `rgb(${r.toFixed(0)}, ${g.toFixed(0)}, ${b.toFixed(0)})`;
  });
});
