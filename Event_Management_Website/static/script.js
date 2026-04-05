function validateForm(){
let email=document.querySelector("input[name='email']").value;
let phone=document.querySelector("input[name='phone']").value;

let pattern=/^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

if(!email.match(pattern)){
alert("Invalid Email");
return false;
}

if(phone.length!=10 || isNaN(phone)){
alert("Invalid Phone");
return false;
}

return true;
}

function searchEvent(){
let input=document.getElementById("search").value.toLowerCase();
let cards=document.querySelectorAll(".card");

cards.forEach(card=>{
if(card.innerText.toLowerCase().includes(input)){
card.style.display="block";
}else{
card.style.display="none";
}
});
}