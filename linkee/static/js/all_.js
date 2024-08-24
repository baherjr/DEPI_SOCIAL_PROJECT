// $(document).ready(function() {
//     $.ajax({
//         url: '/friend_requests/',
//         type: 'GET',
//         success: function(data) {
//             // Access the data from the response object
//             var pendingRequests = data.pending_requests;

//             // Update the DOM with the friend requests
//             $('#friend-requests-container').empty();
//             $.each(pendingRequests, function(index, request) {
//                 var friendRequestHtml = `
//                     <div class="frnd-rqst">
//                         <img src="${request.profile.profileimg}" alt="userprfl">
//                         <div class="frnd-data">
//                             <h3><a href="#">${request.first_name}&nbsp;${request.last_name}</a></h3>
//                             <h5>@${request.username}</h5>
//                         </div>
//                         <button class="btn acpt">Accept</button>
//                         <button class="btn rjct">Reject</button>
//                     </div>
//                 `;
//                 $('#friend-requests-container').append(friendRequestHtml);
//             });
//         }
//     });
// });


$(document).ready(function() {
    $.ajax({
        url: '/friend_requests/',
        type: 'GET',
        success: function(data) {
            // Access the data from the response object
            var pendingRequests = data.pending_requests;
            console.log(pendingRequests);
            // Check if there are any pending requests
            if (pendingRequests && pendingRequests.length > 0) {
                // Update the DOM with the friend requests
                $('#friend-requests-container').empty();
                $.each(pendingRequests, function(index, request) {
                    var acceptUrl = '/handle_friend_request/' + request.friend_id + '/accept/';
                    var rejectUrl = '/handle_friend_request/' + request.friend_id + '/reject/';
                    var friendRequestHtml = `
                        <div class="frnd-rqst">
                            <img src="${request.profile_picture}" alt="userprfl">
                            <div class="frnd-data">
                                <h3><a href="#">${request.first_name}&nbsp;${request.last_name}</a></h3>
                                <h5>@${request.username}</h5>
                            </div>
                            <a class="btn acpt" href="${acceptUrl}">Accept</a>
                            <a class="btn rjct" href="${rejectUrl}">Reject</a>
                        </div>
                    `;
                    $('#friend-requests-container').append(friendRequestHtml);
                });
            } else {
                // No pending requests found
                const text_display = "<h4 class='none'>No Friend Requests</h4>";
                $('#friend-requests-container').append(text_display);
            }
        }
    });
});