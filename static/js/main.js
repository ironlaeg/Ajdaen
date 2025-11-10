// Основной JavaScript файл для интерактивности и анимаций

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех функций
    initAnimations();
    initImagePreview();
    initFilterButtons();
    initSmoothScroll();
    initSearchEnhancements();
    initCardHoverEffects();
});

// Анимации при прокрутке
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Наблюдаем за карточками новостей
    document.querySelectorAll('.news-card').forEach(card => {
        observer.observe(card);
    });

    // Наблюдаем за заголовками
    document.querySelectorAll('h1, h2, h3').forEach(heading => {
        observer.observe(heading);
    });
}

// Превью изображений
function initImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(e.target.result, input);
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function showImagePreview(src, input) {
    // Удаляем существующий превью
    const existingPreview = input.parentNode.querySelector('.image-preview');
    if (existingPreview) {
        existingPreview.remove();
    }

    // Создаем новый превью
    const preview = document.createElement('div');
    preview.className = 'image-preview mt-3';
    preview.innerHTML = `
        <div class="preview-container" style="position: relative; max-width: 300px;">
            <img src="${src}" alt="Превью" class="img-fluid rounded shadow-custom" style="max-height: 200px; object-fit: cover;">
            <button type="button" class="btn btn-sm btn-danger remove-preview" style="position: absolute; top: 5px; right: 5px;">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    input.parentNode.appendChild(preview);

    // Обработчик удаления превью
    preview.querySelector('.remove-preview').addEventListener('click', function() {
        preview.remove();
        input.value = '';
    });
}

// Фильтры по категориям и тегам
function initFilterButtons() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Убираем активный класс со всех кнопок
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Добавляем активный класс к текущей кнопке
            this.classList.add('active');
            
            // Анимация нажатия
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

// Плавная прокрутка
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Улучшения поиска
function initSearchEnhancements() {
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('form[method="get"]');
    
    if (searchInput && searchForm) {
        // Добавляем иконку поиска
        if (!searchInput.parentNode.querySelector('.search-icon')) {
            const searchIcon = document.createElement('i');
            searchIcon.className = 'fas fa-search search-icon';
            searchIcon.style.position = 'absolute';
            searchIcon.style.right = '15px';
            searchIcon.style.top = '50%';
            searchIcon.style.transform = 'translateY(-50%)';
            searchIcon.style.color = 'var(--ossetia-gray-medium)';
            
            searchInput.parentNode.style.position = 'relative';
            searchInput.parentNode.appendChild(searchIcon);
        }

        // Анимация при фокусе
        searchInput.addEventListener('focus', function() {
            this.parentNode.style.transform = 'scale(1.02)';
        });

        searchInput.addEventListener('blur', function() {
            this.parentNode.style.transform = 'scale(1)';
        });

        // Поиск при вводе (debounced)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Здесь можно добавить AJAX поиск
                console.log('Поиск:', this.value);
            }, 300);
        });
    }
}

// Эффекты при наведении на карточки
function initCardHoverEffects() {
    const cards = document.querySelectorAll('.news-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Функция для создания уведомлений
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Анимация появления
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

// Функция для загрузки изображений с drag & drop
function initDragAndDrop() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        const container = input.closest('.form-group') || input.parentNode;
        
        container.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });
        
        container.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
        });
        
        container.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
}

// Инициализация drag & drop при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initDragAndDrop();
});

// Функция для анимации счетчиков
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 секунды
        const increment = target / (duration / 16); // 60 FPS
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            counter.textContent = Math.floor(current);
            
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    });
}

// Функция для ленивой загрузки изображений
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Инициализация ленивой загрузки
document.addEventListener('DOMContentLoaded', function() {
    initLazyLoading();
});

// Функция для создания эффекта печатания
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Функция для создания параллакс эффекта
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const rate = scrolled * -0.5;
            element.style.transform = `translateY(${rate}px)`;
        });
    });
}

// Инициализация параллакса
document.addEventListener('DOMContentLoaded', function() {
    initParallax();
});

// Экспорт функций для использования в других скриптах
window.AidaenJS = {
    showNotification,
    animateCounters,
    typeWriter,
    initAnimations,
    initImagePreview
};
