document.addEventListener("DOMContentLoaded", init, false)

function init() {
  let css_colors = [
    "AliceBlue",
    "AntiqueWhite",
    "Aqua",
    "Aquamarine",
    "Azure",
    "Beige",
    "Bisque",
    "BlanchedAlmond",
    "Blue",
    "BlueViolet",
    "Brown",
    "BurlyWood",
    "CadetBlue",
    "Chartreuse",
    "Chocolate",
    "Coral",
    "CornflowerBlue",
    "Cornsilk",
    "Crimson",
    "Cyan",
    "DarkBlue",
    "DarkCyan",
    "DarkGoldenRod",
    "DarkGray",
    "DarkGrey",
    "DarkGreen",
    "DarkKhaki",
    "DarkMagenta",
    "DarkOliveGreen",
    "DarkOrange",
    "DarkOrchid",
    "DarkRed",
    "DarkSalmon",
    "DarkSeaGreen",
    "DarkSlateBlue",
    "DarkSlateGray",
    "DarkSlateGrey",
    "DarkTurquoise",
    "DarkViolet",
    "DeepPink",
    "DeepSkyBlue",
    "DimGray",
    "DimGrey",
    "DodgerBlue",
    "FireBrick",
    "FloralWhite",
    "ForestGreen",
    "Fuchsia",
    "GhostWhite",
    "Gold",
    "GoldenRod",
    "Gray",
    "Grey",
    "Green",
    "GreenYellow",
    "HoneyDew",
    "HotPink",
    "IndianRed",
    "Indigo",
    "Khaki",
    "LavenderBlush",
    "LawnGreen",
    "LemonChiffon",
    "LightBlue",
    "LightCoral",
    "LightCyan",
    "LightGray",
    "LightGrey",
    "LightGreen",
    "LightPink",
    "LightSalmon",
    "LightSeaGreen",
    "LightSkyBlue",
    "LightSlateGray",
    "LightSlateGrey",
    "LightSteelBlue",
    "LightYellow",
    "Lime",
    "LimeGreen",
    "Linen",
    "Magenta",
    "Maroon",
    "MediumAquaMarine",
    "MediumBlue",
    "MediumOrchid",
    "MediumPurple",
    "MediumSeaGreen",
    "MediumSlateBlue",
    "MediumSpringGreen",
    "MediumTurquoise",
    "MediumVioletRed",
    "MidnightBlue",
    "MintCream",
    "MistyRose",
    "Moccasin",
    "NavajoWhite",
    "Navy",
    "OldLace",
    "Olive",
    "OliveDrab",
    "Orange",
    "OrangeRed",
    "Orchid",
    "PaleGoldenRod",
    "PaleGreen",
    "PaleTurquoise",
    "PaleVioletRed",
    "PapayaWhip",
    "PeachPuff",
    "Peru",
    "Pink",
    "Plum",
    "PowderBlue",
    "Purple",
    "Red",
    "RosyBrown",
    "RoyalBlue",
    "SaddleBrown",
    "Salmon",
    "SandyBrown",
    "SeaGreen",
    "SeaShell",
    "Sienna",
    "Silver",
    "SkyBlue",
    "SlateBlue",
    "SlateGray",
    "Snow",
    "SpringGreen",
    "SteelBlue",
    "Tan",
    "Teal",
    "Thistle",
    "Tomato",
    "Turquoise",
    "Violet",
    "Wheat",
    "Yellow",
    "YellowGreen"
  ]

  let random_color = css_colors[randint(1, css_colors.length)];
  let random_color2 = css_colors[randint(1, css_colors.length)];

  document.querySelector(":root").style.cssText = "--vehicle_theme: " + random_color + "; --random_color: " + random_color2 + ";"

  if (document.querySelector("#editing")) {
    let edit_buttons = document.querySelectorAll("#entries form > img");
    console.log("Found " + edit_buttons.length + " edit buttons")
    for (let button of edit_buttons) {
      button.addEventListener("click", edit_field, false);
  }
  }

  if (document.querySelector('#add_entry')) {
    let field1 = document.getElementById('brand_name');
    let field2 = document.getElementById('model');
    let field3 = document.getElementById('type_name');
    let field4 = document.getElementById('production_year');
    let field5 = document.getElementById('engine_size');
    let field6 = document.getElementById('market_value');

    
    if (field1 !== null && field2 !== null && field3 !== null && field4 !== null && field5 !== null && field6 !== null) {
      field1.addEventListener("input", check_fields, false);
      field2.addEventListener("input", check_fields, false);
      field3.addEventListener("input", check_fields, false);
      field4.addEventListener("input", check_fields, false);
      field5.addEventListener("input", check_fields, false);
      field6.addEventListener("input", check_fields, false);

      function check_fields() { 
        if (field1.value != "" && field2.value != "" && field3.value != "" && field4.value != "" && field5.value != "" && field6.value != "") {
          document.getElementById("add").removeAttribute("disabled");
        }
      }
    }
}
}

// error handling on login/register page

function CheckProblemField() {
  let problem_field1 = document.getElementById("name_error");
  let problem_field2 = document.getElementById("username_error");
  let problem_field3 = document.getElementById("password_error");
  let problem_field4 = document.getElementById("re_password_error");

  let problem_fields = [problem_field1, problem_field2, problem_field3, problem_field4];
  let element_ids = ["name", "username", "password", "re_password"]; // array
  
  for (let i = 0; i < problem_fields.length; i++) {
    if (problem_fields[i]) {
      let id = element_ids[i];
      document.getElementById(id).classList = "error_field"; // apply the class to the element with the ID
    }
  }

  let second_password_field = document.getElementById("re_password");
  if (second_password_field) {
  CheckPasswordEquality();
  }
}

// password equality check on register page
function CheckPasswordEquality() {
  let passwordField1 = document.getElementById('password');
  let passwordField2 = document.getElementById('re_password');

  // Add an event listener to the second password field to check for equality
  passwordField2.addEventListener('input', function() {
    if (passwordField1.value !== passwordField2.value) {
      document.querySelector("#register_button").setAttribute("disabled", "true");
      document.querySelector("#register_button").style.cssText = "background:grey;transition:2s"
      console.log("Passwords are not equal")
    } else {
      document.querySelector("#register_button").removeAttribute("disabled")
      document.querySelector("#register_button").style.cssText = ""

      console.log("Passwords are equal")
    }
  });
}


// Toggle Recently Viewed tab

function toggle_recently_viewed() {
  if (document.querySelector("main > section").id == "hidden_recently_viewed") {
    document.getElementById("hidden_recently_viewed").id = "recently_viewed"
}
  
  else if (document.querySelector("main > section").id == "recently_viewed") {
    document.getElementById("recently_viewed").id = "hidden_recently_viewed"
  }
}

// Show input field for admin code on register

function show_codefield() {
  document.getElementById("admin_code").id = "shown_admin_code"
  document.getElementById("shown_admin_code").disabled = false
}


// Compare vehicles on wishlist page
function compare(event) {
  if (event.target.getAttribute("value") == "off") {
    event.target.style.cssText = "background:#00c3ff;color:white;border:1px solid white;";
    event.target.setAttribute("value", "on")
    event.target.parentNode.parentNode.style.cssText = "background:linear-gradient(to right, gold, orange);order:1;";
  }
  else if (event.target.getAttribute("value") == "on") {
    event.target.style.cssText = "";
    event.target.setAttribute("value", "off")
    event.target.parentNode.parentNode.style.cssText = "";
  }
}


// Tabs on Account Page

// Profile
function show_profile() {
  inactive_content = document.querySelectorAll("#content > section")
  for (let content of inactive_content) {
    content.style.cssText = "opacity:0;"
  }

  inactive_tabs = document.querySelectorAll("#tabs h2:not(:first-of-type")
  for (let tab of inactive_tabs) {
    tab.style.cssText = "background:none;"
  }

  document.querySelector("#tabs h2:first-of-type").style.cssText = "background:#ffffff1f;";
  document.getElementById('profile').style.cssText = "visibility:visible;z-index:1";

  let edit_buttons = document.querySelectorAll("#profile > section > img");
  for (let button of edit_buttons) {
  button.addEventListener("click", edit_field, false);
  }

}
function edit_field(event) {
  if (event.target.id == "editing") {
    let inputs = event.target.parentNode.querySelectorAll("input:not(:last-of-type)");

    for (let field of inputs) {
      field.removeAttribute("disabled");
      field.style.cssText = "background:white;transition:2s;";
  }
    event.target.parentNode.querySelector("input:last-of-type").style.cssText = "background:white;transition:2s;cursor:pointer;color:red;";
    event.target.parentNode.querySelector("input:last-of-type").removeAttribute("disabled");
  //   let edit_buttons = document.querySelectorAll("#entries form > img");
  //     for (let button of edit_buttons) {
  //       button.style.visibility = "hidden"; 
  // }  // User might change their mind on which vehicle to edit

}
  else {
  event.target.parentNode.querySelector("input").removeAttribute("disabled");  // Allow user to edit field
  event.target.parentNode.querySelector("input").style.cssText = "background:#4b90b978;transition:2s;";
  save();
  }
}
function save() {
  if (document.getElementById("save_changes").disabled) {
    document.getElementById("save_changes").style.cssText = "opacity:1;transform:translateX(100%);cursor:not-allowed;";
    document.getElementById("current_password").style.cssText = "opacity:1;background:#ffffff40;";
    document.getElementById("current_password").removeAttribute("disabled")

    document.getElementById("current_password").addEventListener("input", function() {
    document.getElementById("save_changes").removeAttribute("disabled")
    document.getElementById("save_changes").style.background = "#009fff"
    document.getElementById("save_changes").style.cursor = "pointer"
  })
}
}

// Orders
function show_orders() {
  inactive_content = document.querySelectorAll("#content > :not(:nth-child(3))")
  for (let content of inactive_content) {
    content.style.cssText = "opacity:0;"
  }

  inactive_tabs = document.querySelectorAll("#tabs h2:not(:nth-of-type(2))")
  for (let tab of inactive_tabs) {
    tab.style.cssText = "background:none;"
  }

  document.querySelector("#tabs h2:nth-of-type(2)").style.cssText = "background:#ffffff1f;"
  document.getElementById('orders').style.cssText = "visibility:visible;z-index:1;"
}

// Admin Settings
function show_admin_settings() {
  inactive_content = document.querySelectorAll("#content > :not(:nth-child(4))")
  for (let content of inactive_content) {
    content.style.cssText = "opacity:0;"
  }

  inactive_tabs = document.querySelectorAll("#tabs h2:not(:nth-of-type(3))")
  for (let tab of inactive_tabs) {
    tab.style.cssText = "background:none;"
  }

  document.querySelector("#tabs h2:last-of-type").style.cssText = "background:#ffffff1f;"
  document.getElementById('admin_settings').style.cssText = "visibility:visible;z-index:1;"
}

// Particle animation on checkout page
let canvas = document.querySelector("canvas");
if (canvas) {
  document.addEventListener("DOMContentLoaded", particles, false);
}

function particles() {
  let context = canvas.getContext("2d");
  let now;
  let then = Date.now();

  let x = canvas.width / 2;
  let y = (canvas.height / 2) + 10;
  let size;
  let xChange;
  let yChange;    
  let color = "#f3" + randint(0,9);
  let particles = [];
  let p;
  
  let fpsInterval = 40;

  document.getElementById("place_order").addEventListener("mouseover", function() {
    color = "cyan";
  });
  document.getElementById("place_order").addEventListener("mouseout", function() {
    color = "#f3" + randint(0,9);
  });



  draw();

  function draw() {
    window.requestAnimationFrame(draw);

        


        let now = Date.now();
        let elapsed = now - then;
        if (elapsed <= fpsInterval) {
            return;
        }
        then = now - (elapsed % fpsInterval);

        for (let i = 0; i < 15; i += 1) { /* controlling the amount of particles spewing out at once */
        
          p = {
                x : x,
                y : y,
                color : color,
                size : 2,
                xChange : randint(-5, 5),
                yChange : randint(-5, 5)
                }
          particles.push(p);
  }
  context.clearRect(0, 0, canvas.width*100, canvas.height*100);

  for (let p of particles) {
    context.fillStyle = p.color;
    context.fillRect(p.x, p.y, p.size, p.size);
  }
  for (let p of particles) {
    p.x += p.xChange;
    p.y += p.yChange;
    p.size = p.size * 0.97
    p.yChange += 0.05;
  }

  }

}

function randint(min, max) {
  return Math.round(Math.random() * (max-min)) + min;
}