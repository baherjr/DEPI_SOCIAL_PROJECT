function togglePopup(){
    console.log("ok");
    document.getElementById("popup1").classList.toggle("active");
}


$(document).ready(function() {
    $.ajax({
        url: '/friends/',
        type: 'GET',
        success: function(data) {
            var friends = data.friends;
            if (friends.length > 0) {
                // There are friends
                $('#friends-list').html('');
                $.each(friends, function(index, friend) {
                    var friendRequestHtml = `
                        <div class="friend">
                            <img class="frnd-img" src="${friend.profile_picture}" alt="my friend photo">
                            <div class="friend-data">
                                <h5>${friend.first_name}&nbsp;${friend.last_name}</h5>
                                <p>@${friend.username}</p>
                            </div>
                        </div>
                    `;
                    $('#friends-list').append(friendRequestHtml);
                });
            } else {
                // No friends
                $('#friends-list').append("<h4 class='none'>You have no friends yet.</h4>");
            }
        }
    });
});

$(document).ready(function() {
    $.ajax({
        url: '/get_friend_count/',
        type: 'GET',
        success: function(data) {
            var friendCount = data.friend_count;
            $('#profileId #count').text(friendCount);
        }
    });
});


$(document).ready(function() {
    $.ajax({
        url: '/view_my_posts/', // Update this with your actual API endpoint
        type: 'GET',
        success: function(data) {
            var posts = data.posts;

            if (posts.length > 0) {
                // Clear the container before appending new content
                $('#posts-container').html('');

                $.each(posts, function(index, post) {
                    var postHtml = `
                        <div class="post">
                            <div class="post__avatar">
                                <img
                                    src="${post.avatar_url}"  // Replace with dynamic URL
                                    alt=""
                                />
                            </div>

                            <div class="post__body">
                                <div class="post__header">
                                    <div class="post__headerText">
                                        <h3>
                                            ${post.username}
                                            <span class="post__headerSpecial">
                                                <span class="material-icons post__badge">verified</span>@${post.handle}
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
                                    <button class="like-button" id="like-button-${post.id}" data-post-id="${post.id}">
                                        <span class="material-icons icon ${post.user_liked ? 'like' : ''}">favorite_border</span> 
                                        <span class="count" id="like-count-${post.id}">${post.like_count}</span>
                                    </button>
                                    <button class="comments-button" id="comments-button-${post.id}" data-post-id="${post.id}">
                                        <span class="material-icons icon">comment</span> 
                                        <span class="count" id="comment-count-${post.id}">${post.comment_count}</span>
                                    </button>
                                    <form method="post" class="comment__input" data-post-id="${post.id}">
                                        <span class="material-icons widgets__searchIcon">comment</span>
                                        <span>&nbsp; &nbsp;</span>
                                        <input type="text" placeholder="Comment" />
                                    </form>
                                </div>
                            </div>
                        </div>
                    `;
                    $('#posts-container').append(postHtml);
                });

                // Attach event listeners to like buttons in the profile view
                $('.like-button').on('click', function() {
                    const button = $(this);
                    const postId = button.data('post-id');

                    $.ajax({
                        url: '/add_like/' + postId + '/',
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        success: function(response) {
                            const icon = button.find('span.icon');
                            if (response.liked) {
                                icon.addClass('like');
                            } else {
                                icon.removeClass('like');
                            }
                            button.find('.count').text(response.like_count);

                            // Update the corresponding like button in the feed page
                            const feedLikeButton = $('#like-button-' + postId);
                            if (feedLikeButton.length > 0) {
                                feedLikeButton.find('.count').text(response.like_count);
                                if (response.liked) {
                                    feedLikeButton.find('.icon').addClass('like');
                                } else {
                                    feedLikeButton.find('.icon').removeClass('like');
                                }
                            }
                        },
                        error: function(error) {
                            console.error("Error liking post:", error);
                        }
                    });
                });
            } else {
                // No posts found
                $('#posts-container').text('You have no posts yet.');
            }
        },
        error: function(error) {
            console.error("Error fetching posts:", error);
        }
    });
});


$(document).ready(function () {
    fetchPosts();

    function fetchPosts() {
        $.ajax({
            url: '/view_my_posts/',
            type: 'GET',
            success: function (data) {
                var postsContainer = $('#posts-container');
                postsContainer.empty(); // Clear the container first

                $.each(data.posts, function (index, post) {
                    var postHtml = `
                        <div class="post">
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
                                    <form method="post" class="comment__input">
                                        <span class="material-icons widgets__searchIcon">comment</span>
                                        <input type="text" placeholder="Comment" />
                                    </form>
                                </div>
                            </div>
                        </div>
                    `;
                    postsContainer.append(postHtml);
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
                postsContainer.on('submit', '.comment__input', function (e) {
                    e.preventDefault();
                    // Handle the comment submission via AJAX here
                });
            },
            error: function (error) {
                console.error("Error fetching posts:", error);
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
