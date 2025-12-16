let movies = [];
let currentEditId = null;

// Загрузка фильмов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadMovies();
});

// Загрузка всех фильмов
async function loadMovies() {
    try {
        const response = await fetch('/api/movies');
        movies = await response.json();
        renderMovies(movies);
    } catch (error) {
        console.error('Ошибка загрузки фильмов:', error);
        alert('Не удалось загрузить фильмы');
    }
}

// Отображение фильмов
function renderMovies(moviesToRender) {
    const grid = document.getElementById('moviesGrid');
    const emptyState = document.getElementById('emptyState');
    
    if (moviesToRender.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    grid.innerHTML = moviesToRender.map(movie => `
        <div class="movie-card">
            <h3>${escapeHtml(movie.title)}</h3>
            ${movie.director ? `<div class="movie-info"><strong>Режиссёр:</strong> ${escapeHtml(movie.director)}</div>` : ''}
            ${movie.year ? `<div class="movie-info"><strong>Год:</strong> ${movie.year}</div>` : ''}
            ${movie.genre ? `<div class="movie-info"><strong>Жанр:</strong> ${escapeHtml(movie.genre)}</div>` : ''}
            ${movie.rating ? `<div class="rating">⭐ ${movie.rating.toFixed(1)}</div>` : ''}
            ${movie.description ? `<div class="movie-description">${escapeHtml(movie.description)}</div>` : ''}
            <div class="movie-actions">
                <button class="btn btn-edit" onclick="editMovie(${movie.id})">Редактировать</button>
                <button class="btn btn-danger" onclick="deleteMovie(${movie.id})">Удалить</button>
            </div>
        </div>
    `).join('');
}

// Фильтрация фильмов
function filterMovies() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = movies.filter(movie => 
        movie.title.toLowerCase().includes(searchTerm) ||
        (movie.director && movie.director.toLowerCase().includes(searchTerm)) ||
        (movie.genre && movie.genre.toLowerCase().includes(searchTerm))
    );
    renderMovies(filtered);
}

// Открытие модального окна
function openModal(movieId = null) {
    const modal = document.getElementById('movieModal');
    const form = document.getElementById('movieForm');
    const modalTitle = document.getElementById('modalTitle');
    
    currentEditId = movieId;
    
    if (movieId) {
        modalTitle.textContent = 'Редактировать фильм';
        const movie = movies.find(m => m.id === movieId);
        if (movie) {
            document.getElementById('movieId').value = movie.id;
            document.getElementById('title').value = movie.title || '';
            document.getElementById('director').value = movie.director || '';
            document.getElementById('year').value = movie.year || '';
            document.getElementById('genre').value = movie.genre || '';
            document.getElementById('rating').value = movie.rating || '';
            document.getElementById('description').value = movie.description || '';
        }
    } else {
        modalTitle.textContent = 'Добавить фильм';
        form.reset();
        document.getElementById('movieId').value = '';
    }
    
    modal.style.display = 'block';
}

// Закрытие модального окна
function closeModal() {
    document.getElementById('movieModal').style.display = 'none';
    currentEditId = null;
}

// Сохранение фильма
async function saveMovie(event) {
    event.preventDefault();
    
    const movieData = {
        title: document.getElementById('title').value,
        director: document.getElementById('director').value || null,
        year: document.getElementById('year').value ? parseInt(document.getElementById('year').value) : null,
        genre: document.getElementById('genre').value || null,
        rating: document.getElementById('rating').value ? parseFloat(document.getElementById('rating').value) : null,
        description: document.getElementById('description').value || null
    };
    
    try {
        let response;
        if (currentEditId) {
            // Обновление существующего фильма
            response = await fetch(`/api/movies/${currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(movieData)
            });
        } else {
            // Создание нового фильма
            response = await fetch('/api/movies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(movieData)
            });
        }
        
        if (response.ok) {
            closeModal();
            loadMovies();
        } else {
            const error = await response.json();
            alert(`Ошибка: ${error.detail || 'Не удалось сохранить фильм'}`);
        }
    } catch (error) {
        console.error('Ошибка сохранения фильма:', error);
        alert('Не удалось сохранить фильм');
    }
}

// Редактирование фильма
function editMovie(movieId) {
    openModal(movieId);
}

// Удаление фильма
async function deleteMovie(movieId) {
    if (!confirm('Вы уверены, что хотите удалить этот фильм?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/movies/${movieId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadMovies();
        } else {
            alert('Не удалось удалить фильм');
        }
    } catch (error) {
        console.error('Ошибка удаления фильма:', error);
        alert('Не удалось удалить фильм');
    }
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('movieModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Экранирование HTML для безопасности
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text ? text.replace(/[&<>"']/g, m => map[m]) : '';
}

