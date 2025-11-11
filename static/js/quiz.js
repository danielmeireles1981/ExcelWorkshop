// static/js/quiz.js
// Comportamento dos flip-cards do quiz geral

document.addEventListener('DOMContentLoaded', () => {
  // Virar os cards ao clicar
  document.querySelectorAll('.quiz-item .flip-card').forEach((card) => {
    card.addEventListener('click', (e) => {
      card.classList.toggle('flipped');
    });
  });

  // Mostrar/ocultar resposta no botão abaixo de cada card
  document.querySelectorAll('.quiz-item').forEach((item) => {
    const btn = item.querySelector('.show-answer-btn');
    const answer = item.querySelector('.answer-content');

    if (!btn || !answer) return;

    btn.addEventListener('click', (e) => {
      e.stopPropagation(); // Evita interferir no flip do card
      const hidden = answer.classList.contains('hidden');
      if (hidden) {
        answer.classList.remove('hidden');
        btn.textContent = 'Ocultar resposta';
        btn.setAttribute('aria-expanded', 'true');
      } else {
        answer.classList.add('hidden');
        btn.textContent = 'Mostrar resposta';
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });
});

