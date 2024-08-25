$(document).ready(function () {
    fetchPosts();

    function fetchPosts() {
        $.ajax({
            url: '/view_feed/',
            type: 'GET',
            success: function (data) {
                var postsContainer = $('#posts-container');
                postsContainer.empty(); // Clear the container first

                $.each(data.posts, function (index, post) {
                    var postHtml = `
                        <div class="post" id="post-${post.post_id}">
                            <div class="post__avatar">
                                <img src="${post.avatar_url}" alt="User Avatar" />
                            </div>

                            <div class="post__body">
                                <div class="post__header">
                                    <div class="post__headerText">
                                        <h3>
                                            ${post.username}
                                            <span class="post__headerSpecial">
                                                <span class="material-icons post__badge">verified</span>
                                                @${post.handle}
                                            </span>
                                            <span class="post__headerSpecial">
                                                /&nbsp;${post.created_at}
                                            </span>
                                        </h3>
                                    </div>
                                    <div class="post__headerDescription">
                                        <p>${post.post_content}</p>
                                    </div>
                                </div>

                                <div class="post__footer">
                                    <button class="like-button" data-post-id="${post.post_id}">
                                        <span class="material-icons icon ${post.user_liked ? 'like' : ''}">
                                            ${post.user_liked ? 'favorite' : 'favorite_border'}
                                        </span>
                                        <span class="count">${post.like_count}</span>
                                    </button>
                                    <button class="comments-button" data-post-id="${post.post_id}">
                                        <span class="material-icons icon">comment</span>
                                        <span class="count">${post.comment_count}</span>
                                    </button>
                                    <form method="post" class="comment__input add-comment-form" data-post-id="${post.post_id}">
                                        <span class="material-icons widgets__searchIcon">comment</span>
                                        <input type="text" class="comment-text" placeholder="Comment" required/>
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                                        <button type="submit">Add Comment</button>
                                    </form>
                                </div>

                                <div class="comments-container" id="comments-list-${post.post_id}">
                                    <!-- Comments will be loaded here -->
                                </div>
                            </div>
                        </div>
                    `;
                    postsContainer.append(postHtml);
                    loadComments(post.post_id);  // Load comments for the post
                });

                // Event delegation to handle like button click
                postsContainer.on('click', '.like-button', function () {
                    const button = $(this);
                    const postId = button.data('post-id');

                    $.ajax({
                        url: '/add_like/' + postId + '/',
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token in the request
                        },
                        success: function (response) {
                            const icon = button.find('span.icon');
                            if (response.liked) {
                                icon.addClass('like');
                                icon.text('favorite'); // Change icon to filled heart
                            } else {
                                icon.removeClass('like');
                                icon.text('favorite_border'); // Change icon to outlined heart
                            }
                            button.find('.count').text(response.like_count);
                        },
                        error: function (error) {
                            console.error("Error liking post:", error);
                        }
                    });
                });

                // Event delegation to handle comment form submission
                postsContainer.on('submit', '.add-comment-form', function (e) {
                    e.preventDefault();

                    const form = $(this);
                    const postId = form.data('post-id');
                    const commentText = form.find('.comment-text').val();
                    const csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();

                    $.ajax({
                        url: `/post/${postId}/add_comment/`,
                        type: 'POST',
                        data: {
                            'text': commentText,
                            'csrfmiddlewaretoken': csrfToken
                        },
                        success: function (response) {
                            if (response.success) {
                                form.find('.comment-text').val('');  // Clear the input field
                                loadComments(postId);  // Reload comments
                            } else {
                                alert('Error: ' + response.error);
                            }
                        },
                        error: function (error) {
                            console.error('Error adding comment:', error);
                        }
                    });
                });
            },
            error: function (error) {
                console.error("Error fetching posts:", error);
            }
        });
    }

    function loadComments(postId) {
        $.ajax({
            url: `/post/${postId}/comments/`,
            type: 'GET',
            success: function (response) {
                const commentsList = $(`#comments-list-${postId}`);
                commentsList.empty();  // Clear existing comments
                $.each(response.comments, function (index, comment) {
                    const commentHtml = `
                        <div class="comment">
                            <strong>${comment.username}</strong> <span>${comment.created_at}</span>
                            <p>${comment.text}</p>
                        </div>
                    `;
                    commentsList.append(commentHtml);
                });
            },
            error: function (error) {
                console.error('Error loading comments:', error);
            }
        });
    }

    // Function to get the CSRF token from cookies
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
});
