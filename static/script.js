// Локальный кэш списка фильмов, полученных с бэкенда
let movies = [];
// Текущий id фильма, который редактируется (null, если создаём новый)
let currentEditId = null;

// При полной загрузке DOM подтягиваем фильмы с сервера
document.addEventListener('DOMContentLoaded', () => {
    loadMovies();
});

// Загрузка всех фильмов из API
async function loadMovies() {
    try {
        const response = await fetch('/api/movies');
        movies = await response.json();
        // Отрисовываем список фильмов в сетке
        renderMovies(movies);
    } catch (error) {
        console.error('Ошибка загрузки фильмов:', error);
        alert('Не удалось загрузить фильмы');
    }
}

// Отображение фильмов в виде карточек
function renderMovies(moviesToRender) {
    const grid = document.getElementById('moviesGrid');
    const emptyState = document.getElementById('emptyState');

    // Если фильмов нет — показываем "пустое" состояние
    if (moviesToRender.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    grid.style.display = 'grid';
    emptyState.style.display = 'none';

    // Формируем HTML карточек на основе массива фильмов
    grid.innerHTML = moviesToRender
        .map(
            movie => `
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
    `,
        )
        .join('');
}

// Фильтрация фильмов по строке поиска
function filterMovies() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = movies.filter(
        movie =>
            movie.title.toLowerCase().includes(searchTerm) ||
            (movie.director && movie.director.toLowerCase().includes(searchTerm)) ||
            (movie.genre && movie.genre.toLowerCase().includes(searchTerm)),
    );
    renderMovies(filtered);
}

// Открытие модального окна для создания/редактирования фильма
function openModal(movieId = null) {
    const modal = document.getElementById('movieModal');
    const form = document.getElementById('movieForm');
    const modalTitle = document.getElementById('modalTitle');

    currentEditId = movieId;

    if (movieId) {
        // Режим редактирования существующего фильма
        modalTitle.textContent = 'Редактировать фильм';
        const movie = movies.find(m => m.id === movieId);
        if (movie) {
            // Заполняем форму значениями из выбранного фильма
            document.getElementById('movieId').value = movie.id;
            document.getElementById('title').value = movie.title || '';
            document.getElementById('director').value = movie.director || '';
            document.getElementById('year').value = movie.year || '';
            document.getElementById('genre').value = movie.genre || '';
            document.getElementById('rating').value = movie.rating || '';
            document.getElementById('description').value = movie.description || '';
        }
    } else {
        // Режим создания нового фильма
        modalTitle.textContent = 'Добавить фильм';
        form.reset();
        document.getElementById('movieId').value = '';
    }

    modal.style.display = 'block';
}

// Закрытие модального окна и сброс текущего контекста редактирования
function closeModal() {
    document.getElementById('movieModal').style.display = 'none';
    currentEditId = null;
}

// Сохранение фильма (создание или обновление)
async function saveMovie(event) {
    event.preventDefault();

    // Собираем данные из формы и приводим типы
    const movieData = {
        title: document.getElementById('title').value,
        director: document.getElementById('director').value || null,
        year: document.getElementById('year').value ? parseInt(document.getElementById('year').value) : null,
        genre: document.getElementById('genre').value || null,
        rating: document.getElementById('rating').value ? parseFloat(document.getElementById('rating').value) : null,
        description: document.getElementById('description').value || null,
    };

    try {
        let response;
        if (currentEditId) {
            // Обновление существующего фильма (PUT /api/movies/{id})
            response = await fetch(`/api/movies/${currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(movieData),
            });
        } else {
            // Создание нового фильма (POST /api/movies)
            response = await fetch('/api/movies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(movieData),
            });
        }

        if (response.ok) {
            // После успешного сохранения закрываем модалку и перезагружаем список
            closeModal();
            loadMovies();
        } else {
            // Если сервер вернул ошибку — пытаемся показать detail из ответа
            const error = await response.json();
            alert(`Ошибка: ${error.detail || 'Не удалось сохранить фильм'}`);
        }
    } catch (error) {
        console.error('Ошибка сохранения фильма:', error);
        alert('Не удалось сохранить фильм');
    }
}

// Обёртка для открытия модалки в режиме редактирования
function editMovie(movieId) {
    openModal(movieId);
}

// Удаление фильма по id
async function deleteMovie(movieId) {
    if (!confirm('Вы уверены, что хотите удалить этот фильм?')) {
        return;
    }

    try {
        const response = await fetch(`/api/movies/${movieId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            // После удаления перезагружаем список фильмов
            loadMovies();
        } else {
            alert('Не удалось удалить фильм');
        }
    } catch (error) {
        console.error('Ошибка удаления фильма:', error);
        alert('Не удалось удалить фильм');
    }
}

// Закрытие модального окна при клике по фону вокруг него
window.onclick = function (event) {
    const modal = document.getElementById('movieModal');
    if (event.target === modal) {
        closeModal();
    }
};

// Экранирование HTML для безопасности (защита от XSS, если данные придут "грязными")
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    };
    return text ? text.replace(/[&<>"']/g, m => map[m]) : '';
}

