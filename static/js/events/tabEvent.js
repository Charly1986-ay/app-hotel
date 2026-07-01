document.addEventListener('DOMContentLoaded', () => {    
    const tabMenus = document.querySelectorAll('.tabs-menu');

    tabMenus.forEach(menu => {
        const tabs = menu.querySelectorAll('.tab-btn');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Encontrar el contenedor de paneles asociado a este menú
                const wrapper = menu.closest('.tabs-wrapper');
                const targetSelector = tab.dataset.target;
                const targetPanel = wrapper.querySelector(targetSelector);

                // 1. Quitar 'is-active' de los botones de ESTE menú
                tabs.forEach(t => t.classList.remove('is-active'));
                
                // 2. Quitar 'is-active' de los paneles de ESTE contenedor
                wrapper.querySelectorAll('.tab-panel').forEach(panel => {
                    panel.classList.remove('is-active');
                });

                // 3. Activar la pestaña y el panel correspondiente
                tab.classList.add('is-active');
                if (targetPanel) {
                    targetPanel.classList.add('is-active');
                }
            });
        });
    });
});