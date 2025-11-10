document.addEventListener('DOMContentLoaded', function() {
    const exerciseModal = document.getElementById('exerciseModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const modalFormula = document.getElementById('modalFormula');
    const openModalButtons = document.querySelectorAll('.open-exercise-modal');
    const closeModalButtons = document.querySelectorAll('.close-modal');

    // Função para abrir o modal
    function openModal() {
        exerciseModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Impede o scroll no body
    }

    // Função para fechar o modal
    function closeModal() {
        exerciseModal.classList.add('hidden');
        document.body.style.overflow = ''; // Restaura o scroll no body
    }

    // Event listeners para abrir o modal
    openModalButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (url) {
                // Busca os detalhes do exercício via AJAX
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        modalTitle.textContent = data.title;
                        modalDescription.innerHTML = data.description; // Alterado para innerHTML
                        modalFormula.textContent = data.reference_formula;
                        openModal();
                    })
                    .catch(error => console.error('Erro ao buscar detalhes do exercício:', error));
            }
        });
    });

    // Event listeners para fechar o modal
    closeModalButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });

    // Fecha o modal ao clicar fora dele
    exerciseModal.addEventListener('click', function(e) {
        if (e.target === exerciseModal) {
            closeModal();
        }
    });
});