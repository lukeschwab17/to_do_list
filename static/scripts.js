
function showEdit(id) {
        let children = document.getElementById(`${id}`).querySelectorAll(".task-editor");
        for(let i = 0; i < children.length; ++i) {
            children[i].style.visibility = 'visible';
        }
       document.getElementById(`edit-${id}`).remove()
    }