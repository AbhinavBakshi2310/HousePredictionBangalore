console.log("Content running");

chrome.runtime.onMessage.addListener(result =>{

  if(result.action == "print_summary"){  
    let sum = document.getElementById('summary');
      sum.innerHTML = result.summary;
      sum.style.textAlign = "left";
  }

  if(result.action == "load_summary"){
    console.log("trying to create div");
    let outer = document.getElementById('info');
        inner = document.createElement("div");
        inner.className = 'style-scope ytd-watch-flexy summary_box';
        inner.id = 'summary-box';
        let inner_text = document.createElement("P");
        inner_text.id = 'summary';
        inner.appendChild(inner_text);
        outer.appendChild(inner);
    let sum = document.getElementById('summary');
    sum.innerHTML = "Loading Summary.......";
    console.log("loading summary");
    sum.style.textAlign = "center";
}    

if(result.action == "clear"){
  let inner = document.getElementById('summary-box');
  if(inner != null)
      inner.remove();
}

});
