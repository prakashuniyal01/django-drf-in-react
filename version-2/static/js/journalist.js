
    // Fetch access token from localStorage or session
    const accessToken = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

    if (!accessToken) {
        window.location.href = '/login/';  // Redirect to login if no access token
    }

    // Verify the access token
    fetch('http://127.0.0.1:8000/users/api/session-check/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Session expired or invalid access token.');
            window.location.href = '/login/';  // Redirect to login if the token is invalid
        }
    })
    .catch(error => {
        console.error('Error verifying token:', error);
        window.location.href = '/login/';  // Redirect to login in case of any errors
    });

    // Function to fetch and display articles (All, Published, Pending)
    function fetchArticles(endpoint) {
        fetch(endpoint, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            }
        })
        .then(response => response.json())
        .then(data => {
            const articlesContent = document.getElementById('articles-content');
            let content = '<h4>Articles List</h4>';

            if (data.results && data.results.length > 0) {
                content += '<ul>';
                data.results.forEach(article => {
                    content += `<li><strong>${article.title}</strong> - ${article.status}</li>`;
                });
                content += '</ul>';
            } else {
                content += '<p>No articles found.</p>';
            }

            articlesContent.innerHTML = content;
        })
        .catch(error => {
            console.error('Error fetching articles:', error);
            document.getElementById('articles-content').innerHTML = '<p>Error fetching articles.</p>';
        });
    }

    // Event listeners for sidebar navigation
    document.getElementById('all-articles-link').addEventListener('click', function() {
        fetchArticles('http://127.0.0.1:8000/articles/articles/');
    });

    document.getElementById('published-articles-link').addEventListener('click', function() {
        fetchArticles('http://127.0.0.1:8000/articles/articles/published/');
    });

    document.getElementById('pending-articles-link').addEventListener('click', function() {
        fetchArticles('http://127.0.0.1:8000/articles/articles/pending/');
    });

    document.getElementById('create-articles-link').addEventListener('click', function() {
        document.getElementById('articles-content').innerHTML = `
            <h4>Create a New Article</h4>
            <form id="createArticleForm">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" id="title" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="content">Content</label>
                    <textarea id="content" class="form-control" required></textarea>
                </div>
                <button type="submit" class="btn btn-success mt-3">Create Article</button>
            </form>
        `;
        
        document.getElementById('createArticleForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;

            fetch('http://127.0.0.1:8000/articles/articles/create/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    content: content,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Article created successfully!');
                } else {
                    alert('Error creating article');
                }
            })
            .catch(error => {
                console.error('Error creating article:', error);
            });
        });
    });

    // Default load of All Articles
    fetchArticles('http://127.0.0.1:8000/articles/articles/');
