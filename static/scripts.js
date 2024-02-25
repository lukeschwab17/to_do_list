
function showEdit(id) {
        let children = document.getElementById(`${id}`).querySelectorAll(".task-editor");
        for(let i = 0; i < children.length; ++i) {
            children[i].style.visibility = 'visible';
        }
        document.getElementById(`edit-${id}`).remove();
        document.getElementById(`delete-${id}`).remove();
        let checkboxesLabels = document.querySelectorAll(".checkbox-label");
        let checkboxes = document.querySelectorAll(".checkbox");
        for(let i = 0; i < checkboxesLabels.length; ++i) {
            checkboxesLabels[i].remove();
            checkboxes[i].remove();
        }
    }