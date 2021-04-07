// // window.onload = function(){

// //     const add_step_btn = document.getElementById("add-step-btn");

// //      refButton.onclick = function() {
// //          alert('I am clicked!');
// //      }
// //  };

// let recipe_steps = document.getElementsByClassName("recipe-steps")[0];
// let step = document.getElementsByClassName("steps-control");
// const add_step_btn = document.getElementById("add-step-btn");

// add_step_btn.onclick = function(){
//     let newStep = document.createElement('div');
//     newStep.classList.add("form-group")
//     newStep.innerHTML = `{{ form.ingredient.label }}
//     {{ form.ingredient(class='form-control', placeholder="ex. 10") }}
//   `
//     while (newStep.firstChild) {
//         recipe_steps.appendChild(newStep.firstChild);
//     }
//     newStep = document.createElement('div');
//     newStep.classList.add("form-group")
//     newStep.innerHTML =`
//     {{ form.instruction.label }}
//     {{ form.instruction(class='form-control', placeholder="ex. beat eggs") }}
//   `;

//     while (newStep.firstChild) {
//         recipe_steps.appendChild(newStep.firstChild);
//     }
// }
// console.log(add_step_btn)