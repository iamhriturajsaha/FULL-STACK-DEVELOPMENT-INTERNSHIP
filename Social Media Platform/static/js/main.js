document.addEventListener('DOMContentLoaded', () => {
    
    // Follow Logic
    const followBtns = document.querySelectorAll('.follow-btn');
    followBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const username = btn.dataset.username;
            btn.style.pointerEvents = 'none';
            btn.style.opacity = '0.5';
            
            try {
                const response = await fetch(`/profile/${username}/follow/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    btn.textContent = data.is_following ? 'FOLLOWING ✓' : 'FOLLOW +';
                }
            } catch (err) {
                console.error(err);
            } finally {
                btn.style.pointerEvents = 'auto';
                btn.style.opacity = '1';
            }
        });
    });

    // Search Overlay
    const searchBtn = document.getElementById('searchBtn');
    const searchOverlay = document.getElementById('searchOverlay');
    const closeSearch = document.getElementById('closeSearch');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            searchOverlay.classList.add('active');
            searchInput.focus();
        });
        
        closeSearch.addEventListener('click', () => {
            searchOverlay.classList.remove('active');
        });
        
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value;
            if (query.length < 2) {
                searchResults.innerHTML = '';
                return;
            }
            
            searchTimeout = setTimeout(async () => {
                const res = await fetch(`/search/?q=${encodeURIComponent(query)}`);
                const data = await res.json();
                searchResults.innerHTML = '';
                data.users.forEach(user => {
                    const el = document.createElement('a');
                    el.href = `/profile/${user.username}/`;
                    el.className = 'search-result-item';
                    const img = user.avatar ? `<img src="${user.avatar}" class="search-avatar">` : `<div class="search-avatar"></div>`;
                    el.innerHTML = `${img}<span>@${user.username}</span>`;
                    searchResults.appendChild(el);
                });
            }, 300);
        });
    }

    // Like Logic
    const likeBtns = document.querySelectorAll('.like-btn');
    likeBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const postId = btn.dataset.postId;
            try {
                const response = await fetch(`/post/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    btn.textContent = `♡ ${data.like_count}`;
                    if (data.is_liked) {
                        btn.style.color = '#fff';
                        btn.innerHTML = `♥ ${data.like_count}`;
                    } else {
                        btn.style.color = 'inherit';
                        btn.innerHTML = `♡ ${data.like_count}`;
                    }
                }
            } catch (err) {
                console.error(err);
            }
        });
    });

    // Comment Logic
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const postId = commentForm.dataset.postId;
            const contentInput = document.getElementById('commentContent');
            const content = contentInput.value;
            
            try {
                const response = await fetch(`/post/${postId}/comment/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    contentInput.value = '';
                    
                    const commentsList = document.getElementById('commentsList');
                    const newComment = document.createElement('div');
                    newComment.className = 'comment';
                    newComment.innerHTML = `
                        <span style="font-weight: 600; text-transform: uppercase; font-size: 0.75rem;">@${data.author}</span>
                        <p style="font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: var(--text-secondary);">${data.content}</p>
                    `;
                    commentsList.appendChild(newComment);
                }
            } catch (err) {
                console.error(err);
            }
        });
    }

    // Intersection Observer for scroll reveal animations
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
