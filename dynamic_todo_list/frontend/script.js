let tasks=[]

function loadTasks(){

fetch("http://localhost:3000/tasks")
.then(res=>res.json())
.then(data=>{
tasks=data
displayTasks(tasks)
})

}

function addTask(){

let title=document.getElementById("taskTitle").value
let priority=document.getElementById("priority").value

if(title=="" || title.length>50){
alert("Task title invalid")
return
}

fetch("http://localhost:3000/tasks",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({title,priority})
})
.then(()=>loadTasks())

}

function displayTasks(list){
    let ul=document.getElementById("taskList")
    ul.innerHTML=""

    list.forEach(task=>{
        let li=document.createElement("li")

        if(task.isDone){
            li.classList.add("completed")
        }

        li.innerHTML=`
        <span class="${task.priority.toLowerCase()} task-text">
            ${task.title} (${task.priority})
        </span>

        <div>
            <button onclick="toggleTask(${task.id})">✔</button>
            <button onclick="editTask(${task.id}, '${task.title}', '${task.priority}')">✏️</button>
            <button onclick="deleteTask(${task.id})">❌</button>
        </div>
        `

        ul.appendChild(li)
    })

    updateCounter()
}
function editTask(id, currentTitle, currentPriority){

    let newTitle = prompt("Edit Task Title:", currentTitle)
    if(!newTitle || newTitle.trim()=="" || newTitle.length>50) return

    let newPriority = prompt("Edit Priority (Low / Medium / High):", currentPriority)
    if(!["Low","Medium","High"].includes(newPriority)) return

    fetch(`http://localhost:3000/tasks/${id}`,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({title: newTitle, priority: newPriority})
    })
    .then(()=>loadTasks())
}

function toggleTask(id){

fetch(`http://localhost:3000/tasks/${id}/status`,{
method:"PATCH"
})
.then(()=>loadTasks())

}

function deleteTask(id){

fetch(`http://localhost:3000/tasks/${id}`,{
method:"DELETE"
})
.then(()=>loadTasks())

}

function filterTasks(type){

if(type=="all")
displayTasks(tasks)

if(type=="active")
displayTasks(tasks.filter(t=>t.isDone==0))

if(type=="completed")
displayTasks(tasks.filter(t=>t.isDone==1))

}

function updateCounter(){

let total=tasks.length
let completed=tasks.filter(t=>t.isDone==1).length

document.getElementById("counter").innerText=
`Completed ${completed} / ${total}`

}

/* BONUS FEATURE 1 */
function searchTask(){

let keyword=document.getElementById("searchBox").value.toLowerCase()

let filtered=tasks.filter(task =>
task.title.toLowerCase().includes(keyword)
)

displayTasks(filtered)

}

/* BONUS FEATURE 2 */
function sortPriority(){

let order={
High:1,
Medium:2,
Low:3
}

let sorted=[...tasks].sort((a,b)=>{
return order[a.priority]-order[b.priority]
})

displayTasks(sorted)

}

loadTasks()