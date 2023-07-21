document.addEventListener("DOMContentLoaded", function () {
    const commentTextarea = document.getElementById("id_content");
    const taggedUsersInput = document.getElementById("id_tagged_users");
    const tagRegex = /@(\w+)/g;
    let taggedUsers = [];

    commentTextarea.addEventListener("input", updateTaggedUsers);

    function updateTaggedUsers() {
        const content = commentTextarea.innerText;
        const matches = content.match(tagRegex);

        if (matches) {
            taggedUsers = matches.map((match) => match.substr(1));
            taggedUsersInput.value = taggedUsers.join(",");
        } else {
            taggedUsers = [];
            taggedUsersInput.value = "";
        }
    }
});
