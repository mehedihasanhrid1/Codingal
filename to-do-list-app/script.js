document.addEventListener("DOMContentLoaded", ()=>{
    const itemInput = document.getElementById("item");
    const addButton = document.getElementById("addBtn");
    const output = document.getElementById("output");

    
    function addItem(){
        const itemText = itemInput.value.trim();
        if (itemText === "") {
            alert("Please enter an item!");
            return;
        }

        const listItem = document.createElement("div");
        listItem.className = "task-item";

        const taskText = document.createElement("span");
        taskText.textContent = itemText;

        const completeBtn = document.createElement("button");
        completeBtn.textContent = "Mark Complete";
        completeBtn.addEventListener("click", () => {
            taskText.style.textDecoration = "line-through";
            completeBtn.disabled = true;
        });

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.addEventListener("click", () => {
            output.removeChild(listItem);
        });

        listItem.appendChild(taskText);
        listItem.appendChild(completeBtn);
        listItem.appendChild(deleteBtn);

        output.appendChild(listItem);
        itemInput.value = "";
    }

    addButton.addEventListener("click", addItem);
});